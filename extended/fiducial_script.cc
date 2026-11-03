
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

constexpr float LEADING_LEPTON_PT  = 25.0f;
constexpr float TRAILING_LEPTON_PT = 20.0f;
constexpr float ADDITIONAL_LEP_PT  = 10.0f;

constexpr float LEPTON_ETA_MAX = 2.5f;

constexpr float JET_PT_MIN  = 30.0f;
constexpr float JET_ETA_MAX = 4.7f;

constexpr float MLL_MIN = 85.0f;

constexpr float GEN_MATCH_DR = 0.1f;


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

    // True if a W is found anywhere in the ancestry.
    //
    // Examples:
    //
    //   W -> e
    //   W -> mu
    //   W -> tau -> e
    //   W -> tau -> mu
    //
    bool FromW;

    // Matching information
    int GenPartIdx;
    float GenPartDR;
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
// Check if GenPart has a W in its ancestry
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
// The W does NOT need to be the direct mother.
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

inline bool IsDirectFromWGen(
    int idx,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_genPartIdxMother
)
{
    if (idx < 0 || idx >= (int)GenPart_pdgId.size())
        return false;

    int mother = GenPart_genPartIdxMother[idx];

    while (mother >= 0 && mother < (int)GenPart_pdgId.size()) {

        int absPID = std::abs(GenPart_pdgId[mother]);

        // Reject any lepton coming from a tau
        if (absPID == 15)
            return false;

        // Accept if the ancestry reaches a W without passing through a tau
        if (absPID == 24)
            return true;

        mother = GenPart_genPartIdxMother[mother];
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
// Match GenDressedLepton to stable GenPart
//
// We look for the closest stable GenPart:
//
//   status == 1
//
// with the same PDG ID.
//
// Require:
//
//   DeltaR < 0.1
//
// ============================================================

inline int MatchDressedLeptonToGenPart(
    float lep_eta,
    float lep_phi,
    int lep_pdgId,

    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status
)
{
    const std::size_t nGen =
        std::min(
            {
                GenPart_eta.size(),
                GenPart_phi.size(),
                GenPart_pdgId.size(),
                GenPart_status.size()
            }
        );

    int bestIdx = -1;

    float bestDR =
        GEN_MATCH_DR;

    for (
        std::size_t i = 0;
        i < nGen;
        ++i
    )
    {
        // Stable GenPart only.
        if (
            GenPart_status[i] != 1
        )
        {
            continue;
        }

        // Same particle including charge.
        if (
            GenPart_pdgId[i] != lep_pdgId
        )
        {
            continue;
        }

        const float dR =
            DeltaRGen(
                lep_eta,
                lep_phi,
                GenPart_eta[i],
                GenPart_phi[i]
            );

        if (dR < bestDR)
        {
            bestDR = dR;

            bestIdx =
                static_cast<int>(i);
        }
    }

    return bestIdx;
}


// ============================================================
// Build dressed e/mu
//
// IMPORTANT:
//
// GenDressedLepton_hasTauAnc is deliberately NOT used.
//
// We determine W ancestry directly from:
//
//   GenPart_pdgId
//   GenPart_genPartIdxMother
//
// Therefore:
//
//   W -> mu
//   W -> tau -> mu
//   W -> tau -> e
//
// are all correctly recognized as FromW.
// ============================================================

inline std::vector<DressedLeptonGen>
BuildDressedLeptonsGen(
    const RVecF &GenDressedLepton_pt,
    const RVecF &GenDressedLepton_eta,
    const RVecF &GenDressedLepton_phi,
    const RVecF &GenDressedLepton_mass,
    const RVecI &GenDressedLepton_pdgId,

    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother,

    bool debug = false
)
{
    std::vector<DressedLeptonGen> leptons;

    const std::size_t nLeptons =
        std::min(
            {
                GenDressedLepton_pt.size(),
                GenDressedLepton_eta.size(),
                GenDressedLepton_phi.size(),
                GenDressedLepton_mass.size(),
                GenDressedLepton_pdgId.size()
            }
        );

    for (
        std::size_t i = 0;
        i < nLeptons;
        ++i
    )
    {
        const int pdgId =
            GenDressedLepton_pdgId[i];

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

        const float pt =
            GenDressedLepton_pt[i];

        const float eta =
            GenDressedLepton_eta[i];

        const float phi =
            GenDressedLepton_phi[i];

        const float mass =
            GenDressedLepton_mass[i];

        // ----------------------------------------------------
        // Sanity checks
        // ----------------------------------------------------

        if (!std::isfinite(pt))
            continue;

        if (!std::isfinite(eta))
            continue;

        if (!std::isfinite(phi))
            continue;

        if (!std::isfinite(mass))
            continue;

        // ----------------------------------------------------
        // Match to stable GenPart
        // ----------------------------------------------------

        const int genIdx =
            MatchDressedLeptonToGenPart(
                eta,
                phi,
                pdgId,

                GenPart_eta,
                GenPart_phi,
                GenPart_pdgId,
                GenPart_status
            );

        if (genIdx < 0)
            continue;

        const float genDR =
            DeltaRGen(
                eta,
                phi,
                GenPart_eta[genIdx],
                GenPart_phi[genIdx]
            );

        // ----------------------------------------------------
        // Determine W ancestry
        // ----------------------------------------------------

        const bool fromW =
            IsFromWGen(
                genIdx,
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );

/*
	const bool fromW =
    	    IsDirectFromWGen(
       	 	genIdx,
        	GenPart_pdgId,
        	GenPart_genPartIdxMother
    	     );	
*/	    
        // ----------------------------------------------------
        // Debug
        // ----------------------------------------------------

        if (debug)
        {
            std::cout
                << "\n=========================================="
                << "\nGenDressedLepton #" << i
                << "\n  pdgId = " << pdgId
                << "\n  pt    = " << pt
                << "\n  eta   = " << eta
                << "\n  phi   = " << phi
                << "\n  GenPartIdx = " << genIdx
                << "\n  GenPartDR  = "
                << std::setprecision(6)
                << genDR
                << "\n  FromW = "
                << fromW
                << std::endl;

            PrintGenAncestry(
                genIdx,
                GenPart_pdgId,
                GenPart_genPartIdxMother
            );
        }

        // ----------------------------------------------------
        // Build object
        // ----------------------------------------------------

        DressedLeptonGen lep;

        lep.pt =
            pt;

        lep.eta =
            eta;

        lep.phi =
            phi;

        lep.mass =
            mass;

        lep.pdgId =
            pdgId;

        lep.FromW =
            fromW;

        lep.GenPartIdx =
            genIdx;

        lep.GenPartDR =
            genDR;

        leptons.push_back(
            lep
        );
    }

    // --------------------------------------------------------
    // Sort by pT
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
// REQUIREMENTS:
//
//   - at least two W-origin dressed e/mu
//   - W can be direct or through tau
//
//     W -> e
//     W -> mu
//     W -> tau -> e
//     W -> tau -> mu
//
//   - leading pT > 25 GeV
//   - subleading pT > 20 GeV
//   - |eta| < 2.5
//   - exactly OS e-mu among the selected W-origin leptons
//   - mll > 85 GeV
//   - veto additional W-origin e/mu with pT > 10 GeV
//
// ============================================================

inline bool FiducialGen(
    const RVecF &GenDressedLepton_pt,
    const RVecF &GenDressedLepton_eta,
    const RVecF &GenDressedLepton_phi,
    const RVecF &GenDressedLepton_mass,
    const RVecI &GenDressedLepton_pdgId,

    const RVecF &GenPart_eta,
    const RVecF &GenPart_phi,
    const RVecI &GenPart_pdgId,
    const RVecI &GenPart_status,
    const RVecI &GenPart_genPartIdxMother,

    bool debug = false
)
{
    // --------------------------------------------------------
    // Build dressed e/mu
    // --------------------------------------------------------

    const auto leptons =
        BuildDressedLeptonsGen(
            GenDressedLepton_pt,
            GenDressedLepton_eta,
            GenDressedLepton_phi,
            GenDressedLepton_mass,
            GenDressedLepton_pdgId,

            GenPart_eta,
            GenPart_phi,
            GenPart_pdgId,
            GenPart_status,
            GenPart_genPartIdxMother,

            debug
        );


    // --------------------------------------------------------
    // Select W-origin leptons
    //
    // DO NOT veto tau ancestry.
    //
    // Therefore:
    //
    //   W -> tau -> e
    //   W -> tau -> mu
    //
    // are accepted.
    // --------------------------------------------------------

    std::vector<DressedLeptonGen>
        selectedLeptons;

    for (const auto &lep : leptons)
    {
        if (!lep.FromW)
            continue;

        selectedLeptons.push_back(
            lep
        );
    }


    // --------------------------------------------------------
    // Need at least two
    // --------------------------------------------------------

    if (selectedLeptons.size() < 2)
        return false;


    // --------------------------------------------------------
    // Additional W-origin lepton veto
    //
    // Because leptons are sorted by pT:
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
        std::abs(selectedLeptons[0].eta) >=
        LEPTON_ETA_MAX
    )
    {
        return false;
    }

    if (
        std::abs(selectedLeptons[1].eta) >=
        LEPTON_ETA_MAX
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
    // For e/mu:
    //
    //   e-  = +11
    //   e+  = -11
    //   mu- = +13
    //   mu+ = -13
    //
    // OS e-mu:
    //
    //   pdg1 * pdg2 = -143
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
            << "\nLeading:"
            << "\n  pdgId = "
            << selectedLeptons[0].pdgId
            << "\n  pt    = "
            << selectedLeptons[0].pt
            << "\n  eta   = "
            << selectedLeptons[0].eta
            << "\n  FromW = "
            << selectedLeptons[0].FromW
            << "\n  GenPartIdx = "
            << selectedLeptons[0].GenPartIdx
            << "\n  GenPartDR = "
            << selectedLeptons[0].GenPartDR
            << std::endl;

        std::cout
            << "\nSubleading:"
            << "\n  pdgId = "
            << selectedLeptons[1].pdgId
            << "\n  pt    = "
            << selectedLeptons[1].pt
            << "\n  eta   = "
            << selectedLeptons[1].eta
            << "\n  FromW = "
            << selectedLeptons[1].FromW
            << "\n  GenPartIdx = "
            << selectedLeptons[1].GenPartIdx
            << "\n  GenPartDR = "
            << selectedLeptons[1].GenPartDR
            << std::endl;

        std::cout
            << "\nmll = "
            << dilepton.M()
            << std::endl;
    }

    return true;
}


// ============================================================
// Count clean generator-level jets
//
// IMPORTANT:
//
// Jet cleaning is independent of the fiducial selection.
//
// We use ALL prompt dressed leptons:
//
//   pT >= 10 GeV
//   prompt == true
//
// and remove:
//
//   DeltaR(jet, lepton) < 0.4
//
// Jets:
//
//   pT >= 30 GeV
//   |eta| <= 4.7
//
// ============================================================

inline int GetNGenJets(
    const RVecF &GenDressedLepton_pt,
    const RVecF &GenDressedLepton_eta,
    const RVecF &GenDressedLepton_phi,


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

    const std::size_t nLeptons =
        std::min(
            {
                GenDressedLepton_pt.size(),
                GenDressedLepton_eta.size(),
                GenDressedLepton_phi.size(),
                // LeptonGen_isPrompt.size()
            }
        );

    for (
        std::size_t i = 0;
        i < nLeptons;
        ++i
    )
    {
        // Prompt lepton pT >= 10 GeV
        if (
            GenDressedLepton_pt[i] < 10.0
        )
        {
            continue;
        }

        // // Must be prompt
        // if (
        //     !LeptonGen_isPrompt[i]
        // )
        // {
        //     continue;
        // }

        cleaning_eta.push_back(
            GenDressedLepton_eta[i]
        );

        cleaning_phi.push_back(
            GenDressedLepton_phi[i]
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
        // Jet pT
        if (
            GenJet_pt[iJet] < JET_PT_MIN
        )
        {
            continue;
        }

        // Jet eta
        if (
            std::abs(GenJet_eta[iJet])
            > JET_ETA_MAX
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

        if (overlapsLepton)
            continue;

        ++nCleanJets;
    }

    return nCleanJets;
}


#endif

// const RVecI &LeptonGen_isPrompt,