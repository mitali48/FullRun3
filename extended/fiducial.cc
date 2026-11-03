#ifndef FIDUCIAL
#define FIDUCIAL

#include <vector>
#include <string>
#include <iostream>
#include <cmath>

#include "TString.h"
#include "TVector2.h"
#include "ROOT/RVec.hxx"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

using namespace ROOT;
using namespace ROOT::VecOps;

bool Fiducial(
    const RVecF& DressedLepton_pt,
    const RVecF& DressedLepton_eta,
    const RVecF& DressedLepton_phi,
    const RVecF& DressedLepton_mass,
    const RVecI& DressedLepton_pdgId,
    const RVecI& LeptonGen_MotherPID
)

{
    // Number of dressed leptons
    const std::size_t nL = DressedLepton_pt.size();
    if (nL < 2)
        return false;

    std::vector<std::size_t> iPromptL;
    iPromptL.reserve(nL);

    for (std::size_t iL = 0; iL < nL; ++iL) {

    // Keep only electrons and muons
    const auto absId = std::abs(DressedLepton_pdgId[iL]);
    if (absId != 11 && absId != 13)
        continue;

    // // Reject leptons from tau decays
    // if (std::abs(LeptonGen_MotherPID[iL]) == 15)
    //     continue;

    // // Require direct W decay
    // if (std::abs(LeptonGen_MotherPID[iL]) != 24)
    //     continue;

    iPromptL.emplace_back(iL);
}

    if (iPromptL.size() < 2)
        return false;

        // Reject events with an additional prompt lepton
    if (iPromptL.size() >= 3 && DressedLepton_pt[iPromptL[2]] > 10.)
        return false;

    // Require an opposite-sign eμ pair
    const auto pdgId0 = DressedLepton_pdgId[iPromptL[0]];
    const auto pdgId1 = DressedLepton_pdgId[iPromptL[1]];

    if (pdgId0 * pdgId1 != -143)
        return false;

    // Require both leptons to originate directly from a W boson
    if (std::abs(LeptonGen_MotherPID[iPromptL[0]]) != 24 ||
        std::abs(LeptonGen_MotherPID[iPromptL[1]]) != 24)
        return false;

    // pT and η requirements
    if (DressedLepton_pt[iPromptL[0]] < 25. ||
        std::abs(DressedLepton_eta[iPromptL[0]]) > 2.5 ||
        DressedLepton_pt[iPromptL[1]] < 20. ||
        std::abs(DressedLepton_eta[iPromptL[1]]) > 2.5)
        return false;

    // Build the dilepton four-vectors
    ROOT::Math::PtEtaPhiMVector pl0(
        DressedLepton_pt[iPromptL[0]],
        DressedLepton_eta[iPromptL[0]],
        DressedLepton_phi[iPromptL[0]],
        DressedLepton_mass[iPromptL[0]]
    );

    ROOT::Math::PtEtaPhiMVector pl1(
        DressedLepton_pt[iPromptL[1]],
        DressedLepton_eta[iPromptL[1]],
        DressedLepton_phi[iPromptL[1]],
        DressedLepton_mass[iPromptL[1]]
    );

    // Dilepton invariant mass
    if ((pl0 + pl1).M() <= 85.)
        return false;

        return true;
    }
#endif