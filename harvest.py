import json,sys,optparse,argparse,re
from urllib.request import build_opener
from unidecode import unidecode
# macOS brew python hack
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

parser = argparse.ArgumentParser(description='Creates email addresses with optional formatters from names of employees of a company on LinkedIn.')
parser.add_argument('COMPANY', 
                    help='Company ID')
parser.add_argument('DOMAIN',
                    help='Domain to be used in email address')
parser.add_argument('COOKIE',
                    help='Cookie file',metavar="FILE")

parser.add_argument("-o", "--output",
                  default='emails.txt',
                  help="path to output text file for emails")

parser.add_argument("-f", 
                  action="store_true", dest="abbrevF", default=False,
                  help="abbreviate first name")

parser.add_argument("-l",
                  action="store_true", dest="abbrevL", default=False,
                  help="abbreviate last name")

parser.add_argument("-s",
                  action="store_true", dest="swap", default=False,
                  help="switch order of first and last names")
'''
#TODO:
## other possible email transformations:
### remove/include:
#### initials ([A-Z]\.)
#### roman numerals
#### hyphens
### additional permutations
### use nicknames in (.*) 
'''

args = parser.parse_args()

company_id = args.COMPANY
domain = args.DOMAIN
csrf_token = ''
session_id = ''

#get cookies
f = open(args.COOKIE,"r")
content = f.readlines()
csrf_token = content[0][:-1] #removes newline
session_id = content[1][:-1] #removes newline
f.close()

cookie1 = 'li_at='+session_id
cookie2 = 'JSESSIONID='+csrf_token

emails = []

last_page = False

creds='''AAMS
ACA
ADPA
AIF
AWMA
CAIA
CAP
CDFA
CEP
CFA
CFP
ChFC
CIMA
CLU
CPA
CMA
CMM
CMP
CDFA
CPWA
CRPC
CRPS
CTP
CWS
Jr.
MBA
M.A.
RICP
Sr.
WMS'''.split('\n')

def format_name(orig):
    orig = unidecode(orig)
    m = re.match(r'\s*(?:(?:(?:[\x80-\xff]|\)(?:[Rr]|[Tt][Mm])\()?(?:%s),?)+|[^,]+,)*\s*([A-Za-z \-\.\'\(\)]+)\s*'%('|'.join([x[::-1] for x in creds])), orig[::-1])
    if not m:
        print('unexpected format for %s' % orig)
    name = m.group(1)[::-1]

    # for now, remove
    ## paren content
    ## initials (only if -f, -l not specified)
    ## all non local email chars
    final = re.subn(r'(\(.*\)%s|[-\'\.,\\])' % (r'|[A-Z]\.' if (not args.abbrevF and not args.abbrevL) else ''), '', name)[0].lower().split(' ')
    email = '.'.join([f for f in final if len(f)>0]) + '@' + domain
    #print('%50s -> %40s -> %50s -> %40s'%(orig,name,final,email))
    
    return email

def harvest(curr):
    global last_page

    url = ("https://www.linkedin.com/voyager/api/search/blended?"
    "count=49&origin=OTHER&queryContext=List(spellCorrectionEnabled-%3Etrue,"
    "crelatedSearchesEnabled-%3Etrue,kcardTypes-%3EPROFILE%7CCOMPANY)&q=all&filters=List(currentCompany-%3E" + company_id + ",resultType-%3EPEOPLE)&start=" + str(curr))
    opener = build_opener()
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
        if args.abbrevF:
            fname = fname[0:1]
        if args.abbrevL:
            lname = lname[0:1]
        if args.swap:
            fullname = lname + ' ' + fname
        else:
            fullname = fname + ' ' + lname

        email = format_name(fullname)
        emails.append(email)

curr = 0
while not last_page:
    harvest(curr)
    curr = curr + 49


f = open(args.output,"w+")
count = len(emails)
for i in emails:
   try:
      f.write('%s\n'%i)
   except:
      print('error writing one email ("%s") due to strange character'%i)
    

f.close()

print("Done! " + str(count) + " emails have been written to %s" % args.output)
      
