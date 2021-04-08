#author SHANDCRUZ
from Adafruit_IO import Client, Feed
import requests
import csv
import numpy as np
import pandas as pd
import datetime
import time
ts = time.time()
print(ts)
ADAFRUIT_IO_KEY = 'eea9210ecf3a46d5b7e7c3f67e4e8303'
ADAFRUIT_IO_USERNAME = 'SHAN_D_CRUZ'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

#ts = time.time()
#starttime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
#startdate =datetime.datetime(2021,1,16).strftime('%Y-%m-%d')
#enddate = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
startyear = 2021
startmonth = 1
startday = 16

stop = 0
loadvar =[]
runningtime = []
computeflag = []
prelength = []
loadhour = []
avgloadhour = []
avgloadcost = []
meterReading = 300
loadunit = []
loadbill = []
# = pd.ExcelWriter('multiple.xlsx')
#df1 = pd.DataFrame(columns = ["date","time","value"])
load = ["light"] 
loadwatt = [0.04] 
billamount = 0
avgfeedlabel = []
billfeedlabel = []

for i in range(len(load)):
    #df1.to_excel(writer, sheet_name=load[i],index =False)
    temp =0
    loadvar.append(temp)
    runningtime.append(temp)
    computeflag.append(temp)
    prelength.append(temp)
    loadhour.append(temp)
    avgloadhour.append(temp)
    loadunit.append(temp)
    loadbill.append(temp)
    avgfeedlabel.append(load[i]+"avg")
    billfeedlabel.append(load[i]+"bill")
    try:
        aio.feeds(load[i])
    except:
        new_feed = Feed(name=load[i])
        aio.create_feed(new_feed)
#writer.save()
for i in range(len(load)):
    try:
        aio.feeds(avgfeedlabel[i])
        aio.feeds(billfeedlabel[i])
    except:        
        aio.create_feed(Feed(name=avgfeedlabel[i]))
        aio.create_feed(Feed(name=billfeedlabel[i]))


def loadcompute():
    ts = time.time()   
    avgdays =datetime.datetime.fromtimestamp(ts) - datetime.datetime(startyear,startmonth,startday)
    avgday = avgdays.total_seconds()/86400
    for j in range(len(load)):
        global loadhour,runningtime,prelength,computeflag
        loaddata = pd.read_excel("multiple.xlsx",sheet_name = load[j])
        data = loaddata.loc[:]['time'].values
        if(len(data)%2 == 0):
            loadhour[j]-=runningtime[j]
            for i in range(prelength[j],len(data),2):
                date_time_str = data[i]
                date_time_str_next = data[i+1]
                difftime = datetime.datetime.strptime(date_time_str_next, '%H:%M:%S') - datetime.datetime.strptime(date_time_str, '%H:%M:%S')
                timestr = str(difftime)
                hour,minute,second = timestr.split(":")
                hour = int(hour)
                minute = int(minute)
                second = int(second)
                loadhour[j]+=(hour)+(minute/60)+(second/3600)
                prelength[j] = i+2
                computeflag[j] = 0
                
        
        
        if(len(data)%2==1):    
            for i in range(prelength[j],len(data),2):
                if(i != len(data)-1):
                    date_time_str = data[i]
                    date_time_str_next = data[i+1]
                    difftime = datetime.datetime.strptime(date_time_str_next, '%H:%M:%S') - datetime.datetime.strptime(date_time_str, '%H:%M:%S')
                    timestr = str(difftime)
                    hour,minute,second = timestr.split(":")
                    hour = int(hour)
                    minute = int(minute)
                    second = int(second)
                    loadhour[j]+=(hour)+(minute/60)+(second/3600)
                    computeflag[j] = 0
                if(i == len(data)-1 and computeflag[j] == 0):
                    date_time_str=data[i]        
                    ts = time.time()
                    date_time_str_next = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    difftime = datetime.datetime.strptime(date_time_str_next, '%H:%M:%S') - datetime.datetime.strptime(date_time_str, '%H:%M:%S')
                    timestr = str(difftime)
                    hour,minute,second = timestr.split(":")
                    hour = int(hour)
                    minute = int(minute)
                    second = int(second)
                    runningtime[j] =(hour)+(minute/60)+(second/3600)
                    loadhour[j]+=(hour)+(minute/60)+(second/3600)
                    prelength[j] = i
                    computeflag[j] =1
        
        avgloadhour[j] = loadhour[j]/avgday


def calculatebill(unit1):    
        if(unit1<=100):
            bill = 0
            return bill
        elif(unit1<=200):
            bill = (unit1 -100)*1.50 +20
            #print(customerName+" Electricity Bill : Rs. "+str(bill) )
            #print(customerName+" had consumed "+str(per)+" % of slab 2")
            return bill
        elif(unit1<=500):
            unit1 -= 200
            bill = 230+(unit1*3)
            #print(customerName+" Electricity Bill : Rs. "+str(bill) )
            #print(customerName+" had consumed "+str(per)+" % of slab 3")
            return bill
        else:
            unit1 -=500
            bill = 1780+(unit1*6.6)
            #print(customerName+" Electricity Bill : Rs. "+str(bill))
            return bill



def displayload(energycost):
    ts = time.time()   
    avgdays =datetime.datetime.fromtimestamp(ts) - datetime.datetime(startyear,startmonth,startday)
    avgday = avgdays.total_seconds()/86400
    for i in range(len(load)):
        #display to the feed
        #calculate avg amount of load        
        loadunit[i] = avgday*avgloadhour[i]*loadwatt[i]
        loadbill[i] = (loadunit[i]/meterReading)*energycost
        aio.send(billfeedlabel[i], loadbill[i])
        aio.send(avgfeedlabel[i], avgloadhour[i])
        





for i in range(len(load)):    
    while(stop==0):
        for i in range(len(load)):
            if(int(aio.receive(load[i]).value) != loadvar[i]):
                data = pd.read_excel("multiple.xlsx",sheet_name = load[i])
                loadvar[i] = int(aio.receive(load[i]).value)
                ts = time.time()
                starttime = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                data.loc[len(data)] = [date,starttime,loadvar[i]]
                data.to_excel("multiple.xlsx",sheet_name =load[i],index= False)
            
        loadcompute()
        billamount = calculatebill(meterReading)
        displayload(billamount)
        stop = 1

