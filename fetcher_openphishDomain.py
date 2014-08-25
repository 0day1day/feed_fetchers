import requests
import re
from pymemcache.client import Client

feedaddr = 'http://openphish.com/feed.txt'
feedID = 'openphish'
mkey = 'fetcher_openphish:feeddata'
killchain = 'Exploit'

client = Client(('localhost', 11211))
result = client.get(mkey)

if isinstance(result, str):
	splitlines = result.split('\n')
else:
	r = requests.get(feedaddr)
	client.set(mkey, r.content, expire=7200)
	splitlines = r.content.split('\n')

seen = []
	
print('domain,feedID,killchain,description')

for x in splitlines:
	x = x.strip()
	if re.search('^#', x): continue
	if len(x) == 0: continue
	xsplit = x.split('://')
	xsplit[1] = re.sub('\/.*$','',xsplit[1])
	if not re.search('[a-z,A-Z]', xsplit[1]): continue
	if not re.search('\.', xsplit[1]): continue
	if re.search('\.$', xsplit[1]): continue
	if xsplit[1] in seen: continue
	seen.append(xsplit[1])
	print("%s,%s,%s,%s" % (xsplit[1], feedID, killchain, 'Openphish malware pages'))
	
