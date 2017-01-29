from __future__ import print_function
import ROOT as R
import numpy as n
import glob
ev = 0
evnumber = 0

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
nEvents = t.GetEntries()
print("calculation started")
for ievt in xrange(nEvents):
	t.GetEntry(ievt)
	evnumber += 1
	if (evnumber and not evnumber%10000): print("analyzed",evnumber)	
#MET Using 200 GeV of Preselection at the moment!
	MET = t.GenMET_pt
	if MET <= 200:
		continue
#Ht (Just the visible Jets (every single Jet_pt > 30 and abs(Jeteta) < 2.4)) - Sum has to be bigger than 300
	execfile("htjet.py")
	htjet(t.nGenJet,t.GenJet_pt,t.GenJet_eta)
	if Ht <= 300:
		continue
#ISR JET (at least one jet with pt above 100 and abs(Jeteta) < 2.4) 
	if ISR == 0:
		continue		 			
#Lepton pt between 5 GeV and 30 GeV
#Just one lepton in the event with lepton pt > 20 pt
#Function leptonpt:
	execfile("leptonpt.py")
        leptonpt(t.GenPart_pdgId,t.GenPart_pt,lepton,t.GenPart_eta)
	if nlep == 0:
		continue
	if nlep20 > 1:
		continue	
#Use just events with bottom quark 30 < pt < 60
	if nb == 0:
		continue
#Prints
	ev += 1
print("--------------------------")
print("accepted","Events","Acceptance (%)")
print(ev,evnumber,float(ev)/float(evnumber)*100)
    
