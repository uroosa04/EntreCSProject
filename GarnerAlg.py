import sys
import math

#Variables needed
milesTraveled = 0.00
fudgeFactor = 0.00 
elevationGain = 0 
elevationLoss = 0
lossRate = 0
totalMiles = 0.00 
gainFactor = 0.00 
lossFactor = 0.00 
elevationFactor = 0.00 
totalMovingTime = 0.00
totalTravelTime = 0.00
paceIndex = 0
trail = ""

#Ask user to choose trail
trail=int(input("Please pick a trail: \n 1. Old Entrance Road \n 2. Donovan Trail \n 3. Bridges Trail \n 4. Crystal Cave Trail \n 5. Blinn River Trail \n 6. Old Baldy Trail \n 7. Foshee Trail \n 8. Ashe Juniper Trail \n 9. Old Horse Trail \n 10. Frio Canyon Trail \n"))

#function to set values for chosen trail
def getTrailInfo(x):
	global milesTraveled
	global elevationGain
	global elevationLoss
	if x==1:
		print("You have chosen Old Entrance Road!")
		milesTraveled=.84
		elevationGain = 160
		elevationLoss = 0
	elif x==2:
		print("You have chosen Donovan Trail!")
		milesTraveled=.71
		elevationGain = 240
		elevationLoss = 0
	elif x==3:
		print("You have chosen Bridges Trail!")
		milesTraveled=.65
		elevationGain = 400
		elevationLoss = 0
	elif x==4:
		print("You have chosen Crystal Cave Trail!")
		milesTraveled=.62
		elevationGain = 340
		elevationLoss = 0
	elif x==5:
		print("You have chosen Blinn River Trail!")
		milesTraveled=.53
		elevationGain = 20
		elevationLoss = 0
	elif x==6:
		print("You have chosen Old Baldy Trail!")
		milesTraveled=.53
		elevationGain = 480
		elevationLoss = 0
	elif x==7:
		print("You have chosen Foshee Trail!")
		milesTraveled=1.66
		elevationGain = 560
		elevationLoss = 0
	elif x==8:
		print("You have chosen Ashe Juniper Trail!")
		milesTraveled=2.49
		elevationGain = 260
		elevationLoss = 0
	elif x==9:
		print("You have chosen Old Horse Trail!")
		milesTraveled=.48
		elevationGain = 80
		elevationLoss = 0
	elif x==10:
		print("You have chosen Frio Canyon Trail!")
		milesTraveled=2.88
		elevationGain = 320
		elevationLoss = 0
	else:
		print("Invalid entry. Please try again.")						

#Assign trail
getTrailInfo(trail)

print(" ")

paceIndex=int(input("Input pace index 1 - 4, (1 for beginner, 4 for experienced hiker)"))

print(" ")

x =(milesTraveled / 10)
fudgeFactor=round(x,1)
print("Fudge Factor: ", fudgeFactor)

totalMiles = round((milesTraveled + fudgeFactor),1)
int(totalMiles)
print("Total Miles: " , totalMiles)


climbingRate = 1000	#CONSTANT
gainFactor = round(elevationGain / climbingRate,1)
print("Gain Factor: ", gainFactor)


lossRate = 2000 #CONSTANT
lossFactor = round((elevationLoss / lossRate),1)
print("Loss Factor: " , lossFactor)

elevationFactor = (gainFactor - lossFactor)
print("Elevation Factor: " , elevationFactor)

totalMovingTime = round(((totalMiles/paceIndex)+elevationFactor),1)
print("Total Moving Time: ", totalMovingTime, " hours.")


if ((totalMovingTime) > 0) :
	tempMovingTime=math.floor(totalMovingTime)
	numLongBreaks=int(tempMovingTime/4)
	leftoverMovingTime=tempMovingTime-numLongBreaks
	numshortbreaks=leftoverMovingTime
	shortbreakstime=(numshortbreaks * 5) 
	longbreakstime=numLongBreaks * 30
	print("Short Breaks: ", shortbreakstime, " minutes.")
	print("Long Breaks: ", longbreakstime, " minutes.")
else :
	shortbreakstime=0
	longbreakstime=0
	print("Short Breaks: ", shortbreakstime, " minutes.")
	print("Long Breaks: ", longbreakstime, " minutes.")	


totalTravelTime = round((totalMovingTime + (shortbreakstime/60) + (longbreakstime/60)),1)
print("Total Travel Time: " , totalTravelTime, " hours.")

