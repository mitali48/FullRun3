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

#include "fastjet/ClusterSequence.hh"

using namespace ROOT;
using namespace ROOT::VecOps;


// ============================================================
// Constants
// ============================================================

constexpr float LEPTON_DRESSING_R  = 0.1;
constexpr float JET_R               = 0.4;
constexpr float JET_LEPTON_R        = 0.4;

constexpr float LEADING_LEPTON_PT   = 25.0;
constexpr float TRAILING_LEPTON_PT  = 20.0;
constexpr float ADDITIONAL_LEP_PT   = 10.0;

constexpr float LEPTON_ETA_MAX      = 2.5;
constexpr float JET_PT_MIN          = 30.0;
constexpr float JET_ETA_MAX         = 4.7;
constexpr float MLL_MIN             = 85.0;


// ============================================================
// Simple particle-level dressed lepton structure
// ============================================================

struct DressedLeptonGen {

    float pt;
    float eta;
    float phi;
    float mass;

    int pdgId;

    // Immediate mother from GenPart
    int MotherPID;

    // First ancestor with a different PDG ID
    int OriginalMotherPID;

    // True if a tau occurs anywhere in the ancestry
    bool FromTau;

    // True if the first distinct mother is a W
    bool DirectFromW;

    // Original GenPart index
    int genPartIdx;
};


// ============================================================
// Delta phi
// ============================================================

inline float DeltaPhiGen(
    float phi1,
    float phi2
)
{
    float dphi = phi1 - phi2;

    while (dphi > M_PI)
        dphi -= 2.0 * M_PI;

    while (dphi <= -M_PI)
        dphi += 2.0 * M_PI;

    return dphi;
}


// ============================================================
// Delta R
// ============================================================

inline float DeltaRGen(
    float eta1,
    float phi1,
    float eta2,
    float phi2
)
{
    const float deta = eta1 - eta2;
    const float dphi = DeltaPhiGen(phi1, phi2);

    return std::sqrt(
        deta * deta +
        dphi * dphi
    );
}


// ============================================================
// Find immediate mother PID
// ============================================================

int GetMotherPIDGen(
    int idx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    if (idx < 0 ||
        idx >= static_cast<int>(GenPart_pdgId.size()))
        return 0;

    if (idx >= static_cast<int>(
        GenPart_genPartIdxMother.size()))
        return 0;

    const int motherIdx =
        GenPart_genPartIdxMother[idx];

    if (motherIdx < 0 ||
        motherIdx >= static_cast<int>(GenPart_pdgId.size()))
        return 0;

    return GenPart_pdgId[motherIdx];
}


// ============================================================
// Find first ancestor with different PDG ID
//
// Example:
//
// e -> e -> e -> W
//
// returns W.
//
// e -> e -> tau -> W
//
// returns tau.
//
// This is the quantity used to identify direct W decay.
// ============================================================

int FindOriginalMotherPIDGen(
    int idx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    if (idx < 0 ||
        idx >= static_cast<int>(GenPart_pdgId.size()))
        return 0;

    const int leptonPID =
        GenPart_pdgId[idx];

    int current = idx;

    const int maxDepth =
        static_cast<int>(GenPart_pdgId.size());

    for (int depth = 0;
         depth < maxDepth;
         ++depth) {

        if (current < 0 ||
            current >= static_cast<int>(
                GenPart_genPartIdxMother.size()))
            return 0;

        const int motherIdx =
            GenPart_genPartIdxMother[current];

        if (motherIdx < 0 ||
            motherIdx >= static_cast<int>(
                GenPart_pdgId.size()))
            return 0;

        const int motherPID =
            GenPart_pdgId[motherIdx];

        // Ignore same-particle copies
        if (std::abs(motherPID) !=
            std::abs(leptonPID)) {

            return motherPID;
        }

        current = motherIdx;
    }

    return 0;
}


// ============================================================
// Check whether a tau occurs anywhere in ancestry
// ============================================================

bool HasTauAncestorGen(
    int idx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    if (idx < 0 ||
        idx >= static_cast<int>(GenPart_pdgId.size()))
        return false;

    int current = idx;

    const int maxDepth =
        static_cast<int>(GenPart_pdgId.size());

    for (int depth = 0;
         depth < maxDepth;
         ++depth) {

        if (current < 0 ||
            current >= static_cast<int>(
                GenPart_genPartIdxMother.size()))
            return false;

        const int motherIdx =
            GenPart_genPartIdxMother[current];

        if (motherIdx < 0 ||
            motherIdx >= static_cast<int>(
                GenPart_pdgId.size()))
            return false;

        const int motherPID =
            GenPart_pdgId[motherIdx];

        if (std::abs(motherPID) == 15)
            return true;

        current = motherIdx;
    }

    return false;
}


// ============================================================
// Check direct W decay
//
// W -> e
// W -> mu
//
// accepted
//
// W -> tau -> e
// W -> tau -> mu
//
// rejected
// ============================================================

bool IsDirectFromWGen(
    int idx,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_genPartIdxMother
)
{
    const int originalMother =
        FindOriginalMotherPIDGen(
            idx,
            GenPart_pdgId,
            GenPart_genPartIdxMother
        );

    return std::abs(originalMother) == 24;
}


// ============================================================
// Build dressed leptons
//
// Stable e/mu:
//     status == 1
//
// Photons:
//     status == 1
//
// Dressing:
//     photon DeltaR < 0.1
//
// Sorted by dressed pT.
// ============================================================

std::vector<DressedLeptonGen>
BuildDressedLeptonsGen(

    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,

    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,

    const RVecI& GenPart_genPartIdxMother
)
{
    std::vector<DressedLeptonGen>
        dressedLeptons;

    const std::size_t nGen =
        GenPart_pt.size();


    // --------------------------------------------------------
    // Loop over GenPart and select stable e/mu
    // --------------------------------------------------------

    for (std::size_t i = 0;
         i < nGen;
         ++i) {

        const int absPID =
            std::abs(GenPart_pdgId[i]);

        if (GenPart_status[i] != 1)
            continue;

        if (absPID != 11 &&
            absPID != 13)
            continue;


        // ----------------------------------------------------
        // Start with bare lepton
        // ----------------------------------------------------

        ROOT::Math::PtEtaPhiMVector p4(
            GenPart_pt[i],
            GenPart_eta[i],
            GenPart_phi[i],
            GenPart_mass[i]
        );


        // ----------------------------------------------------
        // Photon dressing
        // ----------------------------------------------------

        for (std::size_t j = 0;
             j < nGen;
             ++j) {

            if (GenPart_status[j] != 1)
                continue;

            if (GenPart_pdgId[j] != 22)
                continue;


            const float dR =
                DeltaRGen(
                    GenPart_eta[i],
                    GenPart_phi[i],
                    GenPart_eta[j],
                    GenPart_phi[j]
                );

            if (dR >= LEPTON_DRESSING_R)
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

        const int motherPID =
            GetMotherPIDGen(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );


        const int originalMotherPID =
            FindOriginalMotherPIDGen(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );


        const bool fromTau =
            HasTauAncestorGen(
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


        // ----------------------------------------------------
        // Store dressed lepton
        // ----------------------------------------------------

        DressedLeptonGen lep;

        lep.pt   = p4.Pt();
        lep.eta  = p4.Eta();
        lep.phi  = p4.Phi();
        lep.mass = p4.M();

        lep.pdgId =
            GenPart_pdgId[i];

        lep.MotherPID =
            motherPID;

        lep.OriginalMotherPID =
            originalMotherPID;

        lep.FromTau =
            fromTau;

        lep.DirectFromW =
            directFromW;

        lep.genPartIdx =
            static_cast<int>(i);


        dressedLeptons.push_back(lep);
    }


    // --------------------------------------------------------
    // Sort by pT
    // --------------------------------------------------------

    std::sort(
        dressedLeptons.begin(),
        dressedLeptons.end(),
        [](const DressedLeptonGen& a,
           const DressedLeptonGen& b) {

            return a.pt > b.pt;
        }
    );


    return dressedLeptons;
}


// ============================================================
// Output the requested dressed-lepton branches
//
// These are:
//
// DressedLeptonGen_pdgId
// DressedLeptonGen_pt
// DressedLeptonGen_OriginalMotherPID
// DressedLeptonGen_FromTau
// ============================================================

RVecI GetDressedLeptonGen_pdgId(
    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,
    const RVecI& GenPart_genPartIdxMother
)
{
    const auto leptons =
        BuildDressedLeptonsGen(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );

    RVecI result;

    for (const auto& lep : leptons)
        result.push_back(lep.pdgId);

    return result;
}


RVecF GetDressedLeptonGen_pt(
    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,
    const RVecI& GenPart_genPartIdxMother
)
{
    const auto leptons =
        BuildDressedLeptonsGen(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );

    RVecF result;

    for (const auto& lep : leptons)
        result.push_back(lep.pt);

    return result;
}


RVecI GetDressedLeptonGen_OriginalMotherPID(
    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,
    const RVecI& GenPart_genPartIdxMother
)
{
    const auto leptons =
        BuildDressedLeptonsGen(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );

    RVecI result;

    for (const auto& lep : leptons)
        result.push_back(
            lep.OriginalMotherPID
        );

    return result;
}


RVecB GetDressedLeptonGen_FromTau(
    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,
    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,
    const RVecI& GenPart_genPartIdxMother
)
{
    const auto leptons =
        BuildDressedLeptonsGen(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );

    RVecB result;

    for (const auto& lep : leptons)
        result.push_back(lep.FromTau);

    return result;
}


// ============================================================
// Build particle-level jets
//
// Stable particles: status == 1
//
// Exclude neutrinos:
//   nu_e, nu_mu, nu_tau
//
// All other stable particles are used.
//
// anti-kT R = 0.4
// ============================================================

std::vector<fastjet::PseudoJet>
BuildGenJets(

    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,

    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status
)
{
    std::vector<fastjet::PseudoJet>
        particles;

    const std::size_t nGen =
        GenPart_pt.size();


    // --------------------------------------------------------
    // Build input particle collection
    // --------------------------------------------------------

    for (std::size_t i = 0;
         i < nGen;
         ++i) {

        // Stable particles only
        if (GenPart_status[i] != 1)
            continue;


        const int absPID =
            std::abs(GenPart_pdgId[i]);


        // Exclude neutrinos
        if (absPID == 12 ||
            absPID == 14 ||
            absPID == 16)
            continue;


        ROOT::Math::PtEtaPhiMVector p4(
            GenPart_pt[i],
            GenPart_eta[i],
            GenPart_phi[i],
            GenPart_mass[i]
        );


        fastjet::PseudoJet particle(
            p4.Px(),
            p4.Py(),
            p4.Pz(),
            p4.E()
        );

        particles.push_back(particle);
    }


    // --------------------------------------------------------
    // anti-kT clustering
    // --------------------------------------------------------

    fastjet::JetDefinition jetDefinition(
        fastjet::antikt_algorithm,
        JET_R
    );

    fastjet::ClusterSequence clusterSequence(
        particles,
        jetDefinition
    );


    return clusterSequence.inclusive_jets(
        JET_PT_MIN
    );
}


// ============================================================
// Fiducial jet selection
//
// pT > 30 GeV
// |eta| < 2.5
// DeltaR(j, selected lepton) > 0.4
// ============================================================

std::vector<fastjet::PseudoJet>
GetFiducialGenJets(

    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,

    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,

    const RVecI& GenPart_genPartIdxMother,

    const DressedLeptonGen& lep0,
    const DressedLeptonGen& lep1
)
{
    const auto allJets =
        BuildGenJets(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status
        );


    std::vector<fastjet::PseudoJet>
        selectedJets;


    for (const auto& jet : allJets) {

        const float jetPt =
            jet.pt();

        const float jetEta =
            jet.eta();


        // ----------------------------------------------------
        // Jet pT
        // ----------------------------------------------------

        if (jetPt <= JET_PT_MIN)
            continue;


        // ----------------------------------------------------
        // Jet eta
        // ----------------------------------------------------

        if (std::abs(jetEta) >= JET_ETA_MAX)
            continue;


        // ----------------------------------------------------
        // Jet-lepton removal
        // ----------------------------------------------------

        const float dR0 =
            DeltaRGen(
                jetEta,
                jet.phi(),
                lep0.eta,
                lep0.phi
            );


        const float dR1 =
            DeltaRGen(
                jetEta,
                jet.phi(),
                lep1.eta,
                lep1.phi
            );


        if (dR0 < JET_LEPTON_R)
            continue;

        if (dR1 < JET_LEPTON_R)
            continue;


        selectedJets.push_back(jet);
    }


    // --------------------------------------------------------
    // Sort by pT
    // --------------------------------------------------------

    std::sort(
        selectedJets.begin(),
        selectedJets.end(),
        [](const fastjet::PseudoJet& a,
           const fastjet::PseudoJet& b) {

            return a.pt() > b.pt();
        }
    );


    return selectedJets;
}

// ============================================================
// Number of fiducial GenJets
// ============================================================

int GetNGenJets(

    const RVecF& GenPart_pt,
    const RVecF& GenPart_eta,
    const RVecF& GenPart_phi,
    const RVecF& GenPart_mass,

    const RVecI& GenPart_pdgId,
    const RVecI& GenPart_status,

    const RVecI& GenPart_genPartIdxMother
)
{
    // --------------------------------------------------------
    // Build dressed leptons
    // --------------------------------------------------------

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
    // Select leptons relevant for fiducial jet cleaning
    // --------------------------------------------------------

    std::vector<DressedLeptonGen> selectedLeptons;

    for (const auto& lep : dressedLeptons) {

        const int absPID = std::abs(lep.pdgId);

        if (absPID != 11 &&
            absPID != 13)
            continue;

        // Reject leptons from tau decays
        if (lep.FromTau)
            continue;

        // Require direct W decay
        if (!lep.DirectFromW)
            continue;

        selectedLeptons.push_back(lep);
    }


    // --------------------------------------------------------
    // Need at least two selected leptons
    // --------------------------------------------------------

    if (selectedLeptons.size() < 2)
        return -1;


    // --------------------------------------------------------
    // Build the fiducial GenJets
    // --------------------------------------------------------

    const auto fiducialJets =
        GetFiducialGenJets(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother,
            selectedLeptons[0],
            selectedLeptons[1]
        );


    // --------------------------------------------------------
    // Return number of fiducial jets
    // --------------------------------------------------------

    return static_cast<int>(fiducialJets.size());
}

// ============================================================
// Main fiducial selection
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
    // ========================================================
    // Build dressed leptons
    // ========================================================

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


    // ========================================================
    // Select prompt/direct-W e/mu
    // ========================================================

    std::vector<DressedLeptonGen>
        selectedLeptons;


    for (const auto& lep : dressedLeptons) {

        const int absPID =
            std::abs(lep.pdgId);

        if (absPID != 11 &&
            absPID != 13)
            continue;


        // Reject W -> tau -> e/mu
        if (lep.FromTau)
            continue;


        // Require direct W decay
        if (!lep.DirectFromW)
            continue;


        selectedLeptons.push_back(lep);
    }


    // Need at least two
    if (selectedLeptons.size() < 2)
        return false;


    // ========================================================
    // Additional prompt/direct-W lepton veto
    //
    // Same logic as your existing macro:
    // third selected lepton with pT > 10 -> reject
    // ========================================================

    if (selectedLeptons.size() >= 3 &&
        selectedLeptons[2].pt > ADDITIONAL_LEP_PT)
        return false;


    // ========================================================
    // Opposite-sign e mu
    // ========================================================

    const int pdgId0 =
        selectedLeptons[0].pdgId;

    const int pdgId1 =
        selectedLeptons[1].pdgId;


    if (pdgId0 * pdgId1 != -143)
        return false;


    // ========================================================
    // Leading lepton
    // ========================================================

    if (selectedLeptons[0].pt <=
        LEADING_LEPTON_PT)
        return false;


    // ========================================================
    // Trailing lepton
    // ========================================================

    if (selectedLeptons[1].pt <=
        TRAILING_LEPTON_PT)
        return false;


    // ========================================================
    // Eta
    // ========================================================

    if (std::abs(selectedLeptons[0].eta) >=
        LEPTON_ETA_MAX)
        return false;

    if (std::abs(selectedLeptons[1].eta) >=
        LEPTON_ETA_MAX)
        return false;


    // ========================================================
    // Dilepton invariant mass
    // ========================================================

    ROOT::Math::PtEtaPhiMVector l0(
        selectedLeptons[0].pt,
        selectedLeptons[0].eta,
        selectedLeptons[0].phi,
        selectedLeptons[0].mass
    );

    ROOT::Math::PtEtaPhiMVector l1(
        selectedLeptons[1].pt,
        selectedLeptons[1].eta,
        selectedLeptons[1].phi,
        selectedLeptons[1].mass
    );


    if ((l0 + l1).M() <= MLL_MIN)
        return false;


    // ========================================================
    // Build fiducial GenJets
    // ========================================================

    const auto fiducialJets =
        GetFiducialGenJets(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother,
            selectedLeptons[0],
            selectedLeptons[1]
        );


    // ========================================================
    // The event is fiducial.
    //
    // No explicit requirement on number of jets.
    // Njets is used later to categorize the event.
    // ========================================================

    return true;
}


#endif