# open file & create csvreader
import csv
from main.models import BillEntry

with open('entry.csv', newline='') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
         for line in csv file:
             line = parse line to a list

     # add some custom validation\parsing for some of the fields
             billentry = BillEntry(category=line[1], name=line[2] ,cost=line[3] )
             try:
                 billentry.save()
             except:
         # if the're a problem anywhere, you wanna know about it
                 print "there was a problem with line", i

#loop:
