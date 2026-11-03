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
// Fiducial selection constants
// ============================================================

constexpr float DRESSING_R = 0.1;

constexpr float LEADING_LEPTON_PT  = 25.0;
constexpr float TRAILING_LEPTON_PT = 20.0;
constexpr float ADDITIONAL_LEP_PT  = 10.0;

constexpr float LEPTON_ETA_MAX = 2.5;

constexpr float MLL_MIN = 85.0;

constexpr float JET_PT_MIN   = 30.0;
constexpr float JET_ETA_MAX  = 4.7;
constexpr float JET_LEPTON_R = 0.4;


// ============================================================
// Lorentz vector
// ============================================================

using LorentzVectorGen =
    ROOT::Math::LorentzVector<
        ROOT::Math::PtEtaPhiM4D<float>
    >;


// ============================================================
// Generator-level lepton
// ============================================================

struct LeptonGen {

    float pt;
    float eta;
    float phi;
    float mass;

    int pdgId;

    bool fromTau;
    bool fromW;
};


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
    float dphi = phi1 - phi2;

    while (dphi > M_PI)
        dphi -= 2.0 * M_PI;

    while (dphi <= -M_PI)
        dphi += 2.0 * M_PI;

    const float deta = eta1 - eta2;

    return std::sqrt(
        deta * deta +
        dphi * dphi
    );
}


// ============================================================
// Build dressed lepton
//
// Starting from a stable GenPart e/mu:
//
//     dressed lepton
//          = lepton
//          + stable photons within DeltaR < 0.1
//
// Photon definition:
//
//     GenPart_pdgId == 22
//     GenPart_status == 1
//
// This is the generator-level dressed lepton used for the
// fiducial kinematics.
// ============================================================

inline LorentzVectorGen BuildDressedLepton(
    int leptonIdx,

    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecF &GenPart_mass,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status
)
{
    LorentzVectorGen dressed(
        GenPart_pt[leptonIdx],
        GenPart_eta[leptonIdx],
        GenPart_phi[leptonIdx],
        GenPart_mass[leptonIdx]
    );


    const std::size_t nGen =
        std::min({
            GenPart_pt.size(),
            GenPart_eta.size(),
            GenPart_phi.size(),
            GenPart_mass.size(),
            GenPart_pdgId.size(),
            GenPart_status.size()
        });


    // --------------------------------------------------------
    // Add stable photons within DeltaR < 0.1
    // --------------------------------------------------------

    for (std::size_t i = 0; i < nGen; ++i) {

        // Photon
        if (GenPart_pdgId[i] != 22)
            continue;

        // Stable photon
        if (GenPart_status[i] != 1)
            continue;


        const float dR =
            DeltaRGen(
                GenPart_eta[leptonIdx],
                GenPart_phi[leptonIdx],
                GenPart_eta[i],
                GenPart_phi[i]
            );


        if (dR < DRESSING_R) {

            LorentzVectorGen photon(
                GenPart_pt[i],
                GenPart_eta[i],
                GenPart_phi[i],
                GenPart_mass[i]
            );

            dressed += photon;
        }
    }


    return dressed;
}


// ============================================================
// Check whether a GenPart lepton has a tau ancestor
//
// Example:
//
//     W
//     |
//     tau
//     |
//     e
//
// The mother chain is followed starting from the GenPart
// lepton itself.
// ============================================================

inline bool IsFromTau(
    int genIdx,

    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    const std::size_t nGen =
        std::min(
            GenPart_pdgId.size(),
            GenPart_genPartIdxMother.size()
        );


    if (genIdx < 0 ||
        static_cast<std::size_t>(genIdx) >= nGen)
        return false;


    int currentIdx = genIdx;


    for (std::size_t step = 0; step < nGen; ++step) {

        const int motherIdx =
            GenPart_genPartIdxMother[currentIdx];


        if (motherIdx < 0)
            return false;


        if (static_cast<std::size_t>(motherIdx) >= nGen)
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
// Check whether a GenPart lepton has a W ancestor
//
// Checks any ancestor.
//
//     W -> e/mu
//         fromW = true
//
//     W -> tau -> e/mu
//         fromW = true
//
// This keeps W ancestry and tau ancestry independent.
// ============================================================

inline bool IsFromW(
    int genIdx,

    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    const std::size_t nGen =
        std::min(
            GenPart_pdgId.size(),
            GenPart_genPartIdxMother.size()
        );


    if (genIdx < 0 ||
        static_cast<std::size_t>(genIdx) >= nGen)
        return false;


    int currentIdx = genIdx;


    for (std::size_t step = 0; step < nGen; ++step) {

        const int motherIdx =
            GenPart_genPartIdxMother[currentIdx];


        if (motherIdx < 0)
            return false;


        if (static_cast<std::size_t>(motherIdx) >= nGen)
            return false;


        const int motherPID =
            GenPart_pdgId[motherIdx];


        if (std::abs(motherPID) == 24)
            return true;


        currentIdx = motherIdx;
    }


    return false;
}


// ============================================================
// Build generator-level leptons
//
// We now work directly with GenPart.
//
// For every stable e/mu:
//
//     1. determine W/tau ancestry
//     2. dress the lepton using BuildDressedLepton()
//     3. store the dressed kinematics
//
// No matching to GenDressedLepton is performed.
// ============================================================

inline std::vector<LeptonGen> GetSelectedLeptons(
    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecF &GenPart_mass,
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
            GenPart_mass.size(),
            GenPart_pdgId.size(),
            GenPart_status.size(),
            GenPart_genPartIdxMother.size()
        });


    std::vector<LeptonGen> leptons;


    for (std::size_t i = 0; i < nGen; ++i) {

        const int pdgId =
            GenPart_pdgId[i];


        // ----------------------------------------------------
        // Only electrons and muons
        // ----------------------------------------------------

        if (std::abs(pdgId) != 11 &&
            std::abs(pdgId) != 13)
            continue;


        // ----------------------------------------------------
        // Only stable e/mu
        // ----------------------------------------------------

        if (GenPart_status[i] != 1)
            continue;


        // ----------------------------------------------------
        // Determine ancestry directly from this GenPart index
        // ----------------------------------------------------

        const bool fromTau =
            IsFromTau(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );


        const bool fromW =
            IsFromW(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );


        // ----------------------------------------------------
        // Build dressed lepton
        // ----------------------------------------------------

        const LorentzVectorGen dressed =
            BuildDressedLepton(
                static_cast<int>(i),
                GenPart_pt,
                GenPart_eta,
                GenPart_phi,
                GenPart_mass,
                GenPart_pdgId,
                GenPart_status
            );


        // ----------------------------------------------------
        // Store dressed kinematics
        // ----------------------------------------------------

        leptons.push_back({
            static_cast<float>(dressed.Pt()),
            static_cast<float>(dressed.Eta()),
            static_cast<float>(dressed.Phi()),
            static_cast<float>(dressed.M()),
            pdgId,
            fromTau,
            fromW
        });
    }


    // Sort by dressed pT
    std::sort(
        leptons.begin(),
        leptons.end(),
        [](const LeptonGen &a,
           const LeptonGen &b)
        {
            return a.pt > b.pt;
        }
    );


    return leptons;
}


// ============================================================
// FINAL FUNCTION 1
//
// Fiducial selection
// ============================================================

inline bool FiducialGen(
    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecF &GenPart_mass,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother
)
{
    const auto leptons =
        GetSelectedLeptons(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );


    // --------------------------------------------------------
    // Current WW fiducial definition:
    //
    // W -> e/mu
    // NOT W -> tau -> e/mu
    // --------------------------------------------------------

    std::vector<LeptonGen> selected;


    for (const auto &lep : leptons) {

        if (!lep.fromW)
            continue;

        if (lep.fromTau)
            continue;

        selected.push_back(lep);
    }


    // Need at least two leptons
    if (selected.size() < 2)
        return false;


    // --------------------------------------------------------
    // Third-lepton veto
    // --------------------------------------------------------

    for (std::size_t i = 2; i < selected.size(); ++i) {

        if (selected[i].pt > ADDITIONAL_LEP_PT)
            return false;
    }


    // --------------------------------------------------------
    // Opposite-sign e-mu
    // --------------------------------------------------------

    if (
        selected[0].pdgId *
        selected[1].pdgId != -143
    )
        return false;


    // --------------------------------------------------------
    // pT
    // --------------------------------------------------------

    if (selected[0].pt <= LEADING_LEPTON_PT)
        return false;

    if (selected[1].pt <= TRAILING_LEPTON_PT)
        return false;


    // --------------------------------------------------------
    // eta
    // --------------------------------------------------------

    if (
        std::abs(selected[0].eta) >= LEPTON_ETA_MAX ||
        std::abs(selected[1].eta) >= LEPTON_ETA_MAX
    )
        return false;


    // --------------------------------------------------------
    // mll
    // --------------------------------------------------------

    const LorentzVectorGen lep0(
        selected[0].pt,
        selected[0].eta,
        selected[0].phi,
        selected[0].mass
    );

    const LorentzVectorGen lep1(
        selected[1].pt,
        selected[1].eta,
        selected[1].phi,
        selected[1].mass
    );


    const float mll =
        static_cast<float>((lep0 + lep1).M());


    if (mll <= MLL_MIN)
        return false;


    return true;
}


// ============================================================
// FINAL FUNCTION 2
//
// Number of fiducial GenJets
// ============================================================

inline int GetNGenJets(
    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecF &GenPart_mass,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother,

    const RVecF &GenJet_pt,
    const RVecF &GenJet_eta,
    const RVecF &GenJet_phi
)
{
    const auto leptons =
        GetSelectedLeptons(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother
        );


    // --------------------------------------------------------
    // Current fiducial lepton definition
    // --------------------------------------------------------

    std::vector<LeptonGen> selected;


    for (const auto &lep : leptons) {

        if (!lep.fromW)
            continue;

        if (lep.fromTau)
            continue;

        selected.push_back(lep);
    }


    if (selected.size() < 2)
        return -1;


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


        // ----------------------------------------------------
        // Jet-lepton overlap
        // ----------------------------------------------------

        bool overlaps = false;


        for (int j = 0; j < 2; ++j) {

            const float dR =
                DeltaRGen(
                    GenJet_eta[i],
                    GenJet_phi[i],
                    selected[j].eta,
                    selected[j].phi
                );


            if (dR <= JET_LEPTON_R) {
                overlaps = true;
                break;
            }
        }


        if (overlaps)
            continue;


        ++nFiducialJets;
    }


    return nFiducialJets;
}


#endif
