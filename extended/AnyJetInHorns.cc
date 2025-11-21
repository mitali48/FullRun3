#ifndef JET_HORNS_NO_PT
#define JET_HORNS_NO_PT

#include "ROOT/RVec.hxx"
#include <cmath>

using namespace ROOT;
using namespace ROOT::VecOps;
using namespace std;

// Return true if any jet is in the HF "horn" region (2.6 < |eta| < 3.1)
// No pT requirement applied.
bool AnyJetInHorns(RVecF const & CleanJet_eta){
  for (unsigned int i = 0; i < CleanJet_eta.size(); ++i){
    if ( fabs(CleanJet_eta[i]) <= 2.6 && fabs(CleanJet_eta[i]) >= 3.1 )
      return false;
  }
  return true;
}

#endif