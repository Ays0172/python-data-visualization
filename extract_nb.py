import json, os, sys, glob

folder = sys.argv[1]
outfile = sys.argv[2]
with open(outfile, 'w', encoding='utf-8') as out:
    for nbfile in sorted(glob.glob(os.path.join(folder, '*.ipynb'))):
        out.write(f"\n{'='*60}\n")
        out.write(f"FILE: {os.path.basename(nbfile)}\n")
        out.write('='*60 + '\n')
        with open(nbfile, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        for i, cell in enumerate(nb['cells']):
            src = ''.join(cell.get('source', []))
            if not src.strip():
                continue
            out.write(f"\n[{cell['cell_type'].upper()} #{i}]\n")
            out.write(src[:500] + '\n')
print("Done")
