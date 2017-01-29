from __future__ import print_function
import ROOT as R
import numpy as n
import glob
#Selection
# MET > 200 GeV
# Ht > 300 GeV (Sum of transverse momentum of jets with with pt > 30 and abs(pseudorapidity)<2.4
# ISR-Jet pt > 100 GeV (One Jet needs higher pt than 100 GeV)
# lepton with pt between 5 and 30 GeV and abs(eta)<2.4 and maximum one lepton with pt > 20
# Use just events where the pt of a bottom quark is between 30 and 60 GeV with abs(eta)<2.4 (soft-b events)

#Variables
lepton = range(11,14,2)# + range(-13,-10,2)
print("read files")
#read files
file_dir_base = "/afs/hephy.at/user/m/mwinder/public/flat_GEN_ROOT/GenJetNoNu/"
file_list = glob.glob(file_dir_base +"/degStop300_270_Chunk*/treeProducerSusySingleLepton/tree.root")
t = R.TChain("tree")
for f in file_list:
	t.Add(f)
#Preselection and Selection
evnumber = t.GetEntries()
print("calculation started")

#MET Using 200 GeV of Preselection at the moment!
met = "GenMET_pt>=200"
#Ht (Just the visible Jets (every single Jet_pt > 30 and abs(Jeteta) < 2.4)) - Sum has to be bigger than 300
ht = "Sum$(GenJet_pt*(GenJet_pt>30&&abs(GenJet_eta)<2.4))>300"
#ISR JET (at least one jet with pt above 100 and abs(Jeteta) < 2.4) 
ISR = "Sum$(GenJet_pt>100&&abs(GenJet_eta)<2.4)>0"  #Wieso muss ich  hier eine Summe bilden und dann groesser 0 - geht ohne nicht auch? - Ws werden Events doppelt gezaehlt? zB bei zwei Jets mit pt > 100 in einem Event werden diese doppelt angenommen? 
#Just one lepton in the event with lepton pt > 20 pt
lep20 = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&GenPart_pt>20&&GenPart_pt<30&&abs(GenPart_eta)<2.4)<2"
#Lepton pt between 5 GeV and 30 GeV
lep = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&GenPart_pt>5&&GenPart_pt<30&&abs(GenPart_eta)<2.4)>0"
#Use just events with bottom quark 30 < pt < 60
bottom = "Sum$(abs(GenPart_pdgId)==5&&GenPart_pt<60&&GenPart_pt>30&&abs(GenPart_eta)<2.4)>0" 
#put together
cuts = [met,ht,ISR,lep20,lep,bottom]
cut = "&&".join(cuts)
	
#draw
hh = R.TH1F("hh","Jets",1000,0,300)
hh.SetLineColor(R.kBlue)
#hh.SetFillColor(R.kBlue)
hh.SetXTitle("test")
hh.SetYTitle("Number of Jets")
hh.GetYaxis().SetTitleOffset(1)
t.Draw("nGenJet>>hh",cut)

ev = hh.GetEntries()
print("--------------------------")
print("accepted","Events","Acceptance (%)")
print(ev,evnumber,float(ev)/float(evnumber)*100)
    
