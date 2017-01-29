import ROOT as R
import numpy as n
import glob
accepted = 0
total = 0
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

#Preselection and Selection
nEvents = t.GetEntries()
print "number of events",nEvents
for ievt in xrange(nEvents):
	t.GetEntry(ievt)
	total += 1
        if(total and not total%10000): print "analyzed",total
#MET Using 200 GeV of Preselection at the moment!
	MET = t.GenMET_pt
	if MET <= 200: continue
#Ht
#ISR JET
#	H = n.sum(t.GenJet_pt)
	H = 0
        nisr = 0
        for ij in xrange(t.nGenJet):
        	if abs(t.GenJet_eta[ij]) < 2.4:
        		if t.GenJet_pt[ij] > 30:
                		H += t.GenJet_pt[ij]
                        if t.GenJet_pt[ij] > 100:
                        	nisr += 1
	if H <= 300: continue
        if nisr == 0: continue
	       
#Just one lepton in the event
#	if len(set(t.GenPart_pdgId).intersection(set(lepton))) > 1:
#		continue
#Lepton pt between 5 GeV and 30 GeV
	
        nlep = 0
        nlep20 = 0
        nb = 0
        for igp in xrange(t.nGenPart):
        	if abs(t.GenPart_pdgId[igp]) in lepton and \
                       t.GenPart_pt[igp] > 5 and \
                       t.GenPart_pt[igp] < 30 and \
                       abs(t.GenPart_eta[igp]) < 2.4:
                	nlep += 1
                        if t.GenPart_pt[igp] > 20:
                        	nlep20 += 1
                if abs(t.GenPart_pdgId[igp])==5 and \
                       t.GenPart_pt[igp] > 30 and \
                       t.GenPart_pt[igp] < 60 and \
                       abs(t.GenPart_eta[igp]) < 2.4:
                	nb += 1
                
	if nlep == 0: continue # ask for a lepton
        if nlep20 > 1: continue # but not two above 20 GeV
        if nb == 0: continue # this is an example for the case we want a soft b (SR2) - even better would be to use GenJet

#Prints
	accepted += 1
        
print "--------------"
print "Accepted","Total","Acceptance"
print accepted,total, float(accepted)/float(total)
