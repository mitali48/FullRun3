#ifndef FIDUCIALGEN
#define FIDUCIALGEN

#include <vector>
#include <algorithm>
#include <cmath>
#include <cstddef>

#include "ROOT/RVec.hxx"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

using namespace ROOT;
using namespace ROOT::VecOps;


// ============================================================
// Constants
// ============================================================

constexpr float JET_LEPTON_R = 0.4;

constexpr float LEADING_LEPTON_PT  = 25.0;
constexpr float TRAILING_LEPTON_PT = 20.0;
constexpr float ADDITIONAL_LEP_PT  = 10.0;

constexpr float LEPTON_ETA_MAX = 2.5;

constexpr float JET_PT_MIN  = 30.0;
constexpr float JET_ETA_MAX = 4.7;

constexpr float MLL_MIN = 85.0;


// ============================================================
// Lorentz vector
// ============================================================

using LorentzVectorGen =
    ROOT::Math::LorentzVector<
        ROOT::Math::PtEtaPhiM4D<float>
    >;


// ============================================================
// Structure for NanoAOD dressed leptons
// ============================================================

struct DressedLeptonGen {

    float pt;
    float eta;
    float phi;
    float mass;

    int pdgId;

    bool FromTau;
    bool DirectFromW;
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
// Get mother PID
//
// Still uses GenPart because NanoAOD GenDressedLepton does
// not store the W ancestry directly.
// ============================================================

inline int GetMotherPIDGen(
    int idx,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    if (idx < 0)
        return 0;

    const std::size_t n =
        std::min(
            GenPart_pdgId.size(),
            GenPart_genPartIdxMother.size()
        );

    if (static_cast<std::size_t>(idx) >= n)
        return 0;

    const int motherIdx =
        GenPart_genPartIdxMother[idx];

    if (motherIdx < 0)
        return 0;

    if (static_cast<std::size_t>(motherIdx) >= n)
        return 0;

    return GenPart_pdgId[motherIdx];
}


// ============================================================
// Find original mother
//
// Skip copies of the same particle.
// ============================================================

inline int FindOriginalMotherPIDGen(
    int idx,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    const std::size_t n =
        std::min(
            GenPart_pdgId.size(),
            GenPart_genPartIdxMother.size()
        );

    if (idx < 0)
        return 0;

    if (static_cast<std::size_t>(idx) >= n)
        return 0;

    const int originalPID =
        GenPart_pdgId[idx];

    int currentIdx = idx;

    for (std::size_t step = 0; step < n; ++step) {

        if (currentIdx < 0)
            return 0;

        if (static_cast<std::size_t>(currentIdx) >= n)
            return 0;

        const int motherIdx =
            GenPart_genPartIdxMother[currentIdx];

        if (motherIdx < 0)
            return 0;

        if (static_cast<std::size_t>(motherIdx) >= n)
            return 0;

        const int motherPID =
            GenPart_pdgId[motherIdx];

        if (std::abs(motherPID) != std::abs(originalPID))
            return motherPID;

        currentIdx = motherIdx;
    }

    return 0;
}


// ============================================================
// Check tau ancestry
//
// This is kept only if we want to cross-check the NanoAOD
// GenDressedLepton_hasTauAnc information.
//
// Normally use GenDressedLepton_hasTauAnc directly.
// ============================================================

inline bool HasTauAncestorGen(
    int idx,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    const std::size_t n =
        std::min(
            GenPart_pdgId.size(),
            GenPart_genPartIdxMother.size()
        );

    if (idx < 0)
        return false;

    if (static_cast<std::size_t>(idx) >= n)
        return false;

    int currentIdx = idx;

    for (std::size_t step = 0; step < n; ++step) {

        if (currentIdx < 0)
            return false;

        if (static_cast<std::size_t>(currentIdx) >= n)
            return false;

        const int motherIdx =
            GenPart_genPartIdxMother[currentIdx];

        if (motherIdx < 0)
            return false;

        if (static_cast<std::size_t>(motherIdx) >= n)
            return false;

        const int motherPID =
            GenPart_pdgId[motherIdx];

        if (std::abs(motherPID) == 15)
            return true;

        currentIdx = motherIdx;
    }

    return false;
}


// ============================================================
// Check whether a GenPart lepton comes directly from W
//
// Used only for the "DirectFromW" requirement.
// ============================================================

inline bool IsDirectFromWGen(
    int idx,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    const int originalPID =
        (idx >= 0 &&
         static_cast<std::size_t>(idx) < GenPart_pdgId.size())
        ? GenPart_pdgId[idx]
        : 0;

    if (originalPID == 0)
        return false;

    const int motherPID =
        FindOriginalMotherPIDGen(
            idx,
            GenPart_pdgId,
            GenPart_genPartIdxMother
        );

    return std::abs(motherPID) == 24;
}


// ============================================================
// Find whether a NanoAOD GenDressedLepton corresponds to a
// direct-W GenPart lepton.
//
// IMPORTANT:
// GenDressedLepton does not contain genPartIdx.
//
// We therefore match the dressed lepton to a stable GenPart
// e/mu using DeltaR and pT.
//
// This is only needed if DirectFromW is required.
// ============================================================

inline bool IsNanoDressedLeptonDirectFromW(
    float lep_pt,
    float lep_eta,
    float lep_phi,
    int lep_pdgId,

    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother
)
{
    const std::size_t nGen =
        std::min({
            GenPart_pt.size(),
            GenPart_eta.size(),
            GenPart_phi.size(),
            GenPart_pdgId.size(),
            GenPart_status.size(),
            GenPart_genPartIdxMother.size()
        });

    float bestDR = 999.0;
    int bestIdx = -1;

    for (std::size_t i = 0; i < nGen; ++i) {

        if (GenPart_status[i] != 1)
            continue;

        if (GenPart_pdgId[i] != lep_pdgId)
            continue;

        const float dR =
            DeltaRGen(
                lep_eta,
                lep_phi,
                GenPart_eta[i],
                GenPart_phi[i]
            );

        if (dR < bestDR) {
            bestDR = dR;
            bestIdx = static_cast<int>(i);
        }
    }

    if (bestIdx < 0)
        return false;

    /*
     * The dressed lepton should be very close to its
     * underlying bare e/mu.
     */
    if (bestDR > 0.1)
        return false;

    return IsDirectFromWGen(
        bestIdx,
        GenPart_pdgId,
        GenPart_genPartIdxMother
    );
}


// ============================================================
// Build leptons directly from NanoAOD GenDressedLepton
//
// No photon dressing.
// No FastJet.
// No manual construction of the dressed lepton.
// ============================================================

inline std::vector<DressedLeptonGen> BuildDressedLeptonsGen(
    const RVecF &GenDressedLepton_pt,
    const RVecF &GenDressedLepton_eta,
    const RVecF &GenDressedLepton_phi,
    const RVecF &GenDressedLepton_mass,
    const RVecI &GenDressedLepton_pdgId,
    const RVecB &GenDressedLepton_hasTauAnc,

    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother
)
{
    const std::size_t nLeptons =
        std::min({
            GenDressedLepton_pt.size(),
            GenDressedLepton_eta.size(),
            GenDressedLepton_phi.size(),
            GenDressedLepton_mass.size(),
            GenDressedLepton_pdgId.size(),
            GenDressedLepton_hasTauAnc.size()
        });

    std::vector<DressedLeptonGen> leptons;

    for (std::size_t i = 0; i < nLeptons; ++i) {

        const int pdgId =
            GenDressedLepton_pdgId[i];

        // Only electrons and muons
        if (std::abs(pdgId) != 11 &&
            std::abs(pdgId) != 13)
            continue;

        // Protect against invalid values
        if (!std::isfinite(GenDressedLepton_pt[i]) ||
            !std::isfinite(GenDressedLepton_eta[i]) ||
            !std::isfinite(GenDressedLepton_phi[i]) ||
            !std::isfinite(GenDressedLepton_mass[i]))
            continue;

        DressedLeptonGen dressed;

        dressed.pt =
            GenDressedLepton_pt[i];

        dressed.eta =
            GenDressedLepton_eta[i];

        dressed.phi =
            GenDressedLepton_phi[i];

        dressed.mass =
            GenDressedLepton_mass[i];

        dressed.pdgId =
            pdgId;

        dressed.FromTau =
            GenDressedLepton_hasTauAnc[i];

        /*
         * DirectFromW is not stored in NanoAOD.
         * Determine it using the underlying GenPart.
         */
        dressed.DirectFromW =
            IsNanoDressedLeptonDirectFromW(
                dressed.pt,
                dressed.eta,
                dressed.phi,
                dressed.pdgId,

                GenPart_pt,
                GenPart_eta,
                GenPart_phi,
                GenPart_pdgId,
                GenPart_status,
                GenPart_genPartIdxMother
            );

        leptons.push_back(dressed);
    }

    // Sort by pT
    std::sort(
        leptons.begin(),
        leptons.end(),
        [](const DressedLeptonGen &a,
           const DressedLeptonGen &b)
        {
            return a.pt > b.pt;
        }
    );

    return leptons;
}


// ============================================================
// Count fiducial GenJets
//
// Uses NanoAOD GenJet collection.
// NO FastJet.
// ============================================================

inline int CountFiducialGenJets(
    const RVecF &GenJet_pt,
    const RVecF &GenJet_eta,
    const RVecF &GenJet_phi,

    const RVecF &lepton_eta,
    const RVecF &lepton_phi
)
{
    const std::size_t nJets =
        std::min({
            GenJet_pt.size(),
            GenJet_eta.size(),
            GenJet_phi.size()
        });

    int nFiducialJets = 0;

    for (std::size_t i = 0; i < nJets; ++i) {

        if (!std::isfinite(GenJet_pt[i]) ||
            !std::isfinite(GenJet_eta[i]) ||
            !std::isfinite(GenJet_phi[i]))
            continue;

        // Jet pT
        if (GenJet_pt[i] <= JET_PT_MIN)
            continue;

        // Jet eta
        if (std::abs(GenJet_eta[i]) >= JET_ETA_MAX)
            continue;

        // Lepton overlap removal
        bool overlapsLepton = false;

        const std::size_t nLeptons =
            std::min(
                lepton_eta.size(),
                lepton_phi.size()
            );

        for (std::size_t j = 0; j < nLeptons; ++j) {

            const float dR =
                DeltaRGen(
                    GenJet_eta[i],
                    GenJet_phi[i],
                    lepton_eta[j],
                    lepton_phi[j]
                );

            if (dR <= JET_LEPTON_R) {
                overlapsLepton = true;
                break;
            }
        }

        if (overlapsLepton)
            continue;

        ++nFiducialJets;
    }

    return nFiducialJets;
}


// ============================================================
// Get number of fiducial GenJets
//
// Uses:
//   GenDressedLepton_*
//   GenJet_*
//
// No FastJet.
// ============================================================

inline int GetNGenJets(
    const RVecF &GenDressedLepton_pt,
    const RVecF &GenDressedLepton_eta,
    const RVecF &GenDressedLepton_phi,
    const RVecF &GenDressedLepton_mass,
    const RVecI &GenDressedLepton_pdgId,
    const RVecB &GenDressedLepton_hasTauAnc,

    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother,

    const RVecF &GenJet_pt,
    const RVecF &GenJet_eta,
    const RVecF &GenJet_phi
)
{
    const auto leptons =
        BuildDressedLeptonsGen(
            GenDressedLepton_pt,
            GenDressedLepton_eta,
            GenDressedLepton_phi,
            GenDressedLepton_mass,
            GenDressedLepton_pdgId,
            GenDressedLepton_hasTauAnc,

            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );

    std::vector<DressedLeptonGen> selectedLeptons;

    for (const auto &lep : leptons) {

        if (std::abs(lep.pdgId) != 11 &&
            std::abs(lep.pdgId) != 13)
            continue;

        if (lep.FromTau)
            continue;

        if (!lep.DirectFromW)
            continue;

        selectedLeptons.push_back(lep);
    }

    // Need at least two leptons
    if (selectedLeptons.size() < 2)
        return -1;

    RVecF lepton_eta;
    RVecF lepton_phi;

    lepton_eta.push_back(selectedLeptons[0].eta);
    lepton_eta.push_back(selectedLeptons[1].eta);

    lepton_phi.push_back(selectedLeptons[0].phi);
    lepton_phi.push_back(selectedLeptons[1].phi);

    return CountFiducialGenJets(
        GenJet_pt,
        GenJet_eta,
        GenJet_phi,
        lepton_eta,
        lepton_phi
    );
}


// ============================================================
// Fiducial Gen selection
//
// Uses NanoAOD GenDressedLepton.
// No FastJet.
// ============================================================

inline bool FiducialGen(
    const RVecF &GenDressedLepton_pt,
    const RVecF &GenDressedLepton_eta,
    const RVecF &GenDressedLepton_phi,
    const RVecF &GenDressedLepton_mass,
    const RVecI &GenDressedLepton_pdgId,
    const RVecB &GenDressedLepton_hasTauAnc,

    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother
)
{
    const auto leptons =
        BuildDressedLeptonsGen(
            GenDressedLepton_pt,
            GenDressedLepton_eta,
            GenDressedLepton_phi,
            GenDressedLepton_mass,
            GenDressedLepton_pdgId,
            GenDressedLepton_hasTauAnc,

            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );

    // --------------------------------------------------------
    // Select direct-W, non-tau e/mu
    // --------------------------------------------------------

    std::vector<DressedLeptonGen> selectedLeptons;

    for (const auto &lep : leptons) {

        if (std::abs(lep.pdgId) != 11 &&
            std::abs(lep.pdgId) != 13)
            continue;

        if (lep.FromTau)
            continue;

        if (!lep.DirectFromW)
            continue;

        selectedLeptons.push_back(lep);
    }

    // Need at least two
    if (selectedLeptons.size() < 2)
        return false;

    // --------------------------------------------------------
    // Third-lepton veto
    // --------------------------------------------------------

    for (std::size_t i = 2;
         i < selectedLeptons.size();
         ++i)
    {
        if (selectedLeptons[i].pt > ADDITIONAL_LEP_PT)
            return false;
    }

    // --------------------------------------------------------
    // Opposite-sign e-mu
    // --------------------------------------------------------

    if (
        selectedLeptons[0].pdgId *
        selectedLeptons[1].pdgId
        != -143
    )
        return false;

    // --------------------------------------------------------
    // pT
    // --------------------------------------------------------

    if (selectedLeptons[0].pt <= LEADING_LEPTON_PT)
        return false;

    if (selectedLeptons[1].pt <= TRAILING_LEPTON_PT)
        return false;

    // --------------------------------------------------------
    // eta
    // --------------------------------------------------------

    if (
        std::abs(selectedLeptons[0].eta) >= LEPTON_ETA_MAX ||
        std::abs(selectedLeptons[1].eta) >= LEPTON_ETA_MAX
    )
        return false;

    // --------------------------------------------------------
    // mll
    // --------------------------------------------------------

    LorentzVectorGen lep0(
        selectedLeptons[0].pt,
        selectedLeptons[0].eta,
        selectedLeptons[0].phi,
        selectedLeptons[0].mass
    );

    LorentzVectorGen lep1(
        selectedLeptons[1].pt,
        selectedLeptons[1].eta,
        selectedLeptons[1].phi,
        selectedLeptons[1].mass
    );

    const float mll =
        static_cast<float>(
            (lep0 + lep1).M()
        );

    if (mll <= MLL_MIN)
        return false;

    return true;
}

#endif
