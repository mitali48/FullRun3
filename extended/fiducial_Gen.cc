#ifndef FIDUCIALGEN
#define FIDUCIALGEN

#include <vector>
#include <algorithm>
#include <cmath>
#include <cstddef>

#include "ROOT/RVec.hxx"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

using namespace ROOT;
using namespace ROOT::VecOps;


// ============================================================
// Helper structure for a dressed lepton
// ============================================================

struct GenDressedLepton {

    float pt;
    float eta;
    float phi;
    float mass;

    int pdgId;

    // Mother information
    int immediateMotherPID;
    int originalMotherPID;

    // W/tau ancestry
    bool hasWMother;
    bool hasTauMother;
    bool directFromW;
};


// ============================================================
// Delta phi
// ============================================================

inline float DeltaPhiGen(float phi1, float phi2)
{
    float dphi = phi1 - phi2;

    while (dphi > M_PI)
        dphi -= 2.0 * M_PI;

    while (dphi <= -M_PI)
        dphi += 2.0 * M_PI;

    return dphi;
}


// ============================================================
// Delta R^2
// ============================================================

inline float DeltaR2Gen(
    float eta1,
    float phi1,
    float eta2,
    float phi2
)
{
    const float deta = eta1 - eta2;
    const float dphi = DeltaPhiGen(phi1, phi2);

    return deta * deta + dphi * dphi;
}


// ============================================================
// Find the first ancestor with a different PDG ID.
//
// Example:
//
// e -> e -> e -> W
//
// gives W.
//
// For
//
// e -> tau -> W
//
// gives tau.
//
// This is the "original/distinct mother" that we want for
// identifying whether the lepton came directly from W.
// ============================================================

int FindOriginalMotherPID(
    int leptonIdx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    if (leptonIdx < 0 ||
        leptonIdx >= static_cast<int>(GenPart_pdgId.size()))
        return 0;

    const int leptonPID = GenPart_pdgId[leptonIdx];

    int current = leptonIdx;

    // Protect against malformed/circular ancestry
    const int maxDepth = static_cast<int>(GenPart_pdgId.size());

    for (int depth = 0; depth < maxDepth; ++depth) {

        if (current < 0 ||
            current >= static_cast<int>(GenPart_genPartIdxMother.size()))
            return 0;

        const int motherIdx = GenPart_genPartIdxMother[current];

        if (motherIdx < 0 ||
            motherIdx >= static_cast<int>(GenPart_pdgId.size()))
            return 0;

        const int motherPID = GenPart_pdgId[motherIdx];

        // Skip copies of the same particle.
        if (std::abs(motherPID) != std::abs(leptonPID))
            return motherPID;

        current = motherIdx;
    }

    return 0;
}


// ============================================================
// Check whether the lepton has a W ancestor.
// ============================================================

bool HasWMotherGen(
    int leptonIdx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    if (leptonIdx < 0 ||
        leptonIdx >= static_cast<int>(GenPart_pdgId.size()))
        return false;

    int current = leptonIdx;

    const int maxDepth = static_cast<int>(GenPart_pdgId.size());

    for (int depth = 0; depth < maxDepth; ++depth) {

        if (current < 0 ||
            current >= static_cast<int>(GenPart_genPartIdxMother.size()))
            return false;

        const int motherIdx = GenPart_genPartIdxMother[current];

        if (motherIdx < 0 ||
            motherIdx >= static_cast<int>(GenPart_pdgId.size()))
            return false;

        const int motherPID = GenPart_pdgId[motherIdx];

        if (std::abs(motherPID) == 24)
            return true;

        current = motherIdx;
    }

    return false;
}


// ============================================================
// Check whether the lepton has a tau ancestor.
// ============================================================

bool HasTauMotherGen(
    int leptonIdx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    if (leptonIdx < 0 ||
        leptonIdx >= static_cast<int>(GenPart_pdgId.size()))
        return false;

    int current = leptonIdx;

    const int maxDepth = static_cast<int>(GenPart_pdgId.size());

    for (int depth = 0; depth < maxDepth; ++depth) {

        if (current < 0 ||
            current >= static_cast<int>(GenPart_genPartIdxMother.size()))
            return false;

        const int motherIdx = GenPart_genPartIdxMother[current];

        if (motherIdx < 0 ||
            motherIdx >= static_cast<int>(GenPart_pdgId.size()))
            return false;

        const int motherPID = GenPart_pdgId[motherIdx];

        if (std::abs(motherPID) == 15)
            return true;

        current = motherIdx;
    }

    return false;
}


// ============================================================
// Check direct W origin.
//
// Important:
//
// W -> e
//       accepted
//
// W -> tau -> e
//          rejected
//
// e -> e -> W
//       accepted
//
// Therefore we use the first DISTINCT ancestor.
// ============================================================

bool IsDirectFromWGen(
    int leptonIdx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    const int originalMother = FindOriginalMotherPID(
        leptonIdx,
        GenPart_pdgId,
        GenPart_genPartIdxMother
    );

    return std::abs(originalMother) == 24;
}


// ============================================================
// Build dressed leptons from GenPart
//
// Leptons:
//   status == 1
//   abs(pdgId) == 11 or 13
//
// Photons:
//   status == 1
//   pdgId == 22
//
// Dressing:
//   add all photons with DeltaR < 0.1
//
// The dressed leptons are finally sorted by pT.
// ============================================================

std::vector<GenDressedLepton> BuildDressedLeptonsGen(
    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,
    const RVecI& GenPart_genPartIdxMother
)
{
    std::vector<GenDressedLepton> dressedLeptons;

    const std::size_t nGen = GenPart_pt.size();

    // --------------------------------------------------------
    // Find stable e/mu
    // --------------------------------------------------------

    for (std::size_t i = 0; i < nGen; ++i) {

        const int absPID = std::abs(GenPart_pdgId[i]);

        if (GenPart_status[i] != 1)
            continue;

        if (absPID != 11 && absPID != 13)
            continue;


        // ----------------------------------------------------
        // Start with the lepton four-vector
        // ----------------------------------------------------

        ROOT::Math::PtEtaPhiMVector p4(
            GenPart_pt[i],
            GenPart_eta[i],
            GenPart_phi[i],
            GenPart_mass[i]
        );


        // ----------------------------------------------------
        // Add photons within DeltaR < 0.1
        // ----------------------------------------------------

        for (std::size_t j = 0; j < nGen; ++j) {

            if (GenPart_status[j] != 1)
                continue;

            if (GenPart_pdgId[j] != 22)
                continue;

            const float dR2 = DeltaR2Gen(
                GenPart_eta[i],
                GenPart_phi[i],
                GenPart_eta[j],
                GenPart_phi[j]
            );

            if (dR2 >= 0.1 * 0.1)
                continue;

            ROOT::Math::PtEtaPhiMVector photon(
                GenPart_pt[j],
                GenPart_eta[j],
                GenPart_phi[j],
                GenPart_mass[j]
            );

            p4 += photon;
        }


        // ----------------------------------------------------
        // Mother information
        // ----------------------------------------------------

        const int immediateMotherIdx =
            (i < GenPart_genPartIdxMother.size())
                ? GenPart_genPartIdxMother[i]
                : -1;

        int immediateMotherPID = 0;

        if (immediateMotherIdx >= 0 &&
            immediateMotherIdx < static_cast<int>(nGen)) {

            immediateMotherPID =
                GenPart_pdgId[immediateMotherIdx];
        }


        const int originalMotherPID =
            FindOriginalMotherPID(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );


        const bool hasW =
            HasWMotherGen(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );

        const bool hasTau =
            HasTauMotherGen(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );

        const bool directFromW =
            IsDirectFromWGen(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );


        GenDressedLepton dl;

        dl.pt  = p4.Pt();
        dl.eta = p4.Eta();
        dl.phi = p4.Phi();
        dl.mass = p4.M();

        dl.pdgId = GenPart_pdgId[i];

        dl.immediateMotherPID = immediateMotherPID;
        dl.originalMotherPID  = originalMotherPID;

        dl.hasWMother = hasW;
        dl.hasTauMother = hasTau;
        dl.directFromW = directFromW;

        dressedLeptons.push_back(dl);
    }


    // --------------------------------------------------------
    // Sort by dressed lepton pT
    // --------------------------------------------------------

    std::sort(
        dressedLeptons.begin(),
        dressedLeptons.end(),
        [](const GenDressedLepton& a,
           const GenDressedLepton& b) {
            return a.pt > b.pt;
        }
    );

    return dressedLeptons;
}


// ============================================================
// Fiducial selection
//
// Matching the lepton part of Table 4:
//
//   direct W -> e/mu
//   dressed leptons
//   OS e mu
//   leading pT > 25
//   trailing pT > 20
//   |eta| < 2.5
//   mll > 85 GeV
//   no additional lepton with pT > 10 GeV
//
// Tau -> e/mu is explicitly rejected.
// ============================================================

bool FiducialGen(
    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,
    const RVecI& GenPart_genPartIdxMother
)
{
    const auto dressedLeptons =
        BuildDressedLeptonsGen(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );


    // --------------------------------------------------------
    // Keep only e/mu directly from W
    // --------------------------------------------------------

    std::vector<GenDressedLepton> selected;

    for (const auto& lep : dressedLeptons) {

        if (std::abs(lep.pdgId) != 11 &&
            std::abs(lep.pdgId) != 13)
            continue;

        // This rejects W -> tau -> e/mu
        if (!lep.directFromW)
            continue;

        selected.push_back(lep);
    }


    // Need at least two W-origin e/mu
    if (selected.size() < 2)
        return false;


    // --------------------------------------------------------
    // Additional leptons
    //
    // Preserve the logic of your current macro:
    // if a third selected e/mu has pT > 10 GeV, reject.
    // --------------------------------------------------------

    if (selected.size() >= 3 &&
        selected[2].pt > 10.)
        return false;


    // --------------------------------------------------------
    // Require opposite-sign e mu
    // --------------------------------------------------------

    const int pdgId0 = selected[0].pdgId;
    const int pdgId1 = selected[1].pdgId;

    if (pdgId0 * pdgId1 != -143)
        return false;


    // --------------------------------------------------------
    // pT and eta
    // --------------------------------------------------------

    if (selected[0].pt <= 25.)
        return false;

    if (selected[1].pt <= 20.)
        return false;

    if (std::abs(selected[0].eta) >= 2.5)
        return false;

    if (std::abs(selected[1].eta) >= 2.5)
        return false;


    // --------------------------------------------------------
    // Dilepton mass
    // --------------------------------------------------------

    ROOT::Math::PtEtaPhiMVector l0(
        selected[0].pt,
        selected[0].eta,
        selected[0].phi,
        selected[0].mass
    );

    ROOT::Math::PtEtaPhiMVector l1(
        selected[1].pt,
        selected[1].eta,
        selected[1].phi,
        selected[1].mass
    );

    if ((l0 + l1).M() <= 85.)
        return false;


    return true;
}

#endif