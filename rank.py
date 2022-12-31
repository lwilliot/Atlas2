import json
import sys
import numpy as np


city=sys.argv[1]
f=open('./data/'+city+'_data.json')
data=json.load(f)
ases=list(data.keys())
nb_destination=len(data[ases[0]])
remaining_destination=len(data[ases[0]])
data_by_destination=[]
leaderboard={}
medians=[]
threshhold = 1.0



#clean the data by removing destinations that are not pinged by all AS. 
# And format data by destination instead of by AS to make the ranking easier to compute.
def clear():
    global medians
    global remaining_destination
    global data_by_destination

    data_by_destination=[]
    to_clean=[]
    #add index of invalid destination in to_clean and build data_by_destination
    for dest in range(nb_destination):
        count = 0
        data_by_destination.append({})

        for AS in ases:
            data_by_destination[dest][AS]=data[AS][dest]
            if data[AS][dest]==-1:
                count+=1
            
        if(len(ases)-count < (int)(len(ases)*threshhold)):
             to_clean.append(dest)
    
    #remove invalid destinations
    offset=0
    for ind in to_clean:
        del(data_by_destination[ind-offset])
        offset += 1
    remaining_destination = nb_destination - len(to_clean)



while(True):
    clear()
    user_input=input("Rank will be calculated from pings on {} differents targets. Do you wanna try to increase the number of targets? (It could lower the quality of the data) (y/n): ".format(remaining_destination))
    
    if user_input == "y":
        threshhold -= 0.1
        print("current threshold is {}".format(threshhold))

        if(threshhold<0.2):
            print("You can't increase the number of targets anymore")
            break
        continue

    elif user_input == "n":
        break
    else:
        print("Bad response.Please type y or n")



#Sort the AS for each destination and normalize the RTT value
for i in range (len(data_by_destination)):
    liste =(list(data_by_destination[i].values()))
    array=np.array([element for element in liste if element != -1])
    min=np.min(array)
    max=np.max(array)
    median=np.median(array)
    for AS in data_by_destination[i]:
        if(data_by_destination[i][AS]<.0):
            replace = True
            data_by_destination[i].update({AS:median})
        data_by_destination[i].update({AS:1-((data_by_destination[i][AS]-min)/(max-min))})
    data_by_destination[i]=dict(sorted(data_by_destination[i].items(), key=lambda item: item[1]))



#build global leaderboard
for AS in ases:
    leaderboard[AS]=0

#Add value of each ranking to leaderboard and compute the mean.
count=1
for dest in data_by_destination:
    point=len(ases)
    for AS in dest:
        multiplier=0
        leaderboard.update({AS:leaderboard[AS]+dest[AS]})
        if(count==remaining_destination):
            leaderboard.update({AS:round((leaderboard[AS]/(remaining_destination)),3)}) 
    count+=1
leaderboard=dict(sorted(leaderboard.items(), key=lambda item: item[1],reverse=True))



print("\nRESULTS based on {} destinations:".format(remaining_destination))
for item in leaderboard.items():
    print(item)


#Write result data in ./result
with open('./result/'+city+'.txt', 'w') as outfile:
    outfile.write("RESULTS:\n")
    for item in leaderboard.items():
        outfile.write(str(item)+"\n")

