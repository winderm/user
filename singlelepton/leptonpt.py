def leptonpt(pdgid,pt,lepton,eta):
	global nlep
	nlep = 0
	global nlep20
	nlep20 = 0	
	global nb
	nb = 0
	for x in xrange(len(t.GenPart_pdgId)):
		if abs(pdgid[x]) in lepton and pt[x] > 5 and pt[x] < 30 and abs(eta[x]) < 2.4:	
			nlep += 1
			if pt[x] >= 20:
				nlep20 += 1	
		if abs(pdgid[x]) == 5 and pt[x] > 30 and pt[x] < 60  and abs(eta[x]) < 2.4:
			nb += 1			


