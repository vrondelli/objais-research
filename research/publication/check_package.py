"""Check public reader links, image targets and accidental local/private references."""
from pathlib import Path
from urllib.parse import unquote
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[2]
TEXT_SUFFIXES = {'.md', '.py', '.cjs', '.json', '.csv', '.tex', '.html', '.svg', '.mmd', '.yml'}
forbidden = re.compile(r'/mnt/[a-z]/(?:Users|users)/|/home/[^ /]+/|[A-Za-z]:[\\/](?:Users|users)[\\/]|chatgpt\.com/(?:space/|c/)|\bgh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----')
errors = []
links = 0
images = 0
files = []


def anchors(path):
    found = set()
    for line in path.read_text().splitlines():
        if not re.match(r'^#{1,6} ', line):
            continue
        title = re.sub(r'^#{1,6} ', '', line)
        title = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', title)
        title = re.sub(r'[^\w\s-]', '', title.lower())
        found.add(re.sub(r'\s', '-', title))
    return found


for path in sorted(ROOT.rglob('*')):
    if not path.is_file() or any(x in path.relative_to(ROOT).parts for x in ['.git', 'node_modules', '__pycache__']):
        continue
    relative = path.relative_to(ROOT).as_posix()
    files.append(relative)
    if path.suffix in TEXT_SUFFIXES:
        content = path.read_text(encoding='utf-8-sig')
    elif path.suffix == '.xlsx':
        with zipfile.ZipFile(path) as z:
            content = '\n'.join(z.read(n).decode('utf-8') for n in z.namelist() if n.endswith(('.xml', '.rels')))
    else:
        continue
    if forbidden.search(content):
        errors.append(relative + ': private/local reference or credential-shaped content')
    if path.suffix != '.md':
        continue
    if content.count('```') % 2:
        errors.append(relative + ': unclosed code fence')
    for match in re.finditer(r'(!?)\[[^\]]*\]\((?:<([^>]+)>|([^)]*))\)', content):
        image, angle, plain = match.groups()
        target = angle or plain
        if re.match(r'@[A-Z_]+@', target):
            continue  # Template placeholders are resolved by the guide builder.
        if target.startswith(('http:', 'https:', 'mailto:')):
            continue
        base, _, fragment = unquote(target).partition('#')
        linked = (path.parent / base).resolve() if base else path
        if base.startswith('/') or not linked.is_relative_to(ROOT):
            errors.append(relative + ': nonportable link ' + target)
        elif not linked.exists():
            errors.append(relative + ': missing target ' + target)
        elif fragment and linked.suffix == '.md' and fragment not in anchors(linked):
            errors.append(relative + ': missing anchor ' + target)
        links += 1
        images += bool(image)
assert not errors, '\n'.join(errors)
report = {'status':'pass', 'local_links_and_anchors_checked':links, 'image_links_checked':images,
          'scope':'Public package paths, internal heading anchors and limited accidental-reference scan; external URLs are dated sources, not revalidated here',
          'files_checked':len(files)}
(ROOT / 'research/publication/package-check.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report))
