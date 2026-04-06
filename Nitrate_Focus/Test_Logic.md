---

  Nitrate Reduction Validation Criteria
  To quantitatively assess the alignment between the identified redox interfaces and geochemical nitrate attenuation, we established three distinct validation tests: Threshold, Strict Reduction, and Relaxed Reduction. These tests evaluate the spatial progression of nitrate
  depletion within defined depth intervals (DISTANCE_1 and DISTANCE_2, typically 1 m and 2 m) immediately below the predicted interface. To ensure analytical robustness, boreholes are only evaluated for reduction if their historical maximum nitrate concentration in the overlying
  oxic zone exceeds a required baseline (MIN_BASELINE_FOR_REDUCTION). 

  The three validation frameworks are defined as follows:

  1. Threshold Depletion Test
  This test evaluates absolute nitrate removal. An interface passes if the nitrate concentration within the evaluation window drops below a defined background limit (NO_NITRATE_THRESHOLD). To ensure the depletion represents a true geochemical transition rather than a transient
  anomaly, the concentration must remain stable below this threshold for all subsequent measurements deeper in the profile. The STABILITY_MARGIN defines the allowable variance for this deeper stability check, permitting subsequent data points to fluctuate slightly (e.g., by 10%
  if set to 0.10) above the NO_NITRATE_THRESHOLD without failing the validation.

  2. Strict Reduction Test (Local Gradient)
  This test evaluates the immediate, localized intensity of nitrate attenuation across the interface. It requires the minimum nitrate concentration within the evaluation window to decrease by a specified proportion (REDUCTION_RATIO) relative to the concentration at the exact
  point it entered the window. Furthermore, boreholes that have already experienced a pre-emptive drop of >50% before reaching the interface window are rejected, ensuring the metric isolates the localized reduction gradient directly associated with the predicted boundary.

  3. Relaxed Reduction Test (System-Scale Depletion)
  This test evaluates overall systemic depletion rather than localized gradients. It considers an interface validated if the minimum nitrate concentration within the evaluation window drops by the required REDUCTION_RATIO relative to the absolute maximum nitrate concentration
  observed anywhere in the overlying oxic zone. This approach accommodates broader, more diffuse transition zones where initial nitrate decline may begin slightly above the strictly defined redox boundary.

  ---