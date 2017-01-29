import ROOT as R
import numpy as n
import glob
#Use events with one lepton

#Preselection
# MET > 200 GeV
# Ht > 300 GeV (Sum of transverse momentum of all jets)
# ISR-Jet pt > 100 GeV (I use just the jet with the highest pt)
# lepton with pt > 5 GeV

#Selection
# 
# Using just events where the pt of a bottom quark is less than 30 GeV 

#Signal region
# lepton pt < 30 GeV
# MET > 300 GeV

#Variables
lepton = [11,13]

#read files
file_dir_base = "/afs/hephy.at/user/m/mwinder/public/flat_GEN_ROOT/GenJetNoNu/"
file_list = glob.glob(file_dir_base +"/degStop300_270_Chunk*/treeProducerSusySingleLepton/tree.root")
t = R.TChain("tree")
for f in file_list:
      t.Add(f)

total = t.GetEntries()

cut_met = "GenMET_pt>200"
cut_ht = "Sum$(GenJet_pt*(abs(GenJet_eta)<2.4&&GenJet_pt>30))>300"
cut_isr = "Sum$(abs(GenJet_eta)<2.4&&GenJet_pt>100)>0"
cut_nlep = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&abs(GenPart_eta)<2.4&&GenPart_pt>5&&GenPart_pt<30)>0"
cut_nlep20 = "Sum$((abs(GenPart_pdgId)==11||abs(GenPart_pdgId)==13)&&abs(GenPart_eta)<2.4&&GenPart_pt>20&&GenPart_pt<30)<2"
cut_nb = "Sum$(abs(GenPart_pdgId)==5&&abs(GenPart_eta)<2.4&&GenPart_pt>30&&GenPart_pt<60)>0"


cuts = [cut_met,cut_ht,cut_isr,cut_nlep,cut_nlep20,cut_nb]
cut = "&&".join(cuts)

hh = R.TH1F("hh","",100,0,1000)
t.Draw("nGenJet>>hh",cut,"goff")
accepted = hh.GetEntries()

        
print "--------------"
print "Accepted","Total","Acceptance"
print accepted,total, float(accepted)/float(total)
