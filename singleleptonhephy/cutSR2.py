from __future__ import print_function
import ROOT as R
import numpy as n
import glob

#Info
#attributes ``soft'' and ``hard'' refer to the pTpT ranges 30-60 GeV and >>60 GeV, respectively
#CT = min(MET,Ht-100)
#silicon tracker abs(eta)<2.5
#myon tracker abs(eta)<2.4
#endcap calorimeters abs(eta)<3.0

#Jets pt > 30 GeV and abs(eta) < 2.4
#Myons and electrons pt > 5 GeV
#lepton cone size dR > 0.3 with dR = sqrt(dphi**2+deta**2)
#Met > 100 GeV

#Preselection

#CT1 > 200 GeV (MET > 200)
#ISR-Jet pt > 100 GeV and abs(eta) < 2.4
#dphi(j1,j2) < 2.5 rad (if two hard jets)
#Hard 3rd Jet Veto (Cancel events with three hard jets)
#Tau Veto (Events are rejected if a taulepton with pt > 20)
#Single lepton (At least one lepton with pt > 5 GeV and abs(eta) < 2.4 must be present)

#Event Selection (SR1 - Signal Region 1)
#Ct1 > 300 GeV
#Veto BJets (not here)
#lepton abs(eta) < 1.5 
#lepton pt < 30 GeV
#Charge(l) < 0

#Selection (SR2)
#Ct2 > 300 GeV
#1 or more soft but no hard BJet (not here) 
#lepton pt < 30 GeV
#ISR-Jet pt > 325

print("read files")
file_dir_base = "/data/nrad/cmgTuples/8020_mAODv2_v5/RunIISpring16MiniAODv2/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1/"
file_list = glob.glob(file_dir_base +"/SMS-T2tt_dM-10to80_genHT-160_genMET-80_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_RunIISpring16MiniAODv2-PUSpring16Fast_80X_mcRun2_asymptotic_2016_miniAODv2_v0-v1_Chunk_*/tree.root")

t = R.TChain("tree")
for f in file_list:
	t.Add(f)
#----------------------------------------------------------------------
#Preselection and Selection
evnumber = t.GetEntries()
print("calculation started")

susy = "GenSusyMNeutralino==270&&GenSusyMStop==300"

#Preselection
#CT1  
met = "met_genPt>=100"
Ct1 = "min(met_genPt,Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))-100)>200"
#ISR JET (at least one jet with pt above 100 and abs(Jeteta) < 2.4) 
ISR = "Sum$(GenJet_pt>325&&abs(GenJet_eta)<2.4)>0" #ISR pt is now > 325  
##If two hard jets: dphi<2.5 (not checked if eta > 2.4)
dphi = "acos(cos(Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt==Max$(GenJet_pt)&&Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi)!=0)*GenJet_phi)-Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi)))<2.5"
#Veto events with more than three hard jets
vetohard = "Sum$(GenJet_pt>60)<3"
##Veto events with tau lepton
vetotau = "Sum$(abs(GenPart_pdgId)==15)==0"
###Singlelepton
lep = "Sum$(abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13&&GenPart_pt>5&&abs(GenPart_eta)<2.4)>0"

#--------------------------------------------------------------------
#Section SR1
#ctSR1 = "min(met_genPt,Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))-100)>300"
#etaSR1 = "Sum$(abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13&&abs(GenPart_eta)<1.5)>0"
#lepSR1 = "Sum$(abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13&&GenPart_pt<30)>0"
#chargeSR1 = "Sum$(abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13&&GenPart_charge<0)>0"
#Vetobjet missing
#--------------------------------------------------------------------
#Section SR2
ctSR2 = "min(met_genPt,Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))-100)>300"
lepSR2 = "Sum$(abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13&&GenPart_pt<30&&abs(GenPart_eta)<2.4)>0"
#Bottom missing

#put together
cuts = [susy,met,Ct1,ISR,dphi,vetohard,vetotau,lep,ctSR2,lepSR2]
cut = "&&".join(cuts)
	
#draw
hh = R.TH1F("hh","Jets",1000,0,300)
#hh.SetLineColor(R.kBlue)
#hh.SetFillColor(R.kBlue) 
#hh.SetXTitle("test")
#hh.SetYTitle("Number of Jets")
#hh.GetYaxis().SetTitleOffset(1)
t.Draw("nGenJet>>hh",cut,"goff")

ev = hh.GetEntries()
print("--------------------------")
print("accepted","Events","Acceptance (%)")
print(ev,evnumber,float(ev)/float(evnumber)*100)
    
