"""
The purpose of this program is to return the latency measured for each ISP in a given city as an argument. Atlas RIPE probes and anchors are used to make these measurements.
We use ping built-in measurements of Atlas RIPE. The set of built-in measurements contain ping mostly towards well-known targets such as DNS root servers,
but also towards some of the RIPE Atlas infrastructure components.

Args:
[1]:(string) Name of city and some info to help localisation
[3]:(string) Name,(float) latitude,(float) longitude *default radius is 100km
[4]:(string) Name,(float) latitude,(float) longitude, (int) radius in km

Output:
Writes the result to a json file with the name of the city.
"""

import subprocess
import requests
import json
import sys
import time
from statistics import mean

radius = 100 

#Parse args
if len(sys.argv) >= 4:
    city = sys.argv[1]
    latitude = sys.argv[2]
    longitude = sys.argv[3]
    if len(sys.argv) == 5:
        radius = sys.argv[4]
    else:
        print("Error: Bad number of argumetns")
    print('Take '+city+' ['+latitude+','+longitude+'] to mesure lattency.\n' )
elif len(sys.argv) == 2:
    city = sys.argv[1]
    url = 'https://nominatim.openstreetmap.org/search/' + city +'?format=json'
    response = requests.get(url).json()
    latitude = response[0]['lat']
    longitude = response[0]['lon']
    print('Take '+response[0]['display_name']+' to mesure lattency. If error try to precise location.\n' )
else:
    print("Error: Bad number of argumetns")

#Defines the period of time over which the measurements are taken
current_time=time.time()
one_week_ago=int(current_time-604800)
two_days_ago=int(current_time-172800)

#Query probes in ./probes
url ="https://atlas.ripe.net/api/v2/probes/?is_public=true&page_size=500&status_name=Connected&fields=asn_v4,is_anchor&radius={},{}:{}".format(latitude,longitude,radius)
resp = requests.get(url)
content = json.loads(resp.content)

#Write city probes in a file 
with open('./probes/'+city+'.json','w') as outfile:
    json.dump(content, outfile)

probes_id_by_ASN = {}
results_by_ASN = {}
final_ranking = {}
n_anchor = 0

#Lookup for the ASN of each probe and anchor
for probe in content["results"]:
    if probe["asn_v4"] == None:
        continue
    if probe['is_anchor']:
        n_anchor += 1
    
    #Query ASN Name
    holder = json.loads(requests.get('https://stat.ripe.net/data/as-overview/data.json?resource='+str(probe['asn_v4'])).text)['data']['holder']
    
    if holder not in probes_id_by_ASN.keys():
        probes_id_by_ASN[holder] = [probe["id"]]
    else:
        probes_id_by_ASN[holder].append(probe["id"])

print('There are '+str(content['count'])+' probes around '+city+' of which '+str(n_anchor)+' are anchors.\n')
print('ISP are the following:')
for k in probes_id_by_ASN.keys():
    print(str(k)+': '+str(len(probes_id_by_ASN[k]))+' probes')
print()

#GET measurements for each probe on each root dns servers and atlas infrastructures
for ASN in probes_id_by_ASN.keys():
    probes = probes_id_by_ASN[ASN]
    results_by_ASN[ASN] = []

    print("Fetching ping measurements of probes from {} to root dns servers and atlas infrastructures".format(ASN))

    for measurement_id in range(1009,1028):
        error = False
        url = "https://atlas.ripe.net/api/v2/measurements/{}/results/?start={}".format(measurement_id,two_days_ago)+"&probe_ids="

        for prob in probes:
            url = url+str(prob)+","
        resp = json.loads(requests.get(url[:-1]).content)

        acc = 0.0
        count = 0
        for result in resp:
            if(result == "error"):
                error = True
                break
            acc = acc + result["avg"]
            count += 1

        if not error and count != 0 :
            results_by_ASN[ASN].append(acc/count)
        else:
            results_by_ASN[ASN].append(-1)

#Write result data in ./data
with open('./data/'+city+'_data.json', 'w') as outfile:
    json.dump(results_by_ASN, outfile)

print('The program ended successfully')