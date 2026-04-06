 Here is a complete summary of the "competition" rules governing how the different boundary detection methods (redox_primary, redox_secondary, geus_fri, color_with_litho,
  color_without_litho) are evaluated. 

  1. The Rules of the Competition

  The ultimate goal of this validation is to determine which detected boundary is the most spatially coincident with the actual onset of groundwater nitrate reduction.

  The Ground Truth (Geochemical Reality):
  Through manual geochemical analysis, we have established a universal ground truth for the dataset:
   * No True Reduction: Boreholes LOOP2 1 and LOOP2 2A do not exhibit genuine, stable nitrate reduction in their profiles.
   * True Reduction: Every other borehole in the dataset exhibits an active zone of nitrate reduction.

  The Scoring Logic:
  Every boundary method is subjected to the exact same logic matrix for every borehole:

   1. The "True Negative" Test (LOOP2 1 & LOOP2 2A):
       * If a method FAILS to call a boundary here, it is rewarded by being Excluded (No N reduction) from the statistics. It correctly avoided a false positive.
       * If a method CALLS a boundary here, it receives a Fail across all metrics. It is penalized for hallucinating a redox boundary in a zone with no meaningful nitrate
         reduction.
   2. The "False Negative" Test (All other boreholes):
       * If a method FAILS to call a boundary (returns NaN) in any other borehole, it receives a Fail across all metrics. It is penalized for completely missing a known,
         active reduction zone.
   3. The Spatial Coincidence Test (When a boundary is found):
       * If a method finds a boundary in a borehole with true reduction, we draw a 1-meter and 2-meter window around that specific boundary's depth (bz).
       * N-Reduction Check: Does the nitrate drop by 50% (or below the threshold) strictly within this spatial window?
           * Strict Mode: The drop must occur relative to the interpolated nitrate concentration exactly at the top of the window.
           * Relaxed Mode: The drop must occur relative to the global maximum baseline above the interface.
       * Zero Nitrate Check: Does the nitrate drop below the NO_NITRATE_THRESHOLD within 1m or 2m below the boundary, and remain stable/low deeper in the profile?
   4. Handling Sparse Data:
       * If no physical water samples were taken strictly inside a 1m or 2m evaluation window, the algorithm interpolates a straight line between the closest samples above
         and below the window to fairly estimate the concentration at that depth, rather than throwing out the borehole.

  ---

  2. Algorithmic Decision Diagram

  Here is a flowchart illustrating the decision tree applied to every single borehole for any given BOUNDARY_TO_TEST:

    1 graph TD
    2     Start([Start: Evaluate Boundary Method for Borehole]) --> IsLoop2{Is Borehole LOOP2 1<br/>or LOOP2 2A?}
    3     
    4     %% True Negative Path
    5     IsLoop2 -- YES<br/>(No True Reduction) --> FoundBoundaryLoop2{Did the method<br/>find a boundary?}
    6     FoundBoundaryLoop2 -- YES --> PenalizeFalsePos[Mark as FAIL<br/>Penalty for False Positive]
    7     FoundBoundaryLoop2 -- NO --> RewardTrueNeg[Mark as EXCLUDED<br/>Reward for True Negative]
    8     
    9     %% True Positive Path
   10     IsLoop2 -- NO<br/>(True Reduction Exists) --> FoundBoundaryOther{Did the method<br/>find a boundary?}
   11     FoundBoundaryOther -- NO --> PenalizeFalseNeg[Mark as FAIL<br/>Penalty for Missing Reduction Zone]
   12     FoundBoundaryOther -- YES --> SpatialEval[Create 1m & 2m windows<br/>around the proposed Boundary depth]
   13     
   14     %% Data Check
   15     SpatialEval --> CheckData{Are there physical samples<br/>inside the windows?}
   16     CheckData -- NO --> Interpolate[Interpolate nitrate values<br/>using samples above & below]
   17     CheckData -- YES --> EvaluateWindow
   18     Interpolate --> EvaluateWindow
   19     
   20     %% Evaluation
   21     EvaluateWindow --> StrictRelaxed{Evaluate Nitrate<br/>Reduction}
   22     
   23     StrictRelaxed -- Strict Logic --> StrictCheck[Does nitrate drop 50% relative to<br/>the concentration at window entry?]
   24     StrictRelaxed -- Relaxed Logic --> RelaxedCheck[Does nitrate drop 50% relative to<br/>the global maximum above interface?]
   25     
   26     StrictCheck -- YES --> PassReduction[N-Reduction: PASS]
   27     StrictCheck -- NO --> FailReduction[N-Reduction: FAIL]
   28     RelaxedCheck -- YES --> PassReduction
   29     RelaxedCheck -- NO --> FailReduction
   30     
   31     EvaluateWindow --> ZeroCheck{Does nitrate hit near-zero<br/>below boundary & stay low?}
   32     ZeroCheck -- YES --> PassZero[Zero Nitrate: PASS]
   33     ZeroCheck -- NO --> FailZero[Zero Nitrate: FAIL]

  ---

  3. Are any boundaries receiving favorable treatment (Bias)?

  When designing a competition like this, it is critical to acknowledge inherent methodological biases. While the mathematical code applies the rules equally to all methods,
  the geochemical assumptions underlying the rules inherently favor the Redox Probe (redox_primary). 

  Here is why reviewers might point out favorable treatment:

  1. The Window Size Bias (The Depth of the Redox Sequence)
  The rules require the nitrate to drop within a strict 1-meter or 2-meter window around the boundary. 
   * The Redox Probe physically measures the electron activity of the microbes actively performing denitrification. Therefore, its signal will naturally spike at the exact
     depth where nitrate disappears.
   * Sediment Color (color_without_litho), however, responds to the oxidation state of Iron (Fe). In the classic groundwater redox sequence, oxygen is depleted first, then
     nitrate is reduced, and only later (often deeper) is Iron reduced (changing the sediment color from red/brown to gray/green). 
   * The Bias: If the Iron reduction boundary physically occurs 3 meters deeper than the nitrate reduction boundary in the aquifer, the color method will Fail our 1m/2m
     window test. It successfully found the redox sequence, but it failed our test because our metric demands spatial coincidence specifically with Nitrate, implicitly
     favoring the sensor that reacts to Nitrogen over the sensor that reacts to Iron.

  2. Parameter Overfitting
  Parameters like NO_NITRATE_THRESHOLD = 1.5 or REDUCTION_RATIO = 0.5 were likely established by observing the performance of the Redox Probe. If these thresholds were
  fine-tuned specifically to maximize the success rate of redox_primary, other methods are forced to compete on a playing field optimized for the probe's specific
  sensitivity.