# Atlas2
In this project, we use Ripe Atlas to sort the different ISPs that serve a city. This ranking is based on the time to reach important destinations. The area assigned to our group is North America.

As a short reminder, Ripe Atlas is a global network of probes that measure Internet connectivity and reachability, providing an unprecedented understanding of the state of the Internet in real time. There are about 12000 active probes on the planet. Most probes perform built-in measurements that are publicly avail- able, that’s what we used for this project.

The full result are in the /result folder. We have also sort the result by country in the folders /result_CA, /result_US, /result_MX.

If you want to fetch and analyse the data by yourself you can use the generate.sh and analyse.sh script. However, we recommend not to do this because it is very long (several hours).

To test by yourself we advise you to choose a city and to launch the python script for this city. Here are some examples of cities with their coordinates:

Canada:
'Vancouver':'49.280,-123.130' 
'Toronto':'43.650,-79.380'
'Ottawa':'45.420,-75.710'
'Montreal':'45.520,-73.570'
'Winnipeg':'49.880,-97.170'
'Calgary':'51.050,-114.060'
'Quebec':'46.820,-71.230'

USA:
'New-York':'40.712784,-74.005941'

The python script to fetch data is City_data.py, it take variable number of input arguments which can be:
• 1 argument: (string) Name of city and some info to help localisation
• 3 arguments: (string) Name,(float) latitude,(float) longitude *default radius is 100km
• 4 arguments: (string) Name,(float) latitude,(float) longitude, (int) radius in km

It will write the data in a json file in the /data directory.
To genearate the ranking you need to lanch the rank.py script with the name of the city as argument. 