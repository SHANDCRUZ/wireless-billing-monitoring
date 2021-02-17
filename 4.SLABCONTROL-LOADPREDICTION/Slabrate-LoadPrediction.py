# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:00:00 2021

@author: SHANDCRUZ
"""
# unit from the prediction model
unit = 2945840
premonthvalue = 2945540
noofdays = 30
unit = unit - premonthvalue
def unitcalc(unit1):    
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
    
def perctangecalc(unit1):
    if(unit1<=100):
        per =  unit1
        return per,1
    elif(unit1<=200):
        per = int(unit1-100)
        return per,2
    elif(unit1<=500):
        unit1 -= 200
        per = int((unit1/300)*100)
        return per,3
    
def getunit(cost):
    if(cost<1130):
        newunit = (cost - 230)/3
        newunit +=200
        return newunit
    else:
        newunit = (cost - 1780)/6.6
        newunit +=500
        return newunit

consumed=unitcalc(unit)
percent,slab = perctangecalc(unit)
estimatedunit = (60/noofdays)*unit
estimatedcost = unitcalc(estimatedunit)
print("Electricity Bill:"+str("Rs. ")+str(consumed))
print("consumed "+str(percent)+str(" %")+" of energy at slab "+str(slab) )
print("Estimated Bill : "+str("Rs. ") + str(estimatedcost) )

#######################################################################
# ----------------------LOAD PREDICTION--------------------------------
#######################################################################

reducecost = 800   #BASE AMOUNT WITH 780 (765 CASE 2)
reduceunit = getunit(reducecost)
avalunit = reduceunit - unit
print(reduceunit)
print(avalunit)
remainingunit = estimatedunit-unit
print(consumed, percent, estimatedcost, estimatedunit, remainingunit )
##### for load forecast######
noofdays = 30
remdays = 60 - noofdays
dicthour = {
    "light" : 4,
    "fan" : 20,
    "charger" : 3,
    "motor" : 0.5,
    "tv" : 6,
    "refrigerator" : 24,
    "wetgrinder" : 0.5,
    "ironbox" : 0.5,
    "mixer" : 0.0166   
    }


dictload = {
    "light" : 0.040,
    "fan" : 0.075,
    "charger" : 0.007,
    "motor" : 0.750,
    "tv" : 0.100,
    "refrigerator" : 0.0356,
    "wetgrinder" : 0.300,
    "ironbox" : 0.700,
    "mixer" : 0.500   
    }  #all the load in kW

unitperday = 0
for x in dicthour:
    unitperday += dictload[x]* dicthour[x]
print(unitperday*remdays)
basicunit = unitperday*remdays
additionalunit = (avalunit - basicunit)/remdays
print("Additonal unit "+ str(additionalunit))
print(unitperday)
invalidnumber = 0
flag=0
if(additionalunit>0):
    flag = 1
    amt = unitcalc(basicunit+unit)
    amt = reducecost-amt
    print("Amount saved :"+str(amt))   
if(additionalunit<0):
    additionalunit = unitperday+additionalunit
    if(additionalunit>1.67803): 
        runit = additionalunit - 1.67803
        if(runit>0.9):
                #dicthour["wetgrinder"]= 0.1428
                #dicthour["ironbox"]= 0.1428
                #dicthour["mixer"]= 0.0833
                dicthour["fan"] = 8
                dicthour["tv"] = 3
                temp = dicthour["fan"]*dictload["fan"] + dicthour["tv"]*dictload["tv"]
                runit -=temp
                if(runit>0.1428):
                    dicthour["wetgrinder"]= 0.1428
                    dicthour["ironbox"]= 0.1428
                    runit -=0.1428
                    additionaltv = runit/dictload["tv"]
                    additionalfan = runit/dictload["fan"]
                    print(additionaltv,additionalfan)
                else:
                    dicthour["wetgrinder"] = 0
                    dicthour["ironbox"] = 0
                    additionaltv = runit/dictload["tv"]
                    additionalfan = runit/dictload["fan"]
                    print(additionaltv,additionalfan)
        else:
            invalidnumber = 1
            print("Invalid amount")
    else:
        invalidnumber = 1
        print("Invalid amount")
if(not invalidnumber):
    for x,y in dicthour.items():
        print(str(x)+ "  :  "+str(y) )
else:
    print("Invalid amount")