#ifndef CLEANGENJET
#define CLEANGENJET

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

class CleanGenJet {

public:

    CleanGenJet(const std::string& variable)
    : variable_(variable)
    {
        std::cout << "Constructing CleanGenJet for variable: "
                << variable_ << std::endl;
    }

    ~CleanGenJet() 
    {
        std::cout << "Destructing CleanGenJet for variable: "
              << variable_ << std::endl;
    }

    float operator()(
        RVecF GenJet_pt,
        RVecF GenJet_eta,
        RVecF GenJet_phi,
        RVecF DressedLepton_pt,
        RVecF DressedLepton_eta,
        RVecF DressedLepton_phi,
        RVecI LeptonGen_isPrompt
    )
    {
        std::vector<ROOT::Math::PtEtaPhiMVector> cleanGenJets;

        const unsigned int nGenJet = GenJet_pt.size();
        const unsigned int nL = DressedLepton_pt.size();

        for (unsigned int iJ = 0; iJ < nGenJet; ++iJ) {

            // Jet selection
            if (GenJet_pt[iJ] < 30.)
                continue;

            if (std::abs(GenJet_eta[iJ]) > 2.5)
                continue;

            bool cleanJet = true;

            // Remove GenJets close to prompt dressed leptons
            for (unsigned int iL = 0; iL < nL; ++iL) {

                if (DressedLepton_pt[iL] < 10.)
                    continue;

                if (!LeptonGen_isPrompt[iL])
                    continue;

                if (ROOT::VecOps::DeltaR(
                        GenJet_eta[iJ],
                        GenJet_phi[iJ],
                        DressedLepton_eta[iL],
                        DressedLepton_phi[iL]) < 0.4) {

                    cleanJet = false;
                    break;
                }
            }

            if (cleanJet) {
                cleanGenJets.emplace_back(
                    GenJet_pt[iJ],
                    GenJet_eta[iJ],
                    GenJet_phi[iJ],
                    0.0
                );
            }
        }

        if (variable_ == "njet") {
            return cleanGenJets.size();
        }

        std::cout << "Unknown variable: " << variable_ << std::endl;
        return -9999.;
    }

private:

    std::string variable_;
};

#endif