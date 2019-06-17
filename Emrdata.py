import csv
import pandas as pd
import os

import main.models
from main.models import BillEntry  #need to be changed


def add_data(data1, data2,data3):

    created = Emrdata()
    created.category = data1
    created.name = data2
    created.cost = data3
    created.save()
    print("Created: {}".format(str(created)))






def populate():

    data= pd.read_excel('EmrData.xlsx', index_col=None)
    data.to_csv('EmrData.csv', encoding='utf-8',index=False)

    with open('EmrData.csv','r') as csvfile:
             csv_reader = csv.reader(csvfile, delimiter=',')
             next(csv_reader)
             for line in csv_reader:                #need to be changed acc to Emr model 
                 category=line[0]
                 name=line[1]
                 cost =line[2]
                 add_data(category,name,cost)


if __name__ == "__main__":
    populate()
