import requests
import re
from pymemcache.client import Client

feedaddr = 'https://isc.sans.edu/feeds/suspiciousdomains_Low.txt'
feedID = 'isc_suspicious_low'
mkey = 'fetcher_isc_suspicious_low:feeddata'
killchain = 'unknown'

client = Client(('localhost', 11211))
result = client.get(mkey)

if isinstance(result, str):
	splitlines = result.split('\n')
else:
	r = requests.get(feedaddr)
	client.set(mkey, r.content, expire=7200)
	splitlines = r.content.split('\n')

print('domain,feedID,killchain,description')

for x in splitlines:
	x = x.strip()
	if re.search('^#', x): continue
	if len(x) == 0: continue
	if not re.search('[a-z,A-Z]', x): continue
	if not re.search('\.', x): continue
	print("%s,%s,%s,%s" % (x, feedID, killchain, 'ISC SANS suspicious domains LOW'))
	
