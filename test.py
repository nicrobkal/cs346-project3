import os

#from subprocess import call

#topic="First_Post"
#username="nicrobkal@gmail.com"
#bashCommand = """mail -s "%s Posted in Topic %s!" "%s" < /dev/null""" % (username,topic,username)
#process = subprocess.call(bashCommand)
#output, error = process.communicate()

os.system('mail -s "nicrobkal@gmail.com Posted in Topic First_post!" "nicrobkal@gmail.com" < /dev/null')

#call('mail -s "nicrobkal@gmail.com Posted in Topic First_post!" "nicrobkal@gmail.com" < /dev/null'.split())
