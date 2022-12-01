import subprocess
import requests
import json
import sys
import time
from statistics import mean




cities= {'New-York':(40.712784,-74.005941,100)}
city=cities[sys.argv[1]]

current_time=time.time()
one_week_ago=int(current_time-604800)
two_days_ago=int(current_time-172800)



url ="https://atlas.ripe.net/api/v2/probes/?is_public=true&page_size=500&status_name=Connected&radius={},{}:{}".format(city[0],city[1],city[2])
resp = requests.get(url)
content=json.loads(resp.content)
probes_id_by_ASN={}
results_by_ASN={}
final_ranking={}




""" while(content["next"]!="null"):
    with open('./probes_US/'+sys.argv[1]+'.txt','w+') as outfile:
        outfile.write(json.dumps(content)) """

#print(content["results"])
for probe in content["results"]:
    if probe["asn_v4"]== None:
        continue
    holder = json.loads(requests.get('https://stat.ripe.net/data/as-overview/data.json?resource=' + str(probe['asn_v4'])).text)['data']['holder']
    
    if holder not in probes_id_by_ASN.keys():
        probes_id_by_ASN[holder]=[probe["id"]]
    else:
        probes_id_by_ASN[holder].append(probe["id"])

print(probes_id_by_ASN)
for ASN in probes_id_by_ASN.keys():
    probes=probes_id_by_ASN[ASN]
    results_by_ASN[ASN]=[]
    print("Fetching ping measurements of probes from {} to root dns servers and atlas infrastructures".format(ASN))
    for measurement_id in range(1009,1028):
        error=0
        url="https://atlas.ripe.net/api/v2/measurements/{}/results/?start={}".format(measurement_id,two_days_ago)+"&probe_ids="
        for prob in probes:
            url=url+str(prob)+","
        url=url[:-1]
        print(url)
        resp=json.loads(requests.get(url).content)
        acc=0.0
        count=0
        for result in resp:
            if(result=="error"):
                error=1
                break
            acc=acc+(result["avg"])
            count=count+1
        if error==0 and count!=0 :
            results_by_ASN[ASN].append(acc/count)
        else:
            results_by_ASN[ASN].append(-1)

print(results_by_ASN)

        



#resp=json.loads(requests.get(url).content)
#print(resp)

#url="https://atlas.ripe.net/api/v2/measurements/{}/results/?probe_ids=".format(measurement_id)
#resp = requests.get(url)