#!/usr/bin/python

import codecs

import praw
import pdb
import re
import os
import time
from config_bot import *
from padherder import *
from sheet import *

codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None)

# Create the Reddit instance
user_agent = ("pad_linker 0.3")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
	# Read the file into a list and remove any empty values
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = filter(None, posts_replied_to)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("comments_replied_to.txt"):
	comments_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
	# Read the file into a list and remove any empty values
	with open("comments_replied_to.txt", "r") as f:
		comments_replied_to = f.read()
		comments_replied_to = comments_replied_to.split("\n")
		comments_replied_to = filter(None, comments_replied_to)

# Get the top 5 values from our subreddit
subreddit = r.get_subreddit('PuzzleAndDragons')

def createReply(a):
	post = a
	reply = ""
	info = []
	count = 0
	xlist = []
	while (post.find("[[") != -1):
		a = post[post.find("[[")+2:post.find("]]")]
		info.insert(count, a)
		post = post[post.find("]]")+2:]
		count += 1

	count = 0
	for i in range(0, len(info)):
		x = None
		try:
			d = str(info[i])
			d = d.lower()
			d = d.translate(None, '.')
		except UnicodeEncodeError:
			d = "name"
		if d == None or d == "name" or d == "beach" or d == "academy" or d == "school":
			x = None
		else:
			
			try:
				x = int(info[i])
			except ValueError:
				
				try:
					x = int(dump[d])
				except KeyError:
					monster = next((item for item in monsters if (item["name"]).lower() == d), None)
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
		print x
		if x != None and x not in xlist:
			theInfo = createInfo(x)
			if theInfo != None:
				reply += theInfo
				reply += "\n\n-----------------------\n"
				count += 1
				xlist.insert(0, x)
		if count == 7:
			break
	if reply == "":
		return None
	reply += "\n\n^Call ^me ^with ^up ^to ^7 ^monster ^[[id]] ^or ^[[name]]. ^Contact ^my ^owner **[^here](https://www.reddit.com/message/compose/?to=hihoberry)**^.    \n^Submit ^a ^nickname ^suggestion **[^here](https://docs.google.com/forms/d/1kJH9Q0S8iqqULwrRqB9dSxMOMebZj6uZjECqi4t9_z0/edit)**^."
	return reply

numLimit = 200
while True:
	for submission in subreddit.get_new(limit=numLimit):
		# If we haven't replied to this post before
		if submission.id not in posts_replied_to:
			
			# self = submission.selftext
			# Do a case insensitive search
			if re.search("]]", submission.selftext):
				print submission.title
				reply = createReply(submission.selftext)
				if reply != None:
					# Reply to the post
					submission.add_comment(reply)
					print "Bot replied to : ", submission.id

				# Store the current id into our list
				posts_replied_to.append(submission.id)

	for comment in subreddit.get_comments(limit=numLimit):
		if str(comment.author) != 'pad_bot' and comment.id not in comments_replied_to:
			
			if re.search("]]", comment.body):
				print comment.id + ":" + comment.body
				reply = createReply(comment.body)
				if reply != None:
					# Reply to the comment
					comment.reply(reply)
					print "Bot replied to : ", comment.id

				# Store the current id into our list
				comments_replied_to.append(comment.id)

	# Write our updated list back to the file
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")

	with open("comments_replied_to.txt", "w") as f:
		for comment_id in comments_replied_to:
			f.write(comment_id + "\n")
	numLimit = 10
	time.sleep(10)
