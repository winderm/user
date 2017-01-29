import sys, os, copy
import math, re, array, gzip
from xml.dom import minidom
from ROOT import *

filename = sys.argv[1]
outfile = sys.argv[2]

#useful class to describe 4 momentum
class Momentum:
    def __init__(self,px,py,pz,E,m):
        self.px=px
        self.py=py
        self.pz=pz
        self.E=E
        self.m=m
    def __add__(self,other):
        t=Momentum(self.px+other.px,self.py+other.py,self.pz+other.pz,self.E+other.E,0)
        t.m=t.calcMass()
        return t
    def __sub__(self,other):
        t=Momentum(self.px-other.px,self.py-other.py,self.pz-other.pz,self.E-other.E,0)
        t.m=t.calcMass()
        return t
    def calcMass(self):
        tempMass2=self.E**2-self.px**2-self.py**2-self.pz**2
        if tempMass2 > 0:
            t=math.sqrt(tempMass2)
            if t>toler:
                return t
            else:
                return 0
        else:
            return 0
    def boost(self,ref,rdir):
        pmag=ref.E
        DBX=ref.px*rdir/pmag
        DBY=ref.py*rdir/pmag
        DBZ=ref.pz*rdir/pmag
        DB=math.sqrt(DBX**2+DBY**2+DBZ**2)
        DGA=1.0/math.sqrt(1.0-DB**2)        
        DBP=DBX*self.px+DBY*self.py+DBZ*self.pz
        DGABP=DGA*(DGA*DBP/(1.0+DGA)+self.E)
        self.px = self.px+DGABP*DBX
        self.py = self.py+DGABP*DBY
        self.pz = self.pz+DGABP*DBZ
        self.E  = DGA*(self.E+DBP)
    def reScale(self,pi,po):
        self.px = self.px/pi*po
        self.py = self.py/pi*po
        self.pz = self.pz/pi*po
    def printMe(self):
        li = [self.px,self.py, self.pz, self.E, self.m]
        print "| %18.10E %18.10E %18.10E %18.10E %18.10E |" % tuple(li)    

#useful class to describe a particle
class Particle:
    def __init__(self,i,l):
        self.no = i
        self.id = l[0]
        self.status = l[1]
        self.mo1 = l[2]
        self.mo2 = l[3]
        self.co1 = l[4]
        self.co2 = l[5]
        self.mom = Momentum(l[6],l[7],l[8],l[9],l[10])
        self.life = l[11]
        self.polar = l[12]
    def printMe(self):
        li = [self.no, self.id, self.status,self.mo1, self.mo2, self.co1, self.co2, self.mom.px,self.mom.py, self.mom.pz, self.mom.E, self.mom.m, self.life, self.polar]
        print "%2i | %9i | %4i | %4i %4i | %4i %4i | %18.10E %18.10E %18.10E %18.10E %18.10E | %1.0f. %2.0f" % tuple(li)
    def writeMe(self):
        li = [self.id, self.status,self.mo1, self.mo2, self.co1, self.co2, self.mom.px,self.mom.py, self.mom.pz, self.mom.E, self.mom.m, self.life, self.polar]
        return "%9i %4i %4i %4i %4i %4i %18.10E %18.10E %18.10E %18.10E %18.10E  %1.0f. %2.0f\n" % tuple(li)        

#useful function for converting a string to variables
def parseStringToVars(input):
    if input.find(".")>-1 :
        return float(input)
    else:
        return int(input)

def getEventList(inname):
    f = gzip.open(inname)
    try:
	xmldoc = minidom.parse(f)
    except IOError:
	print " could not open file for xml parsing ",f.name
	sys.exit(0)
    f.close()
    return xmldoc.getElementsByTagName('event')
    
def getEvent(lines):
    slines = lines.split("\n")
    next = 0
    nup = 0
    nlines = len(slines)
    counter = 0
    event = []
    event_description=""
    event_poundSign=""

    while counter<nlines:
        s=slines[counter]
        if s.find("<event>")>-1:
            next=1
        elif s.find("</event>")>-1:
            pass
        elif s.find("<")>-1:
            pass
        elif s.find("#")>-1:
            event_poundSign=s
        elif next==1:
            event_description=s
            next=0
        else:
            t=[]
            for l in s.split(): t.append(parseStringToVars(l))
            nup = nup+1
            event.append(Particle(nup,t))
#	    event[nup-1].printMe()
        counter=counter+1
    return [event, event_description, event_poundSign]
    
def getIndex(ev, pid):
    for ip, p in enumerate(ev):
        if(p.id == pid):
	    return ip
#    print "did not find", pid, "in event"
    return -1
    
###
varcountmax = '30'
varcount = 'npar'
varsI = ['no','id','status','mo1','mo2','co1','co2','polar']
varsD = ['pt','eta','phi','mass']
structString = "struct lhe_t { "
structString += "Int_t nevent;"
structString += "Int_t "+varcount+";"
for var in varsI:
  structString += "Int_t "+var+"["+varcountmax+"];"
for var in varsD:
  structString += "Double_t "+var+"["+varcountmax+"];"
structString += " };"

gROOT.ProcessLine(structString)
lhe = lhe_t()
f = TFile( outfile, 'RECREATE' )
t = TTree( 't', '' )
t.Branch('nevent', AddressOf(lhe,'nevent'), 'nevent/I' )
t.Branch(varcount, AddressOf(lhe,varcount), varcount+'/I' )
for var in varsI:
    t.Branch(var, AddressOf(lhe,var), var+'['+varcount+']/I' )
for var in varsD:
    t.Branch(var, AddressOf(lhe,var), var+'['+varcount+']/D' )

###
	

reflist = getEventList(filename)
    

n = len(reflist)
print n

for i in range(0,n):

    if(i>0 and (i%10000)==0): print i
#    print i
    
    [eventP, eventDS, eventPS] = getEvent(reflist[i].toxml())

    lhe.nevent = i
    lhe.npar = len(eventP)
    for ip,parton in enumerate(eventP):
#        parton.printMe()
        for var in varsI:
            exec('lhe.'+var+'[ip] = parton.'+var)
        if parton.mom.px==0.: parton.mom.px = 1e-4
        if parton.mom.py==0.: parton.mom.py = 1e-4
        aux = TLorentzVector(parton.mom.px,parton.mom.py,parton.mom.pz,parton.mom.E)
#        parton.printMe()
        lhe.pt[ip] = aux.Pt()
        lhe.phi[ip] = aux.Phi()
        lhe.eta[ip] = aux.Eta()
        lhe.mass[ip] = aux.M()
    t.Fill()
     
t.Write()

        
