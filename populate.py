import csv
import pandas as pd
import os
from openpyxl import load_workbook
import sqlite3

import main.models
from main.models import Patient
def add_data(data1, data2,data3,data4):

    created = Patient()
    created.name = data1
    created.sex = data2
    created.phone = data3
    created.email = data4

    created.save()
    print("Created: {}".format(str(created)))






def populate():

    data= pd.read_excel('entryigen.xlsx', index_col=None)
    data.to_csv('entryigen.csv', encoding='utf-8',index=False)

    with open('entryigen.csv','r') as csvfile:
             csv_reader = csv.reader(csvfile, delimiter=',')
             next(csv_reader)
             for line in csv_reader:
                 category=line[0]
                 name=line[1]
                 sex=line[2]
                 phone =line[3]
                 email=line[4]
                 add_data(name,sex,phone,email)




if __name__ == "__main__":
    populate()
