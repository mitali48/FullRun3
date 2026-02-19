// NoJetInHorn_pT15to50.cc
// Return true only if NO jet lies in horn region (2.5 < |eta| < 3.0)
// with 15 < pt < 50.

#include "ROOT/RVec.hxx"
#include <cmath>

using namespace ROOT;
using namespace ROOT::VecOps;

// Horn region: 2.5 < |eta| < 3.0
// pT requirement: 15 < pt < 50
// Return true → event passes (no problematic jets)
// Return false → event fails (≥1 jet in horns with 15–50 GeV)
bool NoJetInHorn_pT15to50(const RVecF &CleanJet_pt,
                          const RVecF &CleanJet_eta){
  
  size_t n = CleanJet_pt.size();
  size_t m = CleanJet_eta.size();
  size_t N = std::min(n, m);

  for (size_t i = 0; i < N; ++i){
    float pt   = CleanJet_pt[i];
    float aeta = std::fabs(CleanJet_eta[i]);

    bool lowpt   = (pt > 15.0f && pt < 50.0f);
    bool inhorns = (aeta > 2.5f && aeta < 3.0f);

    if (lowpt && inhorns)
      return false;   // event FAILS
  }

  return true;        // event PASSES
}
