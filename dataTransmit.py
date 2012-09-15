from datetime import datetime,timedelta
from decimal import *
from math import *
import csv
import locale
import matplotlib.pyplot as plt
import random
import time
"""
Type
	A
		Change the amount of recovered MB per day
	R
		Reset the Queue to zero
	T
		Transmit data
	V
		Change recovery variance
"""

##############
### CONFIG ###
##############

currentByteStorage = 0

dataFileStr = "data/transmits.csv"

maxByteStorage = 50*2**30

missionYears = 5

recoveredBytesPerDay = 50*(2**30)

recoveryVariance = 1

startDate = datetime(2017,9,22)

# View min/max
	# Set to [] to view the full range
viewMin = startDate 
viewMax = startDate + timedelta(days=30)

dataMax = 50*4

# NEVER CHANGE THESE!!!!!
timeStep = timedelta(minutes=15)
random.seed("Colony World")
locale.setlocale(locale.LC_NUMERIC,'')

##################
### END CONFIG ###
##################

#################
### FUNCTIONS ###
#################

def SumQueue(data):
	sumVal = 0
	for i in data:
		sumVal+=i[2]
	return sumVal

def RecordPreDelete(record,date):
	print "Record Complete:"
	print "    Transmitted:",date
	print "    User: %s" % record[1]
	print "    Submission:",record[0]
	print "    Total Transmit Time:",date-record[0]
	if(len(record[4])):
		print "    Comment: %s" % record[4]

def RecordStartTrans(record,date):
	print "Record Start:"
	print "    Started:",date
	print "    User: %s" % record[1]
	print "    Submission:",record[0]
	print "    Data:",locale.format("%.2f",record[2],grouping=True),"MiB"
	print "    Delay:",date-record[0]
	if(len(record[4])):
		print "    Comment: %s" % record[4]

def RecordQueueTrans(record,date):
	print "Record Queue:"
	print "    Queued:",date
	print "    User: %s" % record[1]
	print "    Submission:",record[0]
	# print "    Data: %.2f MiB" % record[2]
	print "    Data:",locale.format("%.2f",record[2],grouping=True),"MiB"
	if(len(record[4])):
		print "    Comment: %s" % record[4]
#####################
### END FUNCTIONS ###
#####################

#################
### CALCULATE ###
#################

endDate = startDate + timedelta(days=missionYears*365.24)

if(viewMin == []):
	viewMin = startDate
if(viewMax == []):
	viewMax = endDate

###########
### RUN ###
###########

start = time.time()
dataReader = csv.reader(open(dataFileStr,"rb"))
dataReader.next()
dataTrans=list()
for i in dataReader:
	try:
		dataTrans.append( [datetime.strptime(i[0],"%m/%d/%Y %H:%M:%S"),i[1],float(eval(i[2])),i[3],i[4]])
	except:
		print i
		time.sleep(0.1)
		raise
x=list()
y=list()
y2=list()
curDate = startDate
indexVal = 0
dataQueue = list();
print "Simulate..."
while(curDate < endDate):
	#print curDate
	while(indexVal < len(dataTrans) and dataTrans[indexVal][0] < curDate):
		# Q Up New Transfers and Byte Rate Changes
		#print dataTrans[indexVal]
		if(dataTrans[indexVal][3]=="T"):
			#print "Transfer"
			dataQueue.append(dataTrans[indexVal])
			if(curDate > viewMin and curDate < viewMax):
				RecordQueueTrans(dataTrans[indexVal],curDate)
				if(len(dataQueue)==1):
					RecordStartTrans(dataQueue[0],curDate)
		elif(dataTrans[indexVal][3]=="A"):
			recoveredBytesPerDay = dataTrans[indexVal][2]*2**20
			#print "Alter Data Rate"
		elif(dataTrans[indexVal][3]=="R"):
			dataQueue = list()
		elif(dataTrans[indexVal][3]=="V"):
			recoveryVariance = dataTrans[indexVal][2]
		else:
			print "Error! Cannot read line:"
			print dataTrans[indexVal]
		indexVal+=1
	# Process Data Queue
	if(len(dataQueue)):
		# Loop through the Queue until we burn out data or run out of Queue
		for i in range(len(dataQueue)):
			# Convert MB to B and compare
			if(dataQueue[0][2]*2**20 > currentByteStorage):
				dataQueue[0][2]-=currentByteStorage/(2**20)
				currentByteStorage=0
				break
			else:
				currentByteStorage -= dataQueue[0][2]*(2**20)
				if(curDate > viewMin and curDate < viewMax):
					RecordPreDelete(dataQueue[0],curDate)
				del dataQueue[0]
				if(len(dataQueue)==0):
					break
				elif(curDate > viewMin and curDate < viewMax):
					RecordStartTrans(dataQueue[0],curDate)
	# Recovery Bytes

	x.append(curDate)
	y.append(currentByteStorage/(2**30))
	y2.append(SumQueue(dataQueue)/(2**10))

	currentByteStorage += recoveredBytesPerDay*(timeStep.total_seconds()/(24.*60.*60.)) * random.gauss(1,recoveryVariance)
	if(currentByteStorage > maxByteStorage):
		currentByteStorage = maxByteStorage 
	elif(currentByteStorage<0):
		currentByteStorage = 0
	curDate += timeStep

print "Plot..."
fig, ax = plt.subplots(1)
plt.plot(x,y,x,y2)
fig.autofmt_xdate()
plt.xlim(viewMin,viewMax)
if(dataMax):
	plt.ylim(ymax = dataMax)
plt.ylabel("Data (GiB)")
print "Fin!"
print "Time: ",time.time()-start
plt.show()