
from classify import image_predict

import os, sys
import time

path = "/home/india/Documents/cnn-keras/test"

incorrect_data = {}


for item in os.listdir(path):
    temp = []
    print("-----------------------------------------------------------------"+str(item)+"----------------------------------------------------------------------------")
    for item1 in os.listdir(path+"/"+item):
        label = image_predict(image_path=path+"/"+item+"/"+item1)
        print()
        if str(label.split("\n")[0].split(":")[0]) == str(item):
            print(label)
        else:
            print(label,"-----------------------------------------",item1)
            temp.append(path+"/"+item+"/"+item1)
    
    incorrect_data[str(item)] = temp
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------")
    

print(incorrect_data)

