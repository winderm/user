import ROOT as R
t = R.TChain("tree")
t.Add("hephytree.root")
#t.Scan("evt:(GenJet_pt==Max$(GenJet_pt))*GenJet_phi:Max$(((GenJet_pt>60)*GenJet_pt&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi)")
#")
#t.Scan("acos(cos(Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt==Max$(GenJet_pt)&&Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))!=0))*GenJet_phi)*GenJet_phi)-Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi))):Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt==Max$(GenJet_pt))*GenJet_phi):Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi)")
t.Scan("evt:(GenJet_pt>60)*GenJet_pt:GenJet_phi*(GenJet_pt>60):acos(cos(Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt==Max$(GenJet_pt)&&Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi)!=0)*GenJet_phi)-Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi))):Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt==Max$(GenJet_pt))*GenJet_phi):Sum$((Sum$(GenJet_pt>60)<=2&&GenJet_pt>60&&GenJet_pt<Max$(GenJet_pt))*GenJet_phi)")
