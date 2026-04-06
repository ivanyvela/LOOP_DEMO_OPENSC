# Redox Probe Open Science Platform (LOOP_DEMO_OPENSC)

This project is an open science website hosting research results for "Redox Probe ability to find FRI (First Redox Interface)".

## Tech Stack
- **Framework**: React (TypeScript) via Vite
- **Styling**: Vanilla CSS / Tailwind (for layout)
- **Visuals**: Framer Motion, PNG + SVG Overlays (Performance optimized)
- **Comments**: Custom React Side-Panel (In-app Field Notes)
- **Deployment**: GitHub Pages

## Methodology Focus
- **Segmented Linear Regression**: Mimicking human identification of redox interfaces by drawing straight lines through data segments (Piecewise Linear Representation).
- **Automated Interface Detection**: Comparing human-picked vs. algorithmic-picked redox boundaries.

## Project Structure
- `web-app/`: Main React application.
  - `src/components/layout/`: Header, Footer.
  - `src/components/sections/`: Individual site sections.
- `Gemini Vault/`: Internal storage for scripts, logs, and intermediate data.
- `Python_Redox_Geochemistry/`: Raw data and metadata.
- `Borehole_Multiplots/`: Notebooks for borehole animations.
- `Nitrate_Focus/`: Logic for nitrate reduction statistics.

## Branding & Colors
- **Header/Dark**: `#2c3e50`
- **Nav/Muted**: `#34495e`
- **Action/Blue**: `#2980b9`
- **Background**: `#f4f6f9`
- **Accent/Text**: `#333`, `#bdc3c7`

## Implementation Status
- [x] Scaffolding & Layout
- [x] Home (Interactive Map)
- [x] Method (Data & Papers)
- [x] History & Contact
- [ ] **Borehole Plots** (In Progress)
  - [x] Implement animated PNG + SVG Overlay based on `Borehole_Multiplots/Animated.ipynb`.
  - [x] Custom "Field Notes" side-panel (Replaces Giscus).
  - [ ] Fine-tune animation speed and data interpolation.
- [ ] **Nitrate Reduction** (In Progress)
  - Need to implement interactive widgets for BOUNDARY_TO_TEST, DISTANCE, etc.
  - Display Donut charts and Validation Matrices.

## Instructions for Parallel Agents
1. **Borehole Plots Agent**:
   - Focus on `web-app/src/components/sections/BoreholePlots/`.
   - Utilize the PNG + SVG Overlay pattern established in `BoreholeChart.tsx`.
   - Implement the "Field Notes" side-panel as a custom React component.
   - Order boreholes: DEMO, LOOP2, LOOP3, etc.

2. **Nitrate Reduction Agent**:
   - Focus on `web-app/src/components/sections/NitrateReduction/`.
   - Read `Nitrate_Focus/N_Reduction_vs_Interfaces.ipynb`.
   - Implement sliding widgets for the 5 parameters.
   - Order boreholes: DEMO, LOOP2, LOOP3, etc.

3. **Data Pre-processor**:
   - Convert large CSVs in `Python_Redox_Geochemistry` into optimized JSON files for web consumption.
   - Store results in `web-app/src/data/`.
