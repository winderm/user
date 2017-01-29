from __future__ import print_function
import ROOT as R
import glob
from math import *
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
print("number of events",evnumber)
total = 0
hh = R.TH1F("hh","deltaR",100,0,5)
print("Calculation started")

#Loop over all events
for e in xrange(evnumber):
#Variables
	part = []
	jet = []
	total += 1
	
	if(total and not total%10000): print("analyzed",total)
#Get the length of one event:
	t.GetEntry(e)
	pdgid = []
	for x in xrange(t.nGenPart):
		if abs(t.GenPart_pdgId[x]) == 5 and t.GenPart_pt[x] > 10: # and  abs(t.GenPart_eta[x]) < 2.4: #
		#and t.GenPart_pt[x] < 60 and t.GenPart_pt[x] > 30:
			part.append(float(t.GenPart_eta[x]))
			part.append(float((t.GenPart_phi[x]+2.*pi)%(2.*pi)))
			pdgid.append(t.GenPart_pdgId[x])

	if not pdgid:
		continue	
#			part1 = [float(t.GenPart_eta[x]),float((t.GenPart_phi[x]+2.*pi)%(2.*pi))]
#			part.append(part1)
	mass = []
	for x in xrange(t.nGenJet):
		if abs(t.GenJet_eta[x]) < 2.4 and t.GenJet_pt[x] > 20:
			jet.append(float(t.GenJet_eta[x]))
			jet.append(float((t.GenJet_phi[x]+2.*pi)%(2.*pi)))
			mass.append(t.GenJet_mass[x])
#			jet1 = [float(t.GenJet_eta[x]),float((t.GenJet_phi[x]+2.*pi)%(2.*pi))]
#			jet.append(jet1)
	if not mass:
		continue
	dR = 0.
	dm = 999.	
	for y in xrange(len(part)/2):
		for z in xrange(len(jet)/2):
			dR = float(sqrt(pow(fabs(part[y*2]-jet[z*2]),2)+pow(fabs(part[y*2+1]-jet[z*2+1]),2)))
#			dR = float(sqrt(pow(fabs(part[y][0]-jet[z][0]),2)+pow(fabs(part[y][1]-jet[z][1]),2)))
			if dR < dm:
				dm = dR
	hh.Fill(dm)
	
#hh.SetLineColor(R.kBlue)
#hh.SetFillColor(R.kBlue)
#hh.SetXTitle("deltaR")
##hh.SetYTitle("deltaR")
##hh.GetYaxis().SetTitleOffset(1)
##
##
hh.Draw("box")
#t.Draw("nGenJet:sqrt((GenJet_eta-GenPart_eta*Sum$(abs(GenPart_pdgId)==5))**2+(fmod(GenJet_phi+2*pi,2*pi)-fmod(GenPart_phi*Sum$(abs(GenPart_pdgId)==5)+2*pi,2*pi))**2)>>hh",cut) 
#ev = hh.GetEntries()
#print("--------------------------")
#print("accepted","Events","Acceptance (%)")
#print(ev,evnumber,float(ev)/float(evnumber)*100)
#    
