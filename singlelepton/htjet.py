def htjet(genpart,jetht,eta):
	global Ht
	Ht = 0
	global ISR
	ISR = 0
	for x in xrange(genpart):
                if jetht[x] > 30 and abs(eta[x]) < 2.4:
              		Ht += jetht[x]
	   	if jetht[x] > 100 and abs(eta[x]) < 2.4:
			ISR += 1      
