# Internal Review: Critical Assessment of the National Nitrate Model's Local Allocation Deficits

**Date:** March 21, 2026  
**Author:** Geological Survey of Denmark and Greenland (GEUS) - Internal Modeling & Data Integration Review Board  
**Subject:** Limitations of the National FRI Model in Capturing High-Resolution Individual Soundings

## 1. Introduction and Problem Statement
Following recent comparative analyses incorporating high-resolution, continuous redox probe data against our standard color-based First Redox Interface (FRI) methodology (Kim et al., 2025) and the National Nitrate Model retention map, a critical discrepancy has emerged. While we have historically defended the national map's deviations as necessary artifacts of regional scaling and regulatory conservatism (as outlined in previous memos), we must critically ask ourselves: **Why is the national model fundamentally incapable of accurately allocating and reflecting these individual, high-fidelity soundings?**

This internal critique examines the structural, methodological, and conceptual limitations of our current national modeling framework when confronted with high-resolution localized data.

## 2. The Resolution Mismatch: Grid vs. Geological Reality
The most glaring deficit is the spatial resolution of the National Nitrate Model. Operating on a standardized grid (e.g., 100m x 100m), the model assigns a single, homogenized FRI depth to a vast spatial volume.
*   **Subsurface Heterogeneity:** Glacial and post-glacial landscapes in Denmark are notoriously heterogeneous. A single 100m grid cell can contain highly variable redox boundaries, sand lenses (geological windows), and clay aquitards.
*   **Loss of Local Vulnerability:** By averaging out these variations, the model intrinsically fails to represent specific, localized pathways for nitrate transport or localized zones of high reduction capacity. A high-resolution sounding that detects a shallow, active reduction zone is swallowed by the statistical average of surrounding legacy boreholes.

## 3. The Tyranny of Smoothing and Interpolation
Our geostatistical interpolation methods (e.g., kriging) are designed to create a continuous, aesthetically pleasing, and mathematically stable national surface. However, this mathematical smoothing acts as a low-pass filter on geological reality.
*   **Erasing Anomalies:** When an individual high-resolution probe identifies a sharp, accurate redox interface that contradicts the regional trend, the interpolation algorithm treats it as an anomaly or "noise" to be smoothed over.
*   **Rigidity of the Geological Conceptualization:** The national map heavily weights the overarching 3D hydrostratigraphic model. If a local sounding identifies an FRI depth that conflicts with the "expected" regional geological unit (e.g., finding reduced conditions in a regionally mapped oxic sand unit), the model logic often overrides the empirical point data to maintain regional continuity. This enforces a top-down geological assumption over bottom-up empirical reality.

## 4. The Vulnerability of Legacy Data (The Color Proxy)
The national model's foundational input relies on decades of legacy data from the Jupiter database, primarily visual color logs.
*   **Subjectivity and Sparsity:** Color logging is subjective, categorical, and often recorded at coarse depth intervals. It represents the solid-phase oxidation state of minerals, which can be a relic of past geological eras rather than the active biogeochemical environment.
*   **Incompatibility with Active Sensors:** High-resolution probes measure active, dissolved-phase redox potentials at a centimeter scale. The national model currently lacks the mathematical and structural flexibility to appropriately weight this high-fidelity, continuous "ground truth" data against the massive volume of low-fidelity, discrete categorical legacy data. The model is anchored by the sheer inertia of historical data.

## 5. The Double-Edged Sword of "Conservatism"
We have justified pushing the mapped FRI deeper as a "conservative" safety measure to assume a thicker oxic zone and protect groundwater. However, from a critical scientific standpoint:
*   **Local Inaccuracy:** While conservative at the macro-catchment scale, this intentional bias renders the model highly inaccurate at the point scale (e.g., the individual farm or field). 
*   **Misallocation of Retention:** By failing to capture true local variations, the model may drastically misallocate natural retention estimates. It may classify a highly protected local aquifer as vulnerable, or worse, miss a critical local "geological window" because the surrounding grid cells averaged it out to a "safe" depth.

## 6. Conclusion and Future Imperatives
The inability of the National Nitrate Model to allocate individual, high-resolution soundings is not merely a scaling artifact; it is a symptom of a modeling framework optimized for regional regulatory averaging rather than localized hydro-biogeochemical accuracy. 

To remain at the forefront of subsurface mapping, GEUS must address this limitation. We must develop localized, adaptive modeling frameworks capable of ingesting high-frequency continuous sensor data without losing it to regional interpolation, allowing for dynamic, multi-scale assessments rather than relying solely on a rigid national grid.