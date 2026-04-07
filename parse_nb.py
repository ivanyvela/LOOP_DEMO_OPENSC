import json

def get_markdown(nb_path):
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print("MARKDOWN:")
    print("".join(nb['cells'][0]['source']))
    print("---")

get_markdown('Interface_Detection/2026_Interface_Detection.ipynb')
