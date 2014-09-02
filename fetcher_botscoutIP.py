import requests
import re
from datetime import date, timedelta

feedaddr = 'http://botscout.com/last_caught_cache.htm'
feedID = 'botscout'
killchain = 'Reconnaissance'

r = requests.get(feedaddr)
splitlines = r.content.split('\n')

print('ipv4,feedID,killchain,description')

if r.status_code != 200: exit()
for x in splitlines:
	x = x.strip()
	if not re.search('ipcheck', x): continue
	x = re.sub('^.*\"\>', '', x)
	x = re.sub('\<\/.*$', '', x)
	if re.search('[a-zA-Z]', x): continue
	if len(x) > 0:
		print("%s,%s,%s,%s" % (x, feedID, killchain, 'Botscout malicious IP source'))
	
