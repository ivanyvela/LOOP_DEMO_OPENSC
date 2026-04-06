import json
import os
import re

WORKSPACE_ROOT = "/home/ivany/agentic_initiation/LOOP_DEMO_OPENSC"

def convert_notebook_to_script(notebook_path, output_script_path, output_prefix="", is_dissolved=False):
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    code_lines = []
    
    # Add imports and variables
    code_lines.append("import os")
    code_lines.append("import json")
    code_lines.append("all_animations = {}")
    code_lines.append("OUTPUT_PLOTS_DIR = '/home/ivany/agentic_initiation/LOOP_DEMO_OPENSC/web-app/public/plots'")
    code_lines.append("os.makedirs(OUTPUT_PLOTS_DIR, exist_ok=True)")

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            
            # Fix relative paths to point to workspace root
            source = source.replace("'..', 'Python_Redox_Geochemistry'", f"'{WORKSPACE_ROOT}', 'Python_Redox_Geochemistry'")
            source = source.replace("'..', 'Interface_Detection'", f"'{WORKSPACE_ROOT}', 'Interface_Detection'")
            source = source.replace("'../Interface_Detection/Extracted_Advanced_Interfaces.csv'", f"'{WORKSPACE_ROOT}/Interface_Detection/Extracted_Advanced_Interfaces.csv'")
            source = source.replace("'../Python_Redox_Geochemistry/", f"'{WORKSPACE_ROOT}/Python_Redox_Geochemistry/")
            
            # Remove html displays, replace with savefig and JSON logging
            source = re.sub(r'import base64.*?display\(HTML\(custom_html\)\)', 
                            f'''
    save_name = "{output_prefix}" + f"{{loop_nr}}_{{display_id}}.png"
    save_path = os.path.join(OUTPUT_PLOTS_DIR, save_name)
    fig.savefig(save_path, dpi=300)
    plt.close(fig)
    all_animations["{output_prefix}" + f"{{loop_nr}}_{{display_id}}"] = anim_data
''', 
                            source, flags=re.DOTALL)
            code_lines.append(source)
            code_lines.append("\n")
            
    if is_dissolved:
        code_lines.append("""
with open('/home/ivany/agentic_initiation/LOOP_DEMO_OPENSC/web-app/src/data/plot_animations_dissolved.json', 'w') as f:
    json.dump(all_animations, f)
""")
    else:
        code_lines.append("""
with open('/home/ivany/agentic_initiation/LOOP_DEMO_OPENSC/web-app/src/data/plot_animations.json', 'w') as f:
    json.dump(all_animations, f)
""")
        
    with open(output_script_path, "w", encoding="utf-8") as f:
        f.write("\n".join(code_lines))

print("Converting Animated.ipynb...")
convert_notebook_to_script(
    os.path.join(WORKSPACE_ROOT, "Borehole_Multiplots/Animated.ipynb"), 
    os.path.join(WORKSPACE_ROOT, "Gemini Vault/run_animated.py")
)

print("Converting Animated_Dissolved.ipynb...")
convert_notebook_to_script(
    os.path.join(WORKSPACE_ROOT, "Borehole_Multiplots/Animated_Dissolved.ipynb"), 
    os.path.join(WORKSPACE_ROOT, "Gemini Vault/run_animated_dissolved.py"),
    output_prefix="dissolved_",
    is_dissolved=True
)
