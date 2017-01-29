from __future__ import print_function
from Workspace.HEPHYPythonTools.xsecSMS import stop13TeV_NLONLL
import os, pickle
import ROOT as R
from math import *
import glob
ev = 0
evnumber = 0
cut1 = 0
cut2 = 0
cut3 = 0
cut4 = 0
cut5 = 0
cut6 = 0
cut7 = 0
cut8 = 0
cut9 = 0
cut10 = 0
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


#Variables
lepton = range(11,14,2)
hadron = range(1,7)
print("read files")
#read files

t = R.TChain("tree")
t.Add("/afs/hephy.at/user/m/mwinder/public/singlelepton/tree.root")

#Preselection and Selection
nEvents = t.GetEntries()
print("calculation started")
for ievt in xrange(nEvents):
	t.GetEntry(ievt)
	evnumber += 1
	if (evnumber and not evnumber%10000): print("analyzed",evnumber)	
#CT1 > 200
	ISR = 0
	ct1 = 0.
	anzjet = 0
	phijet = []
	vetob = 0
	for x in xrange(t.nGenJet):
		if t.GenJet_pt[x] > 100 and abs(t.GenJet_eta[x]) < 2.4:
			ISR +=1
		if abs(t.GenJet_eta[x]) < 2.4 and t.GenJet_pt[x] > 30: 
			ct1 += float(t.GenJet_pt[x])
		if t.GenJet_pt[x] > 60 and abs(t.GenJet_eta[x]) < 2.4:
			anzjet += 1
			phijet.append(float(t.GenJet_phi[x]))
		if t.GenJet_bMatched[x] == 1 and t.GenJet_pt[x] > 30 and abs(t.GenJet_eta[x]) < 2.4:
			vetob += 1
	if ISR == 0:
		continue	
	if min(t.GenMET_pt,ct1-100) <= 200:
		continue
	cut1 += 1
#dphi
	if anzjet >= 2 and acos(cos(phijet[0]-phijet[1])) >= 2.5:
		continue
	cut2 += 1 
#3rd Hard Jet veto
	if anzjet > 2:
		continue
	cut3 += 1
#Particles
	tau1 = 0
	tau2 = 0
	lep = 0
	lep20 = 0	
	lepeta = 0
	leppt = 0
	charge = 0
	for x in xrange(t.nGenPart):
		if abs(t.GenPart_pdgId[x]) == 15 and t.GenPart_pt[x] > 20:
			tau1 += 1
		if abs(t.GenPart_motherId[x]) == 15 and abs(t.GenPart_pdgId[x]) in lepton:
			tau2 += 1
		if abs(t.GenPart_pdgId[x]) in lepton and t.GenPart_pt[x] > 5 and abs(t.GenPart_eta[x]) < 2.4:
			lep += 1
		if abs(t.GenPart_pdgId[x]) in lepton and t.GenPart_pt[x] > 20 and abs(t.GenPart_eta[x]) < 2.4:
			lep20 += 1
		if abs(t.GenPart_pdgId[x]) in lepton and t.GenPart_pt[x] > 5 and abs(t.GenPart_eta[x]) < 1.5:
			lepeta += 1
		if abs(t.GenPart_pdgId[x]) in lepton and t.GenPart_pt[x] > 5 and t.GenPart_pt[x] < 30 and abs(t.GenPart_eta[x]) < 1.5:
			leppt += 1
		if abs(t.GenPart_pdgId[x]) in lepton and t.GenPart_pt[x] > 5 and t.GenPart_pt[x] < 30 and abs(t.GenPart_eta[x]) < 1.5 and t.GenPart_charge[x] < 0:
			charge += 1

	if tau1 != 0 and tau2 == 0:
		continue
	cut4 += 1
	if lep == 0:
		continue
	if lep20 > 2:
		continue
	cut5 += 1	
	if min(t.GenMET_pt,ct1-100) <= 300:
		continue
	cut6 += 1
	if vetob != 0:
		continue
	cut7 += 1
	if lepeta == 0:
		continue
	cut8 += 1
	if leppt == 0:
		continue
	cut9 += 1
	if charge == 0:
		continue
	cut10 += 1


#Prints
print("--------------------------------------")
print("Events","Acceptance [%]","T2tt-300-270","reduction")
print(cut1,float(cut1)/float(evnumber)*100,float(cut1)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,1.0)
print(cut2,float(cut2)/float(evnumber)*100,float(cut2)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut2)/float(cut1))
print(cut3,float(cut3)/float(evnumber)*100,float(cut3)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut3)/float(cut2))
print(cut4,float(cut4)/float(evnumber)*100,float(cut4)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut4)/float(cut3))
print(cut5,float(cut5)/float(evnumber)*100,float(cut5)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut5)/float(cut4))
print(cut6,float(cut6)/float(evnumber)*100,float(cut6)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut6)/float(cut5))
print(cut7,float(cut7)/float(evnumber)*100,float(cut7)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut7)/float(cut6))
print(cut8,float(cut8)/float(evnumber)*100,float(cut8)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut8)/float(cut7))
print(cut9,float(cut9)/float(evnumber)*100,float(cut9)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut9)/float(cut8))
print(cut10,float(cut10)/float(evnumber)*100,float(cut10)/float(nEvents)*stop13TeV_NLONLL[300]*12.9*10**3,float(cut10)/float(cut9))
