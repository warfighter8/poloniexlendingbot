import argparse, subprocess, csv, sys, os

parser = argparse.ArgumentParser()
parser.add_argument("-user", "--username", help="Username of user taking action")
parser.add_argument("-start", "--startbot", help="Start the bot", action="store_true")
parser.add_argument("-stop", "--stopbot", help="Stop the bot", action="store_true")
parser.add_argument("-set", "--setvalue", help="Set an acct value ex: mindailyrate:0.0031")
parser.add_argument("-new", "--newuser", help="Create new user with api key")
args = parser.parse_args()

open('users.csv', mode='a') #Create if does not exist
def userexists(username):
	with open('users.csv', mode='r') as userscsv:
		reader = csv.reader(userscsv)
		users = list(rows[0] for rows in reader)
	if username in users:
		return True
	else:
		return False

if args.newuser and args.username: #Create a new user in the CSV with some default values.
	if userexists(args.username) == False:
		userscsv = open('users.csv', mode='a')
		userscsv.write("%s,%s,<secret>,0.0031,2,3,10,200,.2,0.001\n" %(args.username, args.newuser))
		userscsv.close()
		sys.exit(0)
	else:
		print "User already exists..."
		sys.exit(0)

if args.startbot and args.stopbot or args.startbot and args.setvalue or args.stopbot and args.setvalue: #Only one command at a time
	print "You can't do that."
	sys.exit(0)

#Manage users.csv
#users.csv is organized as follows:
csvorder = ["username", "apikey", "apisecret", "mindailyrate", "maxdailyrate", "spreadlend", "gapbottom", "gaptop", "sixtydaythreshold", "minloansize"]
#json and sleep related settings are not available in users.csv because those are handled by the master manager

with open('users.csv', mode='r') as userscsv:
	reader = csv.reader(userscsv)
	users = list(rows[0] for rows in reader)
if args.username in users:
	#Set values related to username
	usernum = users.index(args.username)#Find row number of user.
	with open('users.csv', mode='r') as userscsv:
		reader = csv.reader(userscsv)
		details = list(row for row in reader)
		userdetails = details[usernum]
		#Now assign values
		settings = dict([('apikey', userdetails[1]), ('apisecret', userdetails[2]), ('mindailyrate', userdetails[3]), ('maxdailyrate', userdetails[4]), ('spreadlend', userdetails[5]), ('gapbottom', userdetails[6]), ('gaptop', userdetails[7]), ('sixtydaythreshold', userdetails[8]), ('minloansize', userdetails[9])])
	#Now execute commands
	if args.startbot: #TODO allow stopping by starting bot with an ID? could use occasional updates from a json file, if true continue if false stop
		#subprocess.Popen(["rm","-r","lendingbot.py"])
		os.system("python lendingbot.py -key %s -secret %s -minrate %s -maxrate %s -spread %s -gapbot %s -gaptop %s -60day %s -minloan %s -json www/%s_botlog.json -jsonsize 100 -sleepactive 60 -sleepinactive 300" %(settings['apikey'], settings['apisecret'], settings['mindailyrate'], settings['maxdailyrate'], settings['spreadlend'], settings['gapbottom'], settings['gaptop'], settings['sixtydaythreshold'], settings['minloansize'], args.username))
	if args.stopbot: #TODO be able to stop running bots by username/ID
		pass
	if args.setvalue: #Takes args in the form variable:value and updates the csv with them, one at a time.
		setting = args.setvalue.split(":")
		if setting[0] in csvorder:
			in_file = open("users.csv", "r")
			reader = csv.reader(in_file)
			rows = []
			for row in reader:
				if row[0] == args.username:
					row[csvorder.index(setting[0])] = str(setting[1])
				rows.append(row)
			in_file.close()
			with open("users.csv", "wb") as f:
				writer = csv.writer(f)
				writer.writerows(rows)	
else:
	print "User not found."
	sys.exit(0)
		
