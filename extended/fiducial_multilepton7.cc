#ifndef FIDUCIALGEN_H
#define FIDUCIALGEN_H

#include <ROOT/RVec.hxx>
#include <Math/Vector4D.h>

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <iostream>
#include <iomanip>
#include <vector>

using ROOT::VecOps::RVec;

using RVecF = RVec<float>;
using RVecI = RVec<int>;


// ============================================================
// Constants
// ============================================================

constexpr float JET_LEPTON_R = 0.4f;

constexpr float DRESSING_R = 0.1f;

constexpr float LEADING_LEPTON_PT  = 25.0f;
constexpr float TRAILING_LEPTON_PT = 20.0f;
constexpr float ADDITIONAL_LEP_PT  = 10.0f;

constexpr float LEPTON_ETA_MAX = 2.5f;

constexpr float JET_PT_MIN  = 30.0f;
constexpr float JET_ETA_MAX = 4.7f;

constexpr float MLL_MIN = 85.0f;


// ============================================================
// Lorentz vector
// ============================================================

using LorentzVectorGen =
    ROOT::Math::LorentzVector<
        ROOT::Math::PtEtaPhiM4D<float>
    >;


// ============================================================
// Dressed lepton
// ============================================================

struct DressedLeptonGen
{
    float pt;
    float eta;
    float phi;
    float mass;

    int pdgId;

    // True if a W is found in the ancestry.
    bool FromW;

    // Index of the original stable GenPart lepton.
    int GenPartIdx;
};


// ============================================================
// DeltaPhi
// ============================================================

inline float DeltaPhiGen(
    float phi1,
    float phi2
)
{
    float dphi = phi1 - phi2;

    while (dphi > M_PI)
        dphi -= 2.0f * M_PI;

    while (dphi <= -M_PI)
        dphi += 2.0f * M_PI;

    return dphi;
}


// ============================================================
// DeltaR
// ============================================================

inline float DeltaRGen(
    float eta1,
    float phi1,
    float eta2,
    float phi2
)
{
    const float dEta =
        eta1 - eta2;

    const float dPhi =
        DeltaPhiGen(
            phi1,
            phi2
        );

    return std::sqrt(
        dEta * dEta +
        dPhi * dPhi
    );
}


// ============================================================
// Check if GenPart has a W anywhere in its ancestry
//
// Accepted:
//
//   W -> e
//   W -> mu
//   W -> tau -> e
//   W -> tau -> mu
//   W -> tau -> tau -> e
//   W -> tau -> tau -> mu
//
// ============================================================

inline bool IsFromWGen(
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

    if (
        static_cast<std::size_t>(idx) >= n
    )
    {
        return false;
    }

    int currentIdx = idx;

    // Walk through the complete ancestry.
    for (
        std::size_t step = 0;
        step < n;
        ++step
    )
    {
        if (currentIdx < 0)
            return false;

        if (
            static_cast<std::size_t>(currentIdx) >= n
        )
        {
            return false;
        }

        const int motherIdx =
            GenPart_genPartIdxMother[currentIdx];

        if (motherIdx < 0)
            return false;

        if (
            static_cast<std::size_t>(motherIdx) >= n
        )
        {
            return false;
        }

        const int motherPID =
            GenPart_pdgId[motherIdx];

        // Found a W.
        if (
            std::abs(motherPID) == 24
        )
        {
            return true;
        }

        currentIdx = motherIdx;
    }

    return false;
}


// ============================================================
// Direct W ancestry
//
// Accepted:
//
//   W -> e
//   W -> mu
//
// Rejected:
//
//   W -> tau -> e
//   W -> tau -> mu
//
// More generally, if a tau is encountered before reaching
// the W, the lepton is rejected.
// ============================================================

inline bool IsDirectFromWGen(
    int idx,

    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    if (
        idx < 0 ||
        idx >= static_cast<int>(
            GenPart_pdgId.size()
        )
    )
    {
        return false;
    }

    int mother =
        GenPart_genPartIdxMother[idx];

    while (
        mother >= 0 &&
        mother < static_cast<int>(
            GenPart_pdgId.size()
        )
    )
    {
        const int absPID =
            std::abs(
                GenPart_pdgId[mother]
            );

        // Reject any lepton whose ancestry
        // passes through a tau.
        if (
            absPID == 15
        )
        {
            return false;
        }

        // Accept if ancestry reaches a W
        // without passing through a tau.
        if (
            absPID == 24
        )
        {
            return true;
        }

        mother =
            GenPart_genPartIdxMother[mother];
    }

    return false;
}


// ============================================================
// Print ancestry
//
// Example:
//
//   13 -> 15 -> 24
//
// ============================================================

inline void PrintGenAncestry(
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
        return;

    if (
        static_cast<std::size_t>(idx) >= n
    )
    {
        return;
    }

    int currentIdx = idx;

    std::cout << "  ancestry: ";

    for (
        std::size_t step = 0;
        step < n;
        ++step
    )
    {
        if (currentIdx < 0)
            break;

        if (
            static_cast<std::size_t>(currentIdx) >= n
        )
        {
            break;
        }

        std::cout
            << GenPart_pdgId[currentIdx];

        const int motherIdx =
            GenPart_genPartIdxMother[currentIdx];

        if (motherIdx < 0)
            break;

        if (
            static_cast<std::size_t>(motherIdx) >= n
        )
        {
            break;
        }

        std::cout << " -> ";

        currentIdx = motherIdx;
    }

    std::cout << std::endl;
}


// ============================================================
// Build dressed lepton
//
// Start from a stable GenPart electron/muon and add all
// stable photons within DeltaR < 0.1.
//
// No GenDressedLepton collection is used.
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

    for (
        std::size_t i = 0;
        i < nGen;
        ++i
    )
    {
        // Photon
        if (
            GenPart_pdgId[i] != 22
        )
        {
            continue;
        }

        // Stable photon
        if (
            GenPart_status[i] != 1
        )
        {
            continue;
        }

        const float dR =
            DeltaRGen(
                GenPart_eta[leptonIdx],
                GenPart_phi[leptonIdx],

                GenPart_eta[i],
                GenPart_phi[i]
            );

        if (
            dR < DRESSING_R
        )
        {
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
// Build dressed e/mu directly from GenPart
//
// directWOnly = false:
//
//   Uses IsFromWGen()
//   W -> e/mu
//   W -> tau -> e/mu
//
// directWOnly = true:
//
//   Uses IsDirectFromWGen()
//   W -> e/mu
//   Rejects W -> tau -> e/mu
// ============================================================

inline std::vector<DressedLeptonGen>
BuildDressedLeptonsGen(
    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecF &GenPart_mass,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother,

    bool directWOnly = false,
    bool debug = false
)
{
    std::vector<DressedLeptonGen> leptons;

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

    for (
        std::size_t i = 0;
        i < nGen;
        ++i
    )
    {
        // ----------------------------------------------------
        // Only stable particles
        // ----------------------------------------------------

        if (
            GenPart_status[i] != 1
        )
        {
            continue;
        }

        const int pdgId =
            GenPart_pdgId[i];

        // ----------------------------------------------------
        // Only electrons and muons
        // ----------------------------------------------------

        if (
            std::abs(pdgId) != 11 &&
            std::abs(pdgId) != 13
        )
        {
            continue;
        }

        // ----------------------------------------------------
        // Sanity checks
        // ----------------------------------------------------

        if (
            !std::isfinite(GenPart_pt[i])
        )
        {
            continue;
        }

        if (
            !std::isfinite(GenPart_eta[i])
        )
        {
            continue;
        }

        if (
            !std::isfinite(GenPart_phi[i])
        )
        {
            continue;
        }

        if (
            !std::isfinite(GenPart_mass[i])
        )
        {
            continue;
        }

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
        // Determine W ancestry
        // ----------------------------------------------------

        bool fromW = false;

        if (directWOnly)
        {
            fromW =
                IsDirectFromWGen(
                    static_cast<int>(i),
                    GenPart_pdgId,
                    GenPart_genPartIdxMother
                );
        }
        else
        {
            fromW =
                IsFromWGen(
                    static_cast<int>(i),
                    GenPart_pdgId,
                    GenPart_genPartIdxMother
                );
        }

        // ----------------------------------------------------
        // Build object
        // ----------------------------------------------------

        DressedLeptonGen lep;

        lep.pt =
            dressed.Pt();

        lep.eta =
            dressed.Eta();

        lep.phi =
            dressed.Phi();

        lep.mass =
            dressed.M();

        lep.pdgId =
            pdgId;

        lep.FromW =
            fromW;

        lep.GenPartIdx =
            static_cast<int>(i);

        // ----------------------------------------------------
        // Debug
        // ----------------------------------------------------

        if (debug)
        {
            std::cout
                << "\n=========================================="
                << "\nGenPart lepton #" << i
                << "\n  pdgId = "
                << pdgId
                << "\n  bare pt = "
                << GenPart_pt[i]
                << "\n  dressed pt = "
                << lep.pt
                << "\n  dressed eta = "
                << lep.eta
                << "\n  dressed phi = "
                << lep.phi
                << "\n  dressed mass = "
                << lep.mass
                << "\n  directWOnly = "
                << directWOnly
                << "\n  FromW = "
                << fromW
                << std::endl;

            PrintGenAncestry(
                static_cast<int>(i),
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );
        }

        leptons.push_back(
            lep
        );
    }

    // --------------------------------------------------------
    // Sort by dressed pT
    // --------------------------------------------------------

    std::sort(
        leptons.begin(),
        leptons.end(),
        [](
            const DressedLeptonGen &a,
            const DressedLeptonGen &b
        )
        {
            return a.pt > b.pt;
        }
    );

    return leptons;
}


// ============================================================
// Fiducial generator-level selection
//
// directWOnly = false:
//
//   W -> e/mu
//   W -> tau -> e/mu
//
// directWOnly = true:
//
//   W -> e/mu only
//   tau-mediated leptons rejected
//
// Other requirements:
//
//   - at least two W-origin dressed e/mu
//   - leading pT > 25 GeV
//   - subleading pT > 20 GeV
//   - |eta| < 2.5
//   - OS e-mu
//   - mll > 85 GeV
//   - veto additional W-origin e/mu with pT > 10 GeV
//
// ============================================================

inline bool FiducialGen(
    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecF &GenPart_mass,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother,

    bool directWOnly = false,
    bool debug = false
)
{
    // --------------------------------------------------------
    // Build dressed e/mu directly from GenPart
    // --------------------------------------------------------

    const auto leptons =
        BuildDressedLeptonsGen(
            GenPart_pt,
            GenPart_eta,
            GenPart_phi,
            GenPart_mass,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother,

            directWOnly,
            debug
        );


    // --------------------------------------------------------
    // Select W-origin leptons
    // --------------------------------------------------------

    std::vector<DressedLeptonGen>
        selectedLeptons;

    for (
        const auto &lep : leptons
    )
    {
        if (
            !lep.FromW
        )
        {
            continue;
        }

        selectedLeptons.push_back(
            lep
        );
    }


    // --------------------------------------------------------
    // Need at least two
    // --------------------------------------------------------

    if (
        selectedLeptons.size() < 2
    )
    {
        return false;
    }


    // --------------------------------------------------------
    // Additional W-origin lepton veto
    //
    // Because leptons are sorted by dressed pT:
    //
    //   [0] leading
    //   [1] subleading
    //   [2+] additional
    //
    // --------------------------------------------------------

    for (
        std::size_t i = 2;
        i < selectedLeptons.size();
        ++i
    )
    {
        if (
            selectedLeptons[i].pt >
            ADDITIONAL_LEP_PT
        )
        {
            return false;
        }
    }


    // --------------------------------------------------------
    // Leading pT
    // --------------------------------------------------------

    if (
        selectedLeptons[0].pt <
        LEADING_LEPTON_PT
    )
    {
        return false;
    }


    // --------------------------------------------------------
    // Subleading pT
    // --------------------------------------------------------

    if (
        selectedLeptons[1].pt <
        TRAILING_LEPTON_PT
    )
    {
        return false;
    }


    // --------------------------------------------------------
    // Eta
    // --------------------------------------------------------

    if (
        std::abs(
            selectedLeptons[0].eta
        ) >= LEPTON_ETA_MAX
    )
    {
        return false;
    }

    if (
        std::abs(
            selectedLeptons[1].eta
        ) >= LEPTON_ETA_MAX
    )
    {
        return false;
    }


    // --------------------------------------------------------
    // Require e-mu final state
    // --------------------------------------------------------

    const int pdg1 =
        std::abs(
            selectedLeptons[0].pdgId
        );

    const int pdg2 =
        std::abs(
            selectedLeptons[1].pdgId
        );

    if (
        !(
            (pdg1 == 11 && pdg2 == 13) ||
            (pdg1 == 13 && pdg2 == 11)
        )
    )
    {
        return false;
    }


    // --------------------------------------------------------
    // Opposite sign
    //
    // OS e-mu:
    //
    //   pdgId1 * pdgId2 = -143
    // --------------------------------------------------------

    if (
        selectedLeptons[0].pdgId *
        selectedLeptons[1].pdgId
        != -143
    )
    {
        return false;
    }


    // --------------------------------------------------------
    // Dilepton invariant mass
    // --------------------------------------------------------

    const LorentzVectorGen p4_1(
        selectedLeptons[0].pt,
        selectedLeptons[0].eta,
        selectedLeptons[0].phi,
        selectedLeptons[0].mass
    );

    const LorentzVectorGen p4_2(
        selectedLeptons[1].pt,
        selectedLeptons[1].eta,
        selectedLeptons[1].phi,
        selectedLeptons[1].mass
    );

    const LorentzVectorGen dilepton =
        p4_1 + p4_2;

    if (
        dilepton.M() <= MLL_MIN
    )
    {
        return false;
    }


    // --------------------------------------------------------
    // Debug
    // --------------------------------------------------------

    if (debug)
    {
        std::cout
            << "\n=========================================="
            << "\nFIDUCIAL GEN EVENT ACCEPTED"
            << "\n=========================================="

            << "\nDirect W only = "
            << directWOnly

            << "\n\nLeading:"
            << "\n  pdgId = "
            << selectedLeptons[0].pdgId
            << "\n  pt = "
            << selectedLeptons[0].pt
            << "\n  eta = "
            << selectedLeptons[0].eta
            << "\n  FromW = "
            << selectedLeptons[0].FromW
            << "\n  GenPartIdx = "
            << selectedLeptons[0].GenPartIdx

            << "\n\nSubleading:"
            << "\n  pdgId = "
            << selectedLeptons[1].pdgId
            << "\n  pt = "
            << selectedLeptons[1].pt
            << "\n  eta = "
            << selectedLeptons[1].eta
            << "\n  FromW = "
            << selectedLeptons[1].FromW
            << "\n  GenPartIdx = "
            << selectedLeptons[1].GenPartIdx

            << "\n\nmll = "
            << dilepton.M()
            << std::endl;
    }

    return true;
}



// ============================================================
// Count clean generator-level jets
//
// Jet cleaning uses ALL prompt dressed e/mu.
//
// The dressed leptons are constructed directly from GenPart:
//
//   stable e/mu
//        +
//   stable photons with DeltaR < 0.1
//
// Requirements for cleaning leptons:
//
//   - status == 1
//   - |pdgId| == 11 or 13
//   - prompt
//   - dressed pT >= 10 GeV
//
// Jets:
//
//   pT >= 30 GeV
//   |eta| <= 4.7
//
// Remove a jet if:
//
//   DeltaR(jet, dressed lepton) < 0.4
//
// ============================================================

inline int GetNGenJets(
    const RVecF &GenPart_pt,
    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecF &GenPart_mass,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,

    const RVecI &LeptonGen_isPrompt,

    const RVecF &GenJet_pt,
    const RVecF &GenJet_eta,
    const RVecF &GenJet_phi
)
{
    // --------------------------------------------------------
    // Build list of ALL prompt dressed leptons used for
    // jet cleaning.
    // --------------------------------------------------------

    RVecF cleaning_eta;
    RVecF cleaning_phi;

    const std::size_t nGen =
        std::min(
            {
                GenPart_pt.size(),
                GenPart_eta.size(),
                GenPart_phi.size(),
                GenPart_mass.size(),
                GenPart_pdgId.size(),
                GenPart_status.size(),
                LeptonGen_isPrompt.size()
            }
        );

    for (
        std::size_t i = 0;
        i < nGen;
        ++i
    )
    {
        // ----------------------------------------------------
        // Only stable GenPart particles
        // ----------------------------------------------------

        if (
            GenPart_status[i] != 1
        )
        {
            continue;
        }

        // ----------------------------------------------------
        // Only electrons and muons
        // ----------------------------------------------------

        const int pdgId =
            GenPart_pdgId[i];

        if (
            std::abs(pdgId) != 11 &&
            std::abs(pdgId) != 13
        )
        {
            continue;
        }

        // ----------------------------------------------------
        // Must be prompt
        // ----------------------------------------------------

        if (
            !LeptonGen_isPrompt[i]
        )
        {
            continue;
        }

        // ----------------------------------------------------
        // Build dressed lepton
        //
        // This uses:
        //
        //   stable e/mu
        //   +
        //   stable photons within DeltaR < 0.1
        //
        // No GenDressedLepton collection is used.
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
        // Require dressed lepton pT >= 10 GeV
        // ----------------------------------------------------

        if (
            dressed.Pt() < 10.0
        )
        {
            continue;
        }

        // ----------------------------------------------------
        // Store dressed lepton direction for jet cleaning
        // ----------------------------------------------------

        cleaning_eta.push_back(
            dressed.Eta()
        );

        cleaning_phi.push_back(
            dressed.Phi()
        );
    }


    // --------------------------------------------------------
    // Count clean jets
    // --------------------------------------------------------

    int nCleanJets = 0;

    const std::size_t nJets =
        std::min(
            {
                GenJet_pt.size(),
                GenJet_eta.size(),
                GenJet_phi.size()
            }
        );

    for (
        std::size_t iJet = 0;
        iJet < nJets;
        ++iJet
    )
    {
        // ----------------------------------------------------
        // Jet pT
        // ----------------------------------------------------

        if (
            GenJet_pt[iJet] < JET_PT_MIN
        )
        {
            continue;
        }

        // ----------------------------------------------------
        // Jet eta
        // ----------------------------------------------------

        if (
            std::abs(
                GenJet_eta[iJet]
            ) > JET_ETA_MAX
        )
        {
            continue;
        }

        // ----------------------------------------------------
        // Remove jet if it overlaps ANY prompt dressed lepton
        // ----------------------------------------------------

        bool overlapsLepton = false;

        for (
            std::size_t iLep = 0;
            iLep < cleaning_eta.size();
            ++iLep
        )
        {
            const float dR =
                DeltaRGen(
                    GenJet_eta[iJet],
                    GenJet_phi[iJet],

                    cleaning_eta[iLep],
                    cleaning_phi[iLep]
                );

            if (
                dR < JET_LEPTON_R
            )
            {
                overlapsLepton = true;
                break;
            }
        }

        if (
            overlapsLepton
        )
        {
            continue;
        }

        ++nCleanJets;
    }

    return nCleanJets;
}

#endif // FIDUCIALGEN_H