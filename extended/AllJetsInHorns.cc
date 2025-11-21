#ifndef ALL_JETS_IN_HORNS_H
#define ALL_JETS_IN_HORNS_H

#include "ROOT/RVec.hxx"
#include <cmath>

using namespace ROOT;
using namespace ROOT::VecOps;

// Return true iff ALL jets lie in the HF "horn" region: 2.6 < |eta| < 3.1.
// - If requireNonEmpty==true: function returns false for zero jets.
// - If requireNonEmpty==false: function returns true for zero jets (vacuously true).
inline bool AllJetsInHorns(const RVecF &CleanJet_eta, bool requireNonEmpty = true){
  const size_t n = CleanJet_eta.size();
  if (requireNonEmpty && n == 0) return false;

  for (size_t i = 0; i < n; ++i){
    float aeta = std::fabs(CleanJet_eta[i]);
    // if any jet is NOT inside (2.6, 3.1) -> fail
    if (!(aeta > 2.6f && aeta < 3.1f))
      return false;
  }
  // every jet passed the inside-horn check (or there were zero jets and requireNonEmpty==false)
  return true;
}

#endif // ALL_JETS_IN_HORNS_H
