from __future__ import print_function
from Workspace.HEPHYPythonTools.xsecSMS import stop13TeV_NLONLL
import os, pickle
import ROOT as R
import numpy as n
import glob

#genFilterEff = pickle.load(file(os.path.expandvars("$CMSSW_BASE/src/Workspace/DegenerateStopAnalysis/data/filterEfficiency/SMS_T2tt_dM_10to80_genHT_160_genMET_80/filterEffs_SMS_T2tt_dM_10to80_genHT_160_genMET_80.pkl" )))

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
#from document: ISR-Jet pt > 325

print("read files")
file_dir_base = "/afs/hephy.at/user/m/mwinder/public/flat_GEN_ROOT/GenJetNoNu/"
file_list = glob.glob(file_dir_base +"/degStop300_270_Chunk*/treeProducerSusySingleLepton/tree.root")
t = R.TChain("tree")
for f in file_list:
	t.Add(f)
#----------------------------------------------------------------------
#Preselection and Selection
evnumber = t.GetEntries()
print("calculation started")

#susy = "GenSusyMNeutralino==270&&GenSusyMStop==300"

#Preselection
#CT1 + ISR > 100
Ct1 = "(GenMET_pt>200&&(Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))-100)>200&&Sum$((GenJet_pt>100&&abs(GenJet_eta)<2.4))>0)"
##If two hard jets: 
#dphi = "acos(cos(Sum$(GenJet_pt>60&&abs(GenJet_eta<2.4)==2)*(GenJet_phi[0]-GenJet_phi[1])))<2.5"

dphi = "acos(cos(Sum$((Sum$(GenJet_pt>60&&abs(GenJet_eta)<2.4)<=2&&GenJet_pt==Max$((GenJet_pt>60&&abs(GenJet_eta)<2.4)*GenJet_pt)&&Sum$((Sum$(GenJet_pt>60&&abs(GenJet_eta)<2.4)<=2&&GenJet_pt>60&&abs(GenJet_eta)<2.4&&GenJet_pt<Max$((GenJet_pt>60&&abs(GenJet_eta)<2.4)*GenJet_pt))*GenJet_phi)!=0)*GenJet_phi)-Sum$((Sum$(GenJet_pt>60&&abs(GenJet_eta)<2.4)<=2&&GenJet_pt>60&&abs(GenJet_eta)<2.4&&GenJet_pt<Max$((GenJet_pt>60&&abs(GenJet_eta)<2.4)*GenJet_pt))*GenJet_phi)))<2.5"

#Veto events with more than three hard jets
vetohard = "Sum$(GenJet_pt>60&&abs(GenJet_eta)<2.4)<3"
##Veto events with tau lepton
vetotau = "Sum$(abs(GenPart_pdgId)==15&&GenPart_pt>20)==0"
###Singlelepton
lep = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&GenPart_pt>5&&abs(GenPart_eta)<2.4)>0"
lep20 = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&abs(GenPart_eta)<2.4&&GenPart_pt>20)<=2"

#--------------------------------------------------------------------
#Section SR1

#ctSR1 = "(met_genPt>300&&(Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))-100)>300&&Sum$((GenJet_pt>100&&abs(GenJet_eta)<2.4))>0)"
ctSR1 = "min(GenMET_pt,Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))-100)>300"
etaSR1 = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&GenPart_pt>5&&abs(GenPart_eta)<1.5)>0"
lepSR1 = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&GenPart_pt>5&&GenPart_pt<30&&abs(GenPart_eta)<1.5)>0"
chargeSR1 = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&GenPart_pt>5&&GenPart_pt<30&&abs(GenPart_eta)<1.5&&GenPart_charge<0)>0"
#Vetobjet missing
#--------------------------------------------------------------------
#Section SR2

#CtSR2 = "min(GenMET_pt,Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))-100)>300"
#lepSR2 = "abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13&&GenPart_pt<30"
#Bottom missing

#put together
cuts = [Ct1,dphi,vetohard,vetotau,lep,lep20,ctSR1,etaSR1,lepSR1,chargeSR1]

#draw
hh = R.TH1F("hh","Jets",1000,0,300)
for x in xrange(len(cuts)):
	cut = 0
	cut = "&&".join(cuts[0:(x+1)])

	t.Draw("nGenJet>>hh",cut,"goff")	
#	if x == 0:
#		evnumber1 = hh.GetEntries()
	ev = hh.GetEntries()
	
	print("--------------------------")
	print("Cut","Events","acceptance","T2tt-300-270")
	print(x,ev,ev/evnumber,(ev/evnumber)*stop13TeV_NLONLL[300]*12.9*10**3)
    	
