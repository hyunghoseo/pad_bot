import urllib2

leader_url = 'https://www.padherder.com/api/leader_skills/'
active_url = 'https://www.padherder.com/api/active_skills/'
monster_url = 'https://www.padherder.com/api/monsters/'


leader_req = urllib2.Request(leader_url, headers={'User-Agent' : 'Magic Browser'})
leader_con = urllib2.urlopen( leader_req )

active_req = urllib2.Request(active_url, headers={'User-Agent' : 'Magic Browser'})
active_con = urllib2.urlopen( active_req )

monster_req = urllib2.Request(monster_url, headers={'User-Agent' : 'Magic Browser'})
monster_con = urllib2.urlopen( monster_req )


leader_skills = leader_con.read()
active_skills = active_con.read()
monsters = monster_con.read()


leader_f = open('leader_skills.txt','w')
leader_f.write(leader_skills)
leader_f.close()

active_f = open('active_skills.txt','w')
active_f.write(active_skills)
active_f.close()

monster_f = open('monsters.txt','w')
monster_f.write(leader_skills)
monster_f.close()