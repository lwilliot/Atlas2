import json
import sys


#path=sys.argv[1]
threshhold=0.8
f=open('data/New-york.json')
data=json.load(f)
ases=list(data.keys())
nb_destination=len(data[ases[0]])
means=[]
data_by_destination=[]
leaderboard={}

#clean the data compute means and format by destination
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
    if(count>=(int)(nb_destination*threshhold)):
        to_clean.append(dest)
    else:
        means.append(acc/count_mean)
count=0
for ind in to_clean:
    del(data_by_destination[ind-count])
    count+=1

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

for dest in data_by_destination:
    point=len(ases)
    print(point)
    print(dest)
    for AS in dest:
        leaderboard.update({AS:leaderboard[AS]+point})
        point-=1


leaderboard=dict(sorted(leaderboard.items(), key=lambda item: item[1],reverse=True))
print(leaderboard)




