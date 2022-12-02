import json
import sys

path=sys.argv[1]
threshhold=1.0
f=open(path)
data=json.load(f)
ases=list(data.keys())
nb_destination=len(data[ases[0]])
remaining_destination=len(data[ases[0]])
means=[]
data_by_destination=[]
leaderboard={}

#clean the data compute means and format by destination
def clear():
    global means
    global remaining_destination
    global data_by_destination

    means=[]
    data_by_destination=[]
    to_clean=[]
    for dest in range(nb_destination):
        count=0
        count_mean=0
        acc=0.0
        data_by_destination.append({})
        for AS in ases:
            data_by_destination[dest][AS]=data[AS][dest]
            if data[AS][dest]==-1:
                count+=1
            else:
                count_mean +=1
                acc+=data[AS][dest]
        
        if(len(ases)-count>=(int)(len(ases)*threshhold)):
            means.append(acc/count_mean)
        else:
            to_clean.append(dest)
    count=0
    for ind in to_clean:
        del(data_by_destination[ind-count])
        count+=1
    remaining_destination=nb_destination-len(to_clean)



while(True):
    clear()
    user_input=input("Rank will be calculated from pings on {} differents targets. Do you wanna try to increase the number of targets? (It could lower the quality of the data) (y/n): ".format(remaining_destination))
    if user_input =="y":
        threshhold-=0.1
        print(threshhold)
        if(threshhold<0.2):
            print("You can't increase the number of targets anymore")
            break
        continue
    elif user_input=="n":
        break
    else:
        print("Bad response.Please type y or n")


#rank by destination and update remaining -1
for i in range (len(data_by_destination)):
    data_by_destination[i]=dict(sorted(data_by_destination[i].items(), key=lambda item: item[1]))
    replace=False
    for neg in data_by_destination[i]:
        if(data_by_destination[i][neg]<.0):
            replace=True
            data_by_destination[i].update({neg:means[i]})
        else:
            break
    if(replace):
        data_by_destination[i]=dict(sorted(data_by_destination[i].items(), key=lambda item: item[1]))

#build global leaderboard
for AS in ases:
    leaderboard[AS]=0

count=1
for dest in data_by_destination:
    point=len(ases)
    for AS in dest:
        leaderboard.update({AS:leaderboard[AS]+point})
        point-=1
        if(count==remaining_destination):
            leaderboard.update({AS:round((leaderboard[AS]/(remaining_destination*len(ases))),2)})
    count+=1




leaderboard=dict(sorted(leaderboard.items(), key=lambda item: item[1],reverse=True))



print("\nRESULTS:")
for item in leaderboard.items():
    print(item)
