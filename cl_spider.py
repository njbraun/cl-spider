#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser
import os.path
import smtplib

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login("njbraun","<PASSWORDHERE>")

parsed_root = feedparser.parse('http://seattle.craigslist.org/search/apa/see?maxAsk=1500&query=garage|underground|secured%20patio|porch|balcony%20-2br%20-%22Promenade%20at%20the%20Park%22%20-studio%20-%22west%20seattle%22&srchType=A&format=rss')

found_items = []

if os.path.exists("./found.txt"):
	
	found_file = open("./found.txt", "r")
	# Read in found file to list
	for line in found_file:
		found_items.append(line.strip())
	found_file.close()

for item in parsed_root['items']:
	key = "%s | %s | %s" % (item['updated'], item['id'], item['title'])
	if found_items.count(key) == 0:
		# Notify
		message = "Subject: Apartment Found! - %s\n\n" % item['title']
		message += "%s\n\n%s" % (item['summary'], item['id'])
		#sendemail("Apartment Found! - "+item['title'], item['id'])
		try:
			server.sendmail("njbraun@gmail.com", ["njbraun@gmail.com"], message.encode("utf-8"))
		except:
			print("Unable to send email, ERROR!")
		# Store new item in found items
		found_items.append(key)
		
found_file = open("./found.txt", "w")
for item in found_items:
	found_file.write(item + "\n")
	
server.quit()

found_file.close()
