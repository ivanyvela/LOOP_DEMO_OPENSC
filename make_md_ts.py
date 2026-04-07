import json

with open('Interface_Detection/2026_Interface_Detection.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
md_text = "".join(nb['cells'][0]['source'])
ts_content = f"export const algorithmMarkdown = `{md_text.replace('`', '\\`').replace('$', '\\$')}`;"

with open('web-app/src/data/algorithmMarkdown.ts', 'w', encoding='utf-8') as f:
    f.write(ts_content)

