import os

# Read the original script
with open('N_Reduction_vs_Interfaces.py', 'r') as f:
    script_content = f.read()

# Define the parameter combinations
boundaries = ['redox_primary', 'redox_secondary', 'geus_fri', 'color_with_litho', 'color_without_litho']
ratios = [0.5, 0.8]
thresholds = [1.5, 5.0]

for b in boundaries:
    for r in ratios:
        for t in thresholds:
            print(f"Generating for {b}, ratio={r}, threshold={t}...")
            
            # The identifiers for the files
            r_int = int(r * 100)
            t_str = str(t).replace('.', '_')
            suffix = f"{b}_{r_int}_{t_str}"
            
            # Modify the script string
            modified = "def display(*args, **kwargs): pass\n" + script_content
            
            # 1. Replace Boundary
            modified = modified.replace(
                "BOUNDARY_TO_TEST = 'redox_primary'",
                f"BOUNDARY_TO_TEST = '{b}'"
            )
            
            # 2. Replace Ratio
            modified = modified.replace(
                "'REDUCTION_RATIO': 0.7,",
                f"'REDUCTION_RATIO': {r},"
            )
            
            # 3. Replace Threshold
            modified = modified.replace(
                "'NO_NITRATE_THRESHOLD': 5,",
                f"'NO_NITRATE_THRESHOLD': {t},"
            )
            
            # 4. Replace plt.show() for Validation Matrix
            modified = modified.replace(
                "plt.title(f'Validation Matrix against {BOUNDARY_TO_TEST}', pad=30, size=16, weight='bold')\nplt.tight_layout(); plt.show()",
                f"plt.title(f'Validation Matrix against {{BOUNDARY_TO_TEST}}', pad=30, size=16, weight='bold')\nplt.tight_layout(); plt.savefig(f'../web-app/public/plots/nitrate_validation_matrix_{suffix}.png', bbox_inches='tight'); plt.close()"
            )
            
            # 5. Replace plt.show() for Success Rates
            modified = modified.replace(
                "plt.suptitle(f'Success Rates against {BOUNDARY_TO_TEST}', size=16, weight='bold', y=1.05)\nplt.show()",
                f"plt.suptitle(f'Success Rates against {{BOUNDARY_TO_TEST}}', size=16, weight='bold', y=1.05)\nplt.tight_layout(); plt.savefig(f'../web-app/public/plots/nitrate_success_rates_{suffix}.png', bbox_inches='tight'); plt.close()"
            )
            
            # 6. Replace plt.show() for Profiles
            modified = modified.replace(
                "plt.tight_layout(); plt.show()",
                f"plt.tight_layout(); plt.savefig(f'../web-app/public/plots/nitrate_profiles_{suffix}.png', bbox_inches='tight'); plt.close()"
            )
            
            # To avoid the heatmap tight_layout replacement messing up the Profiles replacement (if any overlap), 
            # I made sure the heatmap string included the title, and the Profiles one is just the remaining one.
            
            # Execute the modified script
            try:
                exec(modified, globals())
            except Exception as e:
                print(f"Failed on {b} {r} {t}: {e}")

print("Done generating all combinations!")
