import csv
import pandas as pd
import os

import main.models
from main.models import BillEntry
def add_data(data1, data2,data3):

    created = BillEntry()
    created.category = data1
    created.name = data2
    created.cost = data3
    created.save()
    print("Created: {}".format(str(created)))




def populate():

    data= pd.read_excel('entry.xlsm', index_col=None)
    data.to_csv('entry.csv', encoding='utf-8',index=False)

    with open('entry.csv','r') as csvfile:
             csv_reader = csv.reader(csvfile, delimiter=',')
             next(csv_reader)
             for line in csv_reader:
                 category=line[0]
                 name=line[1]
                 cost =line[2]
                 add_data(category,name,cost)


if __name__ == "__main__":
    populate()
