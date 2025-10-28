import os
import sys

bad = []
roots = [
    'mckinsey-ppt-generator/app',
    'mckinsey-ppt-generator/frontend',
]

for scan_root in roots:
    for root, _, files in os.walk(scan_root):
        for f in files:
            if f.endswith('.py'):
                p = os.path.join(root, f)
                b = open(p,'rb').read()
                try:
                    b.decode('utf-8')
                except Exception as e:
                    print('NON-UTF8:', p, e)
                    bad.append(p)
print('Bad files:', len(bad))

for p in bad:
    b = open(p,'rb').read()
    decoded = None
    for enc in ('cp949','euc-kr','latin1'):
        try:
            decoded = b.decode(enc)
            break
        except Exception:
            pass
    if decoded is None:
        print('SKIP (unknown encoding):', p)
        continue
    if not decoded.lstrip().startswith('# -*- coding: utf-8 -*-'):
        decoded = '# -*- coding: utf-8 -*-\n' + decoded
    open(p,'wb').write(decoded.encode('utf-8'))
    print('Converted to UTF-8:', p)
