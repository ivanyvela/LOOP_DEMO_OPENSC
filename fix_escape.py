with open('web-app/src/data/algorithmMarkdown.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# Instead of manually escaping, we can just use JSON serialization or string.raw to properly escape everything for TypeScript.
import json

with open('Interface_Detection/2026_Interface_Detection.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)
md_text = "".join(nb['cells'][0]['source'])

ts_content = f"export const algorithmMarkdown = {json.dumps(md_text)};"

with open('web-app/src/data/algorithmMarkdown.ts', 'w', encoding='utf-8') as f:
    f.write(ts_content)
