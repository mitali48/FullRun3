#ifndef BTAGSF
#define BTAGSF
#include <vector>
#include <map>
#include <string>
#include <iostream>
#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "TString.h"

#include <iostream>
#include "ROOT/RVec.hxx"
#include "TH2D.h"
#include "TFile.h"
#include "correction.h"

using namespace ROOT;
using namespace ROOT::VecOps;
using correction::CorrectionSet;


class btagSFbc {

public:

    btagSFbc(TString eff_map, const std::string year, TString algo_extension="");
    ~btagSFbc();

    TH2F* h_bjet_eff;
    TH2F* h_cjet_eff;

    std::string year;
    std::unique_ptr<CorrectionSet> cset;

    RVecF operator()(
        RVecF         CleanJet_pt,
        RVecF         CleanJet_eta,
        RVecI         CleanJet_jetIdx,
        unsigned int  nCleanJet,
        RVecI         Jet_hadronFlavour,
        RVecF         Jet_btag,
        const std::string  WP,
        RVec<std::string> systematic
    )
    {

        RVecF results(systematic.size(), 1.0);

        std::string correctionKey;
        std::string wpKey;

        if (year == "2024_Summer24") {
            correctionKey = "UParTAK4_comb";
            wpKey         = "UParTAK4_wp_values";
        }

        auto cset_btag = cset->at(correctionKey);
        auto cset_wp   = cset->at(wpKey);

        for (size_t i = 0; i < systematic.size(); ++i) {

            float btag_sf = 1.0;

            for (unsigned int iJ = 0; iJ < nCleanJet; ++iJ) {

                int idx = CleanJet_jetIdx[iJ];

                if (idx < 0 || idx >= (int)Jet_btag.size())
                    continue;

                double pt  = std::min(double(CleanJet_pt[iJ]), 9999.0);
                double eta = std::abs(CleanJet_eta[iJ]);

                if (pt <= 20.0 || eta >= 2.5)
                    continue;

                int flav = Jet_hadronFlavour[idx];

                bool tagged = Jet_btag[idx] > cset_wp->evaluate({WP});

                if (tagged) {

                    if (flav == 5 || flav == 4) {

                        float sf = cset_btag->evaluate(
                            {systematic[i], WP, flav, eta, pt});

                        btag_sf *= sf;
                    }

                } else {

                    float btag_eff = getEff(pt, eta, flav);

                    if (btag_eff == 1.0)
                        continue;

                    if (flav == 5 || flav == 4) {

                        float sf = cset_btag->evaluate(
                            {systematic[i], WP, flav, eta, pt});

                        btag_sf *= (1.0 - btag_eff * sf) / (1.0 - btag_eff);
                    }
                }
            }

            results[i] = btag_sf;
        }

        return results;
    }

private:

    float getEff(float pt, float eta, int flavour);

};




/* =========================
   Constructor
   ========================= */

btagSFbc::btagSFbc(TString eff_map, const std::string year, TString algo_extension)
{

    this->year = year;

    if (year == "2024_Summer24") {

        cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/btagging.json.gz");

    }

    TFile *reff = TFile::Open(eff_map, "READ");

    if (!reff)
        throw std::runtime_error("Cannot open btag efficiency file");

    auto hb = (TH2F*)reff->Get("bjet"+algo_extension+"_eff");
    auto hc = (TH2F*)reff->Get("cjet"+algo_extension+"_eff");

    if (!hb || !hc)
        throw std::runtime_error("Efficiency histograms not found");

    h_bjet_eff = (TH2F*)hb->Clone();
    h_cjet_eff = (TH2F*)hc->Clone();

    h_bjet_eff->SetDirectory(0);
    h_cjet_eff->SetDirectory(0);

    reff->Close();
}




/* =========================
   Efficiency lookup
   ========================= */

float btagSFbc::getEff(float pt, float eta, int flavour)
{

    int xbin, ybin;
    float eff;

    if (flavour == 5) {

        xbin = h_bjet_eff->GetXaxis()->FindBin(pt);
        ybin = h_bjet_eff->GetYaxis()->FindBin(eta);

        eff  = h_bjet_eff->GetBinContent(xbin, ybin);

    }
    else if (flavour == 4) {

        xbin = h_cjet_eff->GetXaxis()->FindBin(pt);
        ybin = h_cjet_eff->GetYaxis()->FindBin(eta);

        eff  = h_cjet_eff->GetBinContent(xbin, ybin);

    }
    else {

        eff = 1.0;

    }

    return eff;
}




/* =========================
   Destructor
   ========================= */

btagSFbc::~btagSFbc()
{

    std::cout << "Cleaning up memory" << std::endl;

    delete h_bjet_eff;
    delete h_cjet_eff;

}

#endif


// class btagSFbc {
  
//   public:
//     btagSFbc(TString eff_map, const string year, TString algo_extension);
//     ~btagSFbc();  

//     TH2F* h_bjet_eff;
//     TH2F* h_cjet_eff;
//     std::string year;
//     std::unique_ptr<CorrectionSet> cset;

//     RVecF operator()(
// 		    RVecF         CleanJet_pt,
// 		    RVecF         CleanJet_eta,
// 		    RVecI         CleanJet_jetIdx,
// 		    unsigned int  nCleanJet,
// 		    RVecI         Jet_hadronFlavour,
// 		    RVecF         Jet_btag,
// 		    const string  WP,
// 		    RVec<string> systematic
// 		     )
//     {

//       RVecF results(systematic.size(), 1.0);

//       std::string correctionKey;
//       std::string wpKey;
    
//     // Two possible correction keys for 2024, UParTAK4_comb obtained with a combination of kinfit and ptrel 
//     // and UParTAK4_mujets obtained with ptrel method only.
//     // 'central' for nominal SF. 'up/down' for total SF variation. Other 'up/down_X' for additional uncertainty
//       if (year == "2024_Summer24"){
// 	      correctionKey         = "UParTAK4_comb";                   
//   	      wpKey                = "UParTAK4_wp_values";
//         }

//         auto cset_btag_light  = cset->at(correctionKey);
//         auto cset_btag_wps = cset->at(wpKey);
//      for (long unsigned int i=0; i<systematic.size(); i++){
//         float btag_sf  = 1.;

//         for (unsigned iJ{0}; iJ != nCleanJet; ++iJ) {
// 	    double pt = ROOT::VecOps::Min(ROOT::RVecD{CleanJet_pt[iJ], 9999.9});
	  
// 	    if (CleanJet_pt[iJ] <= 20. || abs(CleanJet_eta[iJ]) >= 2.5) continue;
//         	if (Jet_btag[CleanJet_jetIdx[iJ]] > cset_btag_wps->evaluate({WP})) {

// 	        if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5) {
//               btag_sf *= cset_btag_light->evaluate({systematic[i], WP, 5, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
// 		        // btag_sf *= cset_btag_light->evaluate({"central", WP, 0, abs(CleanJet_eta[iJ]), pt});
//             }
//             else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4) {
//               btag_sf *= cset_btag_light->evaluate({systematic[i], WP, 4, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
//             }
// 	        }
// 	        else {
// 	            continue;
// 	        }
// 	        }
// 	    else {
// 	    float btag_eff = getEff(pt, CleanJet_eta[iJ], Jet_hadronFlavour[CleanJet_jetIdx[iJ]]);
// 	    if (btag_eff == 1.) {
// 	      continue;
// 	    }
// 	    else {
// 	      if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 5) {
//                 btag_sf *= (1-btag_eff*cset_btag_light->evaluate({systematic[i], WP, 5, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
//             }
//             else if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 4) {
//               btag_sf *= (1-btag_eff*cset_btag_light->evaluate({systematic[i], WP, 4, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
//             }
//             else {
//                 continue;
//             }
// 	    }
// 	  }
// 	}
// 	    results[i] = btag_sf;
//     }
//       return results;
//     }

//     private:
//     float getEff(float pt, float eta, int flavour);
  
// };

// btagSFbc::btagSFbc(TString eff_map, const std::string year, TString algo_extension = "") {
    
//     // --- Patch graphics classes first ---
//     //const char* graphicsClasses[] = { "TPaletteAxis", "TCanvas", "TFrame", "TAttBBox2D", "TBox" };
//     //for (auto clsname : graphicsClasses) {
//     //    if (TClass* cl = TClass::GetClass(clsname)) cl->IgnoreTObjectStreamer();
//     //}

//     std::string home = std::string(std::getenv("STARTPATH"));
//     std::string to_replace = "start.sh";
//     size_t start  = home.find(to_replace);
//     size_t stop   = to_replace.length();
//     home.replace(start, stop, "");

//     if (year == "2024_Summer24")
//     {
//         // cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/" + year + "/latest/btagging.json.gz");
//         cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/btagging.json.gz");
//     }

//   TFile *reff = TFile::Open(eff_map, "READ");
//   h_bjet_eff  = (TH2F*)reff->Get("bjet"+algo_extension+"_eff")->Clone();
//   h_cjet_eff  = (TH2F*)reff->Get("cjet"+algo_extension+"_eff")->Clone();
//   h_bjet_eff->SetDirectory(0);
//   h_cjet_eff->SetDirectory(0);
//   reff->Close();
// }

// float btagSFbc::getEff(float pt, float eta, int flavour) {
//   int xbin, ybin;
//   float eff;
//   if (flavour == 5) {
//     xbin = h_bjet_eff->GetXaxis()->FindBin(pt);
//     ybin = h_bjet_eff->GetYaxis()->FindBin(eta);
//     eff  = h_bjet_eff->GetBinContent(xbin, ybin);
//   }
//   else if (flavour == 4) {
//     xbin = h_cjet_eff->GetXaxis()->FindBin(pt);
//     ybin = h_cjet_eff->GetYaxis()->FindBin(eta);
//     eff  = h_cjet_eff->GetBinContent(xbin, ybin);
//   }
//   else {
//     eff   = 1.;
//   }
//   return eff;
// }

// btagSFbc::~btagSFbc(){
//   std::cout << "Cleaning up memory" << std::endl;
//   h_bjet_eff->Delete();
//   h_cjet_eff->Delete();
// }
 
// #endif
