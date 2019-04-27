#! /usr/bin/env python3

import cgi
import os

import cgitb
cgitb.enable(display=0, logdir="/var/log/httpd/cgi_err/")

import MySQLdb
import private_no_share_dangerous_passwords as pnsdp

from common import FormError

form = cgi.FieldStorage()

if "Username" not in form or "Text" not in form or "Topic" not in form or "OriginUsername" not in form:
     raise FormError("Invalid parameters: Username//Text//Topic//Original Username not in form")

topic = form["Topic"].value
username = form["Username"].value
originUsername = form["OriginUsername"].value
text = form["Text"].value

for c in topic+username:
     if c not in "_-@." and not c.isdigit() and not c.isalpha():
         raise FormError("Invalid parameters: The topic and username can only contains upper and lowercase character, digits, underscores, and hypens")

#connect to the database
conn = MySQLdb.connect(host   = pnsdp.SQL_HOST,
    port   = 3306,
    user   = pnsdp.SQL_USER,
    passwd = pnsdp.SQL_PASSWD,
    db     = pnsdp.SQL_DB)

cursor = conn.cursor()

#topic="First_Post"
#username="nicrobkal@gmail.com"
#originUsername="nicrobkal@gmail.com"
#text="Hello"

cursor.execute("""SELECT DISTINCT Username FROM Posts WHERE Topic='%s';""" % (topic))

active = []
for row in cursor.fetchall():
    active.append([row[0]])

bashCommand = """echo "Thank you" | mail -s "%s Posted in Topic %s" "%s" """ % (username,topic,username)
os.system(bashCommand)

cursor.execute("""INSERT INTO Posts(Topic,OriginUsername,Username,Text,Likes) VALUES("%s","%s","%s","%s","%d");""" % (topic,originUsername,username,text,0))

conn.commit()
cursor.close()
conn.close()

try:
    print("Status: 303 See other")
    print("""Location: http://%s/cgi-bin/project3/conversation.py?Topic=%s&Username=%s""" % (pnsdp.WEB_HOST, topic, originUsername))
    print()

except FormError as e:
    print("""Content-Type: text/html;charset=utf-8
<html>
<head><title>ERROR FORM</title></head>
<body>
<p>ERROR: %s
<p><a href="list.py">Return to conversation list</a>
</body>
</html>
""" % e.msg, end="")

except:
    print("""Content-Type: text/html;charset=utf-8\n\n""")

    raise
