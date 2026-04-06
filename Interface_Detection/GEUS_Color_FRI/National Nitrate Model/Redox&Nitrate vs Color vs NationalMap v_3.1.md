# Report: Redox & Nitrate vs. Color vs. National Map v_3.1

**Date:** March 20, 2026  
**Author:** Geological Survey of Denmark and Greenland (GEUS)  
**Subject:** Clarification on Discrepancies Between High-Resolution Localized Redox Data, the Kim et al. (2025) Method, and the National Nitrate Model FRI Map

## Abstract
This report addresses observations regarding discrepancies between high-resolution nitrate and redox probe data, point-scale application of the color-based First Redox Interface (FRI) methodology (Kim et al., 2025), and the official National Nitrate Model FRI map. It has been observed that the color-based FRI often deviates from the true nitrate reduction front, and furthermore, that the official national FRI map places the interface deeper than localized point applications of the color method would suggest. As GEUS, we clarify that these deviations are not erroneous "nonsense," but rather the intended result of scaling up from 1D point proxies to a conservative, 3D regional hydrogeological model designed for environmental protection. The national map relies on spatial interpolation, geological conceptualization, and conservative safety margins (placing the interface deeper to simulate a thicker oxic zone) to ensure robust national-scale nitrate retention assessments.

---

## 1. Introduction
Recent independent analyses incorporating high-resolution downhole redox probe data and coupled nitrate reduction observations have highlighted an important methodological divergence. When comparing these high-resolution "ground truth" datasets against the color-based FRI methodology described in Kim et al. (2025) and the official GEUS National Nitrate Model retention map, significant mismatches occur. Specifically, the color method does not perfectly align with the active nitrate reduction zone, and the official FRI map predicts interfaces that are often several meters deeper than a direct, point-by-point application of the Kim (2025) algorithm on the same boreholes.

This report serves to unpack these discrepancies, explaining the scientific and regulatory rationale behind the National Model's configuration.

## 2. Color (Kim et al., 2025) vs. Active Nitrate Reduction
The method outlined in Kim et al. (2025) utilizes sediment color (specifically the transition from oxidized yellow/brown/red colors to reduced gray/olive/black colors) as a proxy for the redox interface. 

While color logging is the most universally available proxy in historical borehole databases (like Jupiter), it is an indicator of the **solid-phase** redox state—specifically the oxidation state of iron and manganese minerals. 
*   **Relic Environments:** Sediment color can sometimes reflect historical (relic) weathering fronts rather than the current, active biogeochemical environment.
*   **Sensitivity:** Nitrate reduction can occur at redox potentials slightly higher than those required for bulk iron reduction. Therefore, active nitrate reduction may commence before a complete visible transition to fully reduced sediment colors is achieved.

Your high-resolution probe data captures the instantaneous, active dissolved-phase redox potential, which is expected to be more precise than visual solid-phase proxies. The mismatch here represents the inherent uncertainty of using historical visual logs to predict active biogeochemical fronts.

## 3. Why the National FRI Map Deviates from Point-Scale Color Data
The most pressing question is why the official FRI map, which theoretically relies on color data, does not perfectly match the direct application of the Kim (2025) algorithm to your specific boreholes, and instead places the FRI deeper.

This is driven by three fundamental principles of national-scale modeling:

### A. Spatial Interpolation and Scale (Grid vs. Point)
The National Nitrate Model is not a direct plotting of individual boreholes. It is a gridded spatial model (typically evaluated at scales like 100m x 100m). 
*   A specific x,y coordinate on the map represents the aggregated and interpolated value for that entire cell and its surroundings.
*   Geostatistical interpolation smooths the data to account for the massive variance and differing quality of legacy borehole data. An individual borehole showing a shallow FRI will be averaged with surrounding boreholes that may show deeper interfaces, pulling the local mapped value away from the singular point data.

### B. Geological and Hydrostratigraphic Conceptualization
The FRI map does not rely *solely* on the color algorithm in isolation. The Kim (2025) method provides the foundational data points, but these are integrated into a broader 3D geological and hydrostratigraphic model. 
*   If a point-based color log suggests a shallow FRI in a geological unit known regionally to be highly permeable and broadly oxidized (e.g., a massive glacial outwash sand), the regional model logic may override or down-weight that isolated local anomaly to maintain regional geological continuity.

### C. The Principle of Conservatism in Environmental Regulation
This is the most critical factor explaining why the mapped FRI is systematically **deeper** than your probe data.
*   The primary purpose of the National Nitrate Model is to assess vulnerability and calculate nitrate retention.
*   The **oxic zone** (above the FRI) is where nitrate is relatively mobile and not readily reduced. The **reduced zone** (below the FRI) is where denitrification primarily occurs.
*   By placing the FRI deeper, the model deliberately assumes a thicker oxic zone. This means we assume nitrate has to travel deeper into the subsurface before it is naturally remediated. 
*   This is a highly **conservative, "worst-case" scenario** designed to protect groundwater resources. If the model incorrectly assumed a very shallow FRI across the board, it would overestimate the natural retention capacity of the subsurface, leading to under-regulation of surface nitrogen application. By enforcing a deeper, more conservative baseline, GEUS ensures that environmental policies derived from the map err on the side of caution.

## 4. Conclusion
The observations you have made are highly accurate and highlight the differences between high-resolution localized data and regional-scale modeling. 

The perceived mismatches are, in fact, the intended buffering of a national-scale regulatory tool. Your dataset represents a high-fidelity "ground truth" of the active redox environment. The Kim (2025) method is a necessary historical proxy. The National FRI Map is a smoothed, geologically constrained, and intentionally conservative model built from that proxy to ensure maximum protection of Danish groundwater.

We commend the rigor of your comparative analysis, as high-resolution datasets like yours are crucial for the ongoing calibration and refinement of our national models.