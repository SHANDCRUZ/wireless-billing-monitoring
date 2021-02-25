# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 23:01:01 2020

@author: SHAN_D_CRUZ
"""
import math
import tkinter as tk
from tkinter import Message ,Text
import datetime
import time
import tkinter.ttk as ttk
import tkinter.font as font
from PIL import Image, ImageTk, ImageOps
import pandas as pd
import csv
import cv2
import tensorflow.keras
import numpy as np
import time
currtime=datetime.datetime.now().strftime('%H')
currentTime = datetime.datetime.strptime(currtime,"%H").time() 
mor=datetime.datetime.strptime('12',"%H").time()
aft=datetime.datetime.strptime('17',"%H").time()
if currentTime < mor :
     greet = 'Good morning  '
elif currentTime < aft :
     greet = 'Good afternoon  '
else:
     greet = 'Good evening   '


window = tk.Tk()
window.title("Smart Energy Meter")
window.geometry('1000x633')
window.configure(background='blue')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

bg_image = tk.PhotoImage(file='source/test1.png')
w = bg_image.width()
h = bg_image.height()
print(w,h)
cv = tk.Canvas(width=w, height=h)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0, 0, image=bg_image, anchor='nw')

message = tk.Label(window, text="SMART ENERGY MANAGEMENT" ,width=30  ,height=2,font=('BloodWax', 19, 'italic bold underline')) 

message.place(x=230, y=10)

msg2 = tk.Label(window, text="Customer ID: ",width=20  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
msg2.place(x=250, y=80)

name = tk.Entry(window,width=20 ,bg="yellow" ,fg="red",font=('times', 15, ' bold '))

name.place(x=550, y=80)


def service():
    
    customerName = "shan"              #(name.get())
    display = tk.Label(window, text = greet +str(customerName)+'!',bg = "red",font=('times',15,'bold'))
    display.place(x=380,y=165)
    np.set_printoptions(suppress=True)    
    # Load the model
    model = tensorflow.keras.models.load_model('gray.h5')    
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)    
    im = cv2.imread("black and white.jpeg")
    j = int(im.shape[1]/7)
    print(im.shape,j)
    z=0
    unit =0
    premonthval = 2945540
    noofdays = 30
    for i in range(0,7):
        crop = im[0:92 , z:z+j]  
        
        crop =cv2.resize(crop,(224,224))
        
        cv2.imwrite(str(i)+".jpg",crop)
        
        image = Image.open(str(i)+'.jpg')
        #resize the image to a 224x224 with the same strategy as in TM2:
        #resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)        
        #turn the image into a numpy array
        image_array = np.asarray(image)
        
        # display the resized image
        #image.show()
        
        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        
        # Load the image into the array
        data[0] = normalized_image_array
        
        # run the inference
        prediction = model.predict(data)
        #print(prediction)
        value = int(np.argmax(prediction,axis=1))
        unit+=(value*pow(10,6-i))
        print(value)
        z+=j
    unit = unit - premonthval
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
    
    def truncate(number, digits) -> float:
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper
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
    def loadforecast():
        reducecost = int((cusnameEntry.get()))
        reduceunit = getunit(reducecost)
        avalunit = reduceunit - unit
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
            } #in hours
        
        
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
        basicunit = unitperday*remdays
        additionalunit = (avalunit - basicunit)/remdays    
        invalidnumber = 0
        flag = 0
        print(additionalunit)
        if(additionalunit>0):
            flag = 1
            amt = unitcalc(basicunit+unit)
            amt = reducecost-amt
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
                            if(additionalfan>15):
                                additionalfan = 16
                            if(additionaltv>20):
                                additionaltv = 21
                            print(additionaltv,additionalfan)
                        else:
                            dicthour["wetgrinder"] = 0
                            dicthour["ironbox"] = 0
                            additionaltv = runit/dictload["tv"]
                            additionalfan = runit/dictload["fan"]
                            print(additionaltv,additionalfan)
                else:
                    invalidnumber = 1
            else:
                invalidnumber = 1
        if(not invalidnumber):
            load = tk.Label(window, text="Light",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=200)
            loadval = tk.Label(window, text=str(truncate(dicthour["light"], 1))+" hr/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            loadval.place(x=790,y=200)
            load = tk.Label(window, text="Fan",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=250)
            loadval = tk.Label(window, text=str(truncate(dicthour["fan"],1))+" hr/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            loadval.place(x=790,y=250)
            load = tk.Label(window, text="Charger",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=300)
            loadval = tk.Label(window, text=str(truncate(dicthour["charger"],1))+" hr/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            loadval.place(x=790,y=300)
            load = tk.Label(window, text="TV",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=350)
            loadval = tk.Label(window, text=str(truncate(dicthour["tv"],1))+" hr/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            loadval.place(x=790,y=350)
            load = tk.Label(window, text="Motor",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=400)
            loadval = tk.Label(window, text=str(truncate(dicthour["motor"],1))+" hr/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            loadval.place(x=790,y=400)
            load = tk.Label(window, text="Wetgrinder",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=450)
            if(flag==0):
                loadval = tk.Label(window, text=str(truncate(dicthour["wetgrinder"]*7,1))+" hr/week",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
                loadval.place(x=790,y=450)
            if(flag==1):
                loadval = tk.Label(window, text=str(truncate(dicthour["wetgrinder"],1))+" hr/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
                loadval.place(x=790,y=450)
            load = tk.Label(window, text="Mixer",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=500)
            loadval = tk.Label(window, text=str(truncate(dicthour["mixer"]*60,1))+" min/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            loadval.place(x=790,y=500)
            load = tk.Label(window, text="Ironbox",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=550)
            if(flag==0):
                loadval = tk.Label(window, text=str(truncate(dicthour["ironbox"]*7,1))+" hr/week",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
                loadval.place(x=790,y=550)
            if(flag==1):
                loadval = tk.Label(window, text=str(truncate(dicthour["ironbox"],1))+" hr/day",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
                loadval.place(x=790,y=550)
            if(flag==0):
                load = tk.Label(window,text = "Additional: (Fan/tv)",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold '))
                load.place(x=80,y=550)
                loadval = tk.Label(window,text =str(truncate(additionalfan,1))+'/'+str(truncate(additionaltv,3))+' hr/day',fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold '))
                loadval.place(x=300,y=550)
            if(flag == 1):
                load = tk.Label(window,text = "Additional amt.saved",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold '))
                load.place(x=80,y=550)
                loadval = tk.Label(window,text ='Rs. '+str(truncate(amt,1)),fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold '))
                loadval.place(x=300,y=550)
                
        else:
            load = tk.Label(window, text="INVALID AMOUNT",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') )
            load.place(x=600,y=350)
            
   
    
    cusname = tk.Label(window, text="Customer Name:",width=15  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusname.place(x=40, y=200)
    cusnameEntry = tk.Label(window, text=customerName,fg="red",width=15  ,height=1  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusnameEntry.place(x=230, y=200)
    cusname = tk.Label(window, text="Unit Consumed:",width=15  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusname.place(x=40, y=250)
    cusnameEntry = tk.Label(window, text=str(unit)+" kWh",fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusnameEntry.place(x=230, y=250)
    cusname = tk.Label(window, text="Bill Amount:",width=15  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusname.place(x=40, y=300)
    cusnameEntry = tk.Label(window, text= "Rs. "+str(consumed),fg="red",width=15  ,height=1  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusnameEntry.place(x=230, y=300)
    cusname = tk.Label(window, text="Est. Amount: ",width=15  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusname.place(x=40, y=350)
    cusnameEntry = tk.Label(window, text="Rs. "+str(estimatedcost),fg="red" ,width=15  ,height=1 ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusnameEntry.place(x=230, y=350)
    cusname = tk.Label(window, text="Slab: "+str(slab),width=15  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusname.place(x=40, y=400)
    cusnameEntry = tk.Label(window, text=str(percent)+ " %",fg="red",width=15  ,height=1  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusnameEntry.place(x=230, y=400)
    cusname = tk.Label(window, text="Predict Amt: ",width=15  ,height=1  ,fg="red"  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusname.place(x=40, y=450)
    cusnameEntry = tk.Entry(window, fg="red",width=15  ,bg="yellow" ,font=('times', 15, ' bold ') ) 
    cusnameEntry.place(x=230, y=450)
    cusname = tk.Button(window, text="Forecast", command=loadforecast  ,fg="red"  ,bg="yellow"  ,width=20  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
    cusname.place(x=120,y=500)
  
startButton = tk.Button(window, text="Start", command=service  ,fg="red"  ,bg="yellow"  ,width=20  ,height=1 ,activebackground = "Red" ,font=('times', 15, ' bold '))
startButton.place(x=380, y=120)

window.mainloop()


#check the folder
