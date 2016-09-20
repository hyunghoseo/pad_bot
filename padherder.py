import os
from monsters import *
from active_skills import *
from leader_skills import *
from elements import *
from awakenings import *
from types1 import *
from sheet import *

teamSize = 6

def getMonster(numID):
	monster = next((item for item in monsters if item["id"] == numID), None)
	if monster is None:
		return None
	return monster

def getMonsterID(d, info):
	x = None
	if d == None or d == "name" or d == "beach" or d == "academy" or d == "school" or d == "lead":
		x = None
	else:
		
		try:
			x = int(info)
		except ValueError:
			
			try:
				x = int(dump[d])
			except KeyError:
				monster = next((item for item in monsters if ((item["name"]).lower()).translate(None, '.') == d), None)
				if monster != None:
					x = monster["id"]
				else:
					if len(d) >= 4:
						matching = [s for s in dumplist if s.startswith(d)]
						if len(matching) > 0:
							x = int(dump[matching[0]])
						else:
							monsterm = [item for item in monsters if item["name"].lower().startswith(d)]
							if len(monsterm) == 1:
								monster = monsterm[0]
								x = monster["id"]
							else:
								x = None
	return x

def getIcon(num):
	s = num/200
	c = num%200

	S = "%02d"%s
	C = "%03d"%c
	N = str(num)
	return "(http://puzzledragonx.com/en/monster.asp?n=" + str(num) + "#I/S" + S + "/C" + C + "/" + N + ")"

def getSite(num):
	if num == 0:
		return ''
	return "(http://puzzledragonx.com/en/search.asp?q=" + str(num) + ")"


def createInfo(numID):
	monster = getMonster(numID)
	if monster is None:
		return None;
	
	site = getSite(numID)
	info = ""
	ID = 'No.'
	Name = ''
	Elements = ''
	Types = ''
	Rarity = '&#9733; '
	Cost = 'Cost: '
	Stats = ''
	Awoken = 'Awakenings: '
	Leader = 'LS: None'
	Active = 'AS: None'


	def m(att):
		return (monster[att])
	def ms(att):
		return str(m(att))
	def awk(num):
		awk = next((item for item in awakenings if item["id"] == num), None)
		if awk == None:
			return "unknown"
		return "[" + awk["short"] + "]" + awk["icon"]


	ID += ms("id")
	Name += ((ms("name").decode('unicode-escape')).encode("utf-8"))
	Rarity += ms("rarity")
	Cost += ms("team_cost")

	Elements =  elements[monster["element"]]
	if monster[	"element2"] != None:
		Elements += " / " + elements[monster["element2"]]
	Elements = "[" + Elements + "]" + getIcon(numID)

	Types = types[monster["type"]] 
	if monster["type2"] != None:
		Types += " / " + types[monster["type2"]]
	if monster["type3"] != None:
		Types += " / " + types[monster["type3"]]

	level = m("max_level")
	hp = m("hp_max")
	atk = m("atk_max")
	rcv = m("rcv_max")
	weighted = '%.2f' %  (float(hp)/10 + float(atk)/5 + float(rcv)/3)

	Stats = "Lv. " + str(level) + " &nbsp; HP " + str(hp) + " &nbsp; ATK " + str(atk) + " &nbsp; RCV " + str(rcv) + " &nbsp; Weighted " + str(weighted)

	e = monster["awoken_skills"]
	e.sort()

	prev = 0
	count = 1
	for i in range(0, len(e)+1):
		if i == len(e):
			a = 0
		else:
			a = e[i]
		if prev == a:
			count += 1
		else :
			if prev != 0:
				Awoken += awk(prev) + "x" + str(count) + " "
				count = 1
		prev = a

	if Awoken == "Awakenings: ":
		Awoken += "None"

	LS = next((item for item in leader_skills if item["name"] == monster["leader_skill"]), None)
	if LS != None:
		Leader = "LS: " + LS["effect"]

	AS = next((item for item in active_skills if item["name"] == monster["active_skill"]), None)
	if AS != None:
		Active = "AS (" + str(AS["max_cooldown"]) + "->" + str(AS["min_cooldown"]) + "): " + AS["effect"]

	info = "* " + ID + " [**" + Name + "**]" + site + "    \n" + Elements + " | " + Types + " | " + Rarity + " | " + Cost + "    \n" + Stats + "    \n" + Awoken + "    \n" + Leader + "    \n" + Active
	return info

def createTeam(t):
	t = t.replace(' :', ':')
	t = t.replace(': ', ':')
	team = t[t.find(':')+1:]
	team = team.replace(' /', '/')
	team = team.replace('/ ', '/')
	print team
	count = 0
	teamlist = []
	while (team.find('/') != -1):
		a = team[0:team.find('/')]
		teamlist.insert(count, a)
		team = team[team.find('/')+1:]
		count += 1
	teamlist.insert(count, team)
	count += 1
	while (count < 6):
		teamlist.insert(count, '')
		count += 1
	
	count = 0
	myTeam = ""
	for i in range(0, 6):
		monID = getMonsterID(str(teamlist[i]), teamlist[i])
		print monID
		name = ""
		mon = getMonster(monID)
		
		if mon == None:
			monID = 0
			name = "Flex"
			monster = "[" + name + "]" + getIcon(monID)
			count += 1
		else:
			name = ((str(mon["name"])).decode('unicode-escape')).encode("utf-8")
			monster = "[[" + name + "]" + getIcon(monID) + "]" + getSite(monID)
		myTeam += monster
		if i == 0 or i == 4:
			myTeam += " | "
		else:
			if i != 5:
				myTeam += "|"
	
	if count == 6:
		return None
	return myTeam

			

