import json
import requests

dict_cities = {'Vancouver':'49.280,-123.130','Winnipeg':'49.880,-97.170','Calgary':'51.050,-114.060','Toronto':'43.650,-79.380','Ottawa':'45.420,-75.710','Montreal':'45.520,-73.570','Quebec':'46.820,-71.230'}

for cities in dict_cities:
    probes_json = requests.get('https://atlas.ripe.net/api/v2/probes/?is_public=true&status_name=Connected&page_size=500&fields=asn_v4,asn_v6,is_anchor&radius='+dict_cities[cities]+':50')
    
    with open('./probes_CA/'+cities+'.json','w') as outfile:
        outfile.write(probes_json.text)

    
    anchors = 0
    dict_probes = json.loads(probes_json.text)
    count = dict_probes['count']
    list_probes = dict_probes['results']
    dict_asn = {'asn_v4':{},'asn_v6':{}}

    for d in range(len(list_probes)):
        probe = list_probes[d]
        if(probe['is_anchor']):
            anchors+=1
        if str(probe['asn_v4']) not in dict_asn['asn_v4'].keys() and str(probe['asn_v4']) != 'None':
            holder = json.loads(requests.get('https://stat.ripe.net/data/as-overview/data.json?resource=' + str(probe['asn_v4'])).text)['data']['holder']
            dict_asn['asn_v4'][str(probe['asn_v4'])] = holder


        if str(probe['asn_v6']) not in dict_asn['asn_v6'].keys() and str(probe['asn_v6']) != 'None':
            holder = json.loads(requests.get('https://stat.ripe.net/data/as-overview/data.json?resource=' + str(probe['asn_v6'])).text)['data']['holder']
            dict_asn['asn_v6'][str(probe['asn_v6'])] = holder



    print('There are '+str(count)+' probes in '+cities+' of which '+str(anchors)+' are anchors')
    print(dict_asn)
    print()
    


