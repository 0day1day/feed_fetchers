import requests
import re
from pymemcache.client import Client

# User defined variables
feedaddr = 'http://cybercrime-tracker.net/all.php'
feedID = 'cybercrime_tracker'
mkey = 'fetcher_cybercrime_trackerDomain:feeddata'
killchain = 'Command & Control'

# No user modifications needed below.
client = Client(('localhost', 11211))
result = client.get(mkey)

if isinstance(result, str):
	splitlines = result.split('<br />')
else:
	r = requests.get(feedaddr)
	client.set(mkey, r.content, expire=7200)
	splitlines = r.content.split('<br />')

seen = []

print('domain,feedID,killchain,description')

for x in splitlines:
	x = x.strip()
	if re.search('^#', x): continue
	if len(x) == 0: continue
	x = re.sub('\/.*$', '', x)
	x = re.sub('\:.*$', '', x)
	x = re.sub(' .*$', '', x)
	if not re.search('[a-zA-Z]', x): continue
	if x in seen: continue
	seen.append(x)
	print("%s,%s,%s,%s" % (x, feedID, killchain, 'C&C Control Panel'))
	
