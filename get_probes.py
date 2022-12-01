import json
import requests

dict_cities = {'Vancouver':'49.280,-123.130','Winnipeg':'49.880,-97.170','Calgary':'51.050,-114.060','Toronto':'43.650,-79.380','Ottawa':'45.420,-75.710','Montreal':'45.520,-73.570','Quebec':'46.820,-71.230'}

for cities in dict_cities:
    probes = requests.get('https://atlas.ripe.net/api/v2/probes/?is_public=true&status_name=Connected&page_size=500&fields=asn_v4,asn_v6,is_anchor&radius='+dict_cities[cities]+':50')
    
    with open('./probes/'+cities+'.json','w') as outfile:
        outfile.write(probes.text)

