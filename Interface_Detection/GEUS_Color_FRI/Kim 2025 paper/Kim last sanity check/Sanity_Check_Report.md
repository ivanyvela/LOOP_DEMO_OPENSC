# Sanity Check Report: Kim et al. 2025 Algorithm Implementation

**Date:** March 21, 2026
**Scope:** Review of `2026_Color_FRI_Algorithm.ipynb` vs `kim et al 2025.pdf`

After a rigorous and tough review of how the color-based First Redox Interface (FRI) algorithm from Kim et al. 2025 was translated into code, several critical discrepancies were identified. The most significant finding is a mathematical misinterpretation of the depth-dependent equations, which heavily biases the model towards premature "reduced" classifications.

## 1. CRITICAL: Mathematical Flaw in the Depth-Dependent P_ox Equation
The algorithm in the Jupyter notebook attempts to recreate the paper's depth-dependent oxic probabilities using an exponential decay equation: `P_ox = A * exp(-k * z)`. 
To do this, it assumes that `A` (the oxic probability at the surface, `z=0`) is equal to the `Raw Oxic Fraction` (the overall average oxic fraction from Table 2).

**Why this is fundamentally incorrect:**
* The `Raw Oxic Fraction` is a depth-averaged statistic across all groundwater screens, NOT the surface intercept. 
* For colors like "Gray" and "Dark grayish brown", their `Raw Oxic Fraction` is `0.05` and `0.04` respectively.
* Because `0.05` is already below the FRI threshold of `0.1`, the script's logic (`if A > 0.1`) fails. It falls back to keeping `P_ox` clamped at `0.05` down to `z_01`, and then linearly dropping it to `0`.
* **The Contradiction:** Table 4 explicitly states that for "Gray", the depth where `P_ox = 0.1` (`z_01`) is **40.1m**. It is mathematically impossible for the probability to be `0.1` at `40.1m` if the maximum possible probability at the surface is capped at `0.05`. 
* **The Result:** The implemented code *never* allows "Gray" or "Dark grayish brown" to exceed a `P_ox` of `0.1`. Consequently, the algorithm will trigger a false-positive redox interface immediately at the top of these layers, completely ignoring the 30-40 meters of potential oxic zone defined by Table 4.

**The Paper's True Intent:**
Looking at Figure 5 in the paper, the surface oxic fraction for "Gray" is actually around `~0.35`, and it decreases with depth. If we use a simple linear fit between the paper's two defined points: `(z_01, 0.1)` and `(z_0, 0)`, the equation becomes:
`P_ox(z) = 0.1 * (z_0 - z) / (z_0 - z_01)`
For Gray (`z_01=40.1`, `z_0=55.6`), at `z=0`, `P_ox(0) = 0.358`. This perfectly matches Figure 5. The exponential logic mixed with `Raw Oxic Fraction` must be discarded in favor of a direct regression between the provided `z_01` and `z_0` points.

## 2. Missing Key Table 4 Color: "Brownish gray"
The paper prominently features "Brownish gray" (`n=371`) in Table 4, with `z_01 = 46.5m` and `z_0 = 77.2m`.
* **The Discrepancy:** The Danish equivalent "brungrå" is missing from `Color_mapping.csv`. In the notebook (`2026_Color_FRI_Algorithm.ipynb`), `table4_params` completely omits "Brownish gray". 
* **The Patch:** The code includes a fallback: `elif 'brownish gray' in key: key = 'Light brownish gray'`. This maps the missing color to the parameters of "Light brownish gray" (`z_01 = 41.8m`, `z_0 = 59.9m`). This artificial mapping introduces an error of ~5m for `z_01` and ~17m for `z_0` for any sediment that gets translated to this color.

## 4. Lithology Penalties (Sanity Check: Passed)
* **The Paper:** "the oxic probability for fine-grained materials was adjusted to 20% of the originally predicted values." and "organic-rich materials... were adjusted to zero unless predicted oxic probability was 1".
* **The Implementation:** This is executed flawlessly. The `get_litho_factor` successfully multiplies fine-grained outcomes by `0.2` and respects the `unless P_ox=1` override for organic materials like Gyttja.

## Conclusion & Recommendation
The Kim et al. 2025 algorithm was **NOT** applied 100% correctly. The misinterpretation of the `Raw Oxic Fraction` as the y-intercept for depth-dependent equations fundamentally sabotages the calculation for transitional colors (Gray, Dark grayish brown), prematurely triggering the FRI.

**Required Fixes in `2026_Color_FRI_Algorithm.ipynb`:**
1. Rip out the exponential decay logic `P = A * exp(-k * z)`.
2. Replace it with a linear interpolation based strictly on Table 4 parameters:
   `P_ox = 0.1 + (0.1 / (z_01 - z_0)) * (z - z_01)`
   capped between `0.0` and `1.0`.
3. Add "Brownish gray": `(46.5, 77.2)` to the `table4_params` dictionary.