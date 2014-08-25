import requests
import re
from pymemcache.client import Client

feedaddr = 'http://www.chaosreigns.com/iprep/iprep.txt'
feedID = 'chaosreigns'
mkey = 'fetcher_chaosreignsIP:feeddata'

client = Client(('localhost', 11211))
result = client.get(mkey)

if isinstance(result, str):
	splitlines = result.split('\n')
else:
	r = requests.get(feedaddr)
	client.set(mkey, r.content, expire=7200)
	splitlines = r.content.split('\n')

print('ipv4,feedID,killchain,description')

for x in splitlines:
	x = x.strip()
	if re.search('^#', x): continue
	if re.search('\:', x): continue
	if len(x) == 0: continue
	xsplit = x.split()
	if xsplit[1] == '100':
		print("%s,%s,%s,%s" % (xsplit[0], feedID, 'unknown', 'Whitelisted email IP source'))
	else:
		print("%s,%s,%s,%s" % (xsplit[0], feedID, 'Delivery', 'Blacklisted email IP source'))
	
