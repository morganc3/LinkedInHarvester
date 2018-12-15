import json,urllib2,sys

if(len(sys.argv) != 4):
	print("Usage: python harvest.py <COMPANY ID> <DOMAIN> <COOKIE FILE>")
	exit()

company_id = sys.argv[1]
domain = sys.argv[2]
csrf_token = ''
session_id = ''

#get cookies
f = open(sys.argv[3],"r")
content = f.readlines()
csrf_token = content[0][:-1] #removes newline
session_id = content[1][:-1] #removes newline
f.close()

cookie1 = 'li_at='+session_id
cookie2 = 'JSESSIONID='+csrf_token

emails = []

last_page = False

def format_name(name):
	name = name.lower()
	#remove apostrophes and periods from names
	name = name.replace('\'','')
	name = name.replace('.','')
	name = name.replace(',','')
	name = name.replace('(','')
	name = name.replace(')','')

	name = name.replace(' ', '.')
	email = name + '@' + domain + '\n'
	return email

def harvest(curr):
	global last_page

	url = ("https://www.linkedin.com/voyager/api/search/blended?"
	"count=49&origin=OTHER&queryContext=List(spellCorrectionEnabled-%3Etrue,"
	"crelatedSearchesEnabled-%3Etrue,kcardTypes-%3EPROFILE%7CCOMPANY)&q=all&filters=List(currentCompany-%3E" + company_id + ",resultType-%3EPEOPLE)&start=" + str(curr))
	opener = urllib2.build_opener()
	opener.addheaders.append(('csrf-token', csrf_token))
	opener.addheaders.append(('Cookie', cookie1 + ';' + cookie2))
	opener.addheaders.append(('x-restli-protocol-version', '2.0.0'))
	response = opener.open(url)

	data = json.load(response)
	data = data["elements"][0]
	data = data["elements"]

	if len(data) != 49:
		last_page = True
	
	for employee in data:
		employee = employee["image"]
		employee = employee["attributes"]
		employee = employee[0]
		employee = employee["miniProfile"]
		fname = employee["firstName"]
		lname = employee["lastName"]
		fname = fname.replace(' ', '')
		lname = lname.replace(' ', '')
		if fname == "":
			continue

		fullname = fname + ' ' + lname
		email = format_name(fullname)
		emails.append(email)

curr = 0
while not last_page:
	harvest(curr)
	curr = curr + 49


f = open('./emails.txt',"w+")
count = len(emails)
for i in emails:
	f.write(i)

f.close()

print("Done! " + str(count) + " emails have been written to ./emails.txt")
      


