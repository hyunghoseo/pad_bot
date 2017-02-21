import ast

f = open("leader_skills.txt","r")
leader_skills = ast.literal_eval(f.read())

f = open("monsters.txt","r")
monsters = ast.literal_eval(f.read())

f = open("active_skills.txt","r")
active_skills = ast.literal_eval(f.read())