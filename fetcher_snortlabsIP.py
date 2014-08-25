import requests
import re
from pymemcache.client import Client

feedaddr = 'http://labs.snort.org/feeds/ip-filter.blf'
feedID = 'snortlabs'
mkey = 'fetcher_snortlabsIP:feeddata'
killchain = 'unknown'

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
	if len(x) == 0: continue
	print("%s,%s,%s,%s" % (x, feedID, killchain, 'Included in the Snort labs IP filter list'))
	
