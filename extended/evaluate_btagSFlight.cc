#ifndef BTAGLIGHTSF
#define BTAGLIGHTSF

#include <vector>
#include <map>
#include <string>
#include <iostream>
#include "TVector2.h"
#include "Math/Vector4Dfwd.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"
#include "TString.h"

#include "ROOT/RVec.hxx"
#include "TH2D.h"
#include "TFile.h"
#include "correction.h"

using namespace ROOT;
using namespace ROOT::VecOps;
using correction::CorrectionSet;


// ===============================
// Light jet b-tag SF class
// ===============================

class btagSFlight {

public:

    btagSFlight(TString eff_map, const std::string year, TString algo_extension="");
    ~btagSFlight();

    TH2F* h_ljet_eff;

    std::string year;
    std::unique_ptr<CorrectionSet> cset;

    RVecF operator()(

        RVecF         CleanJet_pt,
        RVecF         CleanJet_eta,
        RVecI         CleanJet_jetIdx,
        unsigned int  nCleanJet,
        RVecI         Jet_hadronFlavour,
        RVecF         Jet_btag,
        const std::string WP,
        RVec<std::string> systematic
    )
    {

        RVecF results(systematic.size(),1.0);

        std::string correctionKey;
        std::string wpKey;

        if (year == "2024_Summer24") {

            correctionKey = "UParTAK4_light";
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

                double pt  = std::min(double(CleanJet_pt[iJ]),9999.0);
                double eta = std::abs(CleanJet_eta[iJ]);

                if (pt <= 20.0 || eta >= 2.5)
                    continue;

                int flav = Jet_hadronFlavour[idx];

                bool tagged = Jet_btag[idx] > cset_wp->evaluate({WP});


                if (tagged) {

                    if (flav == 0) {

                        float sf = cset_btag->evaluate(
                            {systematic[i],WP,0,eta,pt});

                        btag_sf *= sf;

                    }

                }
                else {

                    float btag_eff = getEff(pt,eta,flav);

                    if (btag_eff == 1.0)
                        continue;

                    if (flav == 0) {

                        float sf = cset_btag->evaluate(
                            {systematic[i],WP,0,eta,pt});

                        btag_sf *= (1.0 - btag_eff*sf)/(1.0 - btag_eff);

                    }

                }

            }

            results[i] = btag_sf;

        }

        return results;

    }

private:

    float getEff(float pt,float eta,int flavour);

};



// ===============================
// Constructor
// ===============================

btagSFlight::btagSFlight(TString eff_map,const std::string year,TString algo_extension)
{

    this->year = year;

    if (year == "2024_Summer24") {

        cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/btagging.json.gz");

    }


    TFile *reff = TFile::Open(eff_map,"READ");

    if (!reff)
        throw std::runtime_error("Cannot open btag efficiency file");

    auto hl = (TH2F*)reff->Get("ljet"+algo_extension+"_eff");

    if (!hl)
        throw std::runtime_error("Light jet efficiency histogram missing");

    h_ljet_eff = (TH2F*)hl->Clone();
    h_ljet_eff->SetDirectory(0);

    reff->Close();

}



// ===============================
// Efficiency lookup
// ===============================

float btagSFlight::getEff(float pt,float eta,int flavour)
{

    if (flavour != 0)
        return 1.0;

    int xbin = h_ljet_eff->GetXaxis()->FindBin(pt);
    int ybin = h_ljet_eff->GetYaxis()->FindBin(eta);

    return h_ljet_eff->GetBinContent(xbin,ybin);

}



// ===============================
// Destructor
// ===============================

btagSFlight::~btagSFlight()
{

    std::cout << "Cleaning up memory" << std::endl;

    delete h_ljet_eff;

}

#endif

// --- BTag SF class for light jets ---
// class btagSFlight {
      
//   public:
//     btagSFlight(TString eff_map, const std::string year, TString algo_extension);
//     ~btagSFlight();
    
//     TH2F* h_ljet_eff;

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
    

//       if (year == "2024_Summer24"){
// 	      correctionKey         = "UParTAK4_light";
// 	      wpKey                 = "UParTAK4_wp_values";
//         }

//         auto cset_btag_light  = cset->at(correctionKey);
//         auto cset_btag_wps = cset->at(wpKey);

//      for (long unsigned int i=0; i<systematic.size(); i++){
//         float btag_sf  = 1.;

//         for (unsigned iJ{0}; iJ != nCleanJet; ++iJ) {
// 	    double pt = ROOT::VecOps::Min(ROOT::RVecD{CleanJet_pt[iJ], 9999.9});
	  
// 	    if (CleanJet_pt[iJ] <= 20. || abs(CleanJet_eta[iJ]) >= 2.5) continue;
//         	if (Jet_btag[CleanJet_jetIdx[iJ]] > cset_btag_wps->evaluate({WP})) {

// 	        if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 0) {
// 	        if (year == "2024_Summer24"){
//                 btag_sf *= cset_btag_light->evaluate({systematic[i], WP, 0, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]});
// 		        // btag_sf *= cset_btag_light->evaluate({"central", WP, 0, abs(CleanJet_eta[iJ]), pt});
//             }
//             // else{
// 		    //     btag_sf *= cset_btag_light->evaluate({systematic[i], WP, 0, abs(CleanJet_eta[iJ]), pt});		
// 	        // }
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
// 	      if (Jet_hadronFlavour[CleanJet_jetIdx[iJ]] == 0) {
//             if (year == "2024_Summer24"){
//                 btag_sf *= (1-btag_eff*cset_btag_light->evaluate({systematic[i], WP, 0, abs(CleanJet_eta[iJ]), CleanJet_pt[iJ]}))/(1-btag_eff);
//                 // btag_sf *= (1-btag_eff*cset_deepJet_mujets_alt->evaluate({"central", WP, 0, abs(CleanJet_eta[iJ]), pt}))/(1-btag_eff);
//             }
            
//             // else{
//             //     btag_sf *= (1-btag_eff*cset_deepJet_mujets->evaluate({systematic[i], WP, 0, abs(CleanJet_eta[iJ]), pt}))/(1-btag_eff);
//             // }
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


// btagSFlight::btagSFlight(TString eff_map, const std::string year, TString algo_extension = "") {
    
    // --- Patch graphics classes first ---
    //const char* graphicsClasses[] = { "TPaletteAxis", "TCanvas", "TFrame", "TAttBBox2D", "TBox" };
    //for (auto clsname : graphicsClasses) {
    //    if (TClass* cl = TClass::GetClass(clsname)) cl->IgnoreTObjectStreamer();
    //}

    // std::string home = std::string(std::getenv("STARTPATH"));
    // std::string to_replace = "start.sh";
    // size_t start  = home.find(to_replace);
    // size_t stop   = to_replace.length();
    // home.replace(start, stop, "");

    // if (year == "2024_Summer24")
    // {
    //   // cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/" + year + "/latest/btagging.json.gz");
    //   cset = CorrectionSet::from_file("/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/latest/btagging.json.gz");
    // }

    // TFile *reff = TFile::Open(eff_map, "READ");
    // h_ljet_eff  = (TH2F*)reff->Get("ljet"+algo_extension+"_eff")->Clone();
    // h_ljet_eff->SetDirectory(0);
    // reff->Close();
    // }

    // float btagSFlight::getEff(float pt, float eta, int flavour) {
    // int xbin, ybin;
    // float eff;
    // if (flavour == 0) {
    // xbin = h_ljet_eff->GetXaxis()->FindBin(pt);
    // ybin = h_ljet_eff->GetYaxis()->FindBin(eta);
    // eff  = h_ljet_eff->GetBinContent(xbin, ybin);
    // }
    // else {
    // eff   = 1.;
    // }
    // return eff;
    // }

    // btagSFlight::~btagSFlight(){
    // std::cout << "Cleaning up memory" << std::endl;
    // h_ljet_eff->Delete();
    // }

    // #endif





