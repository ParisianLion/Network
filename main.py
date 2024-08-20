#import all libraries
import pandas as pd
import csv
import os
import random
from datetime import datetime



#import all functions
from BuildingData import *
from SelectingProcess import *
from CreatingMessage import *


#import all data
FILEPATH_RELATIONSHIPFOLDER = "/Users/lucanardinocchi/Desktop/Network/Data/Relationships"
FILEPATH_TRANSCRIPTFOLDER = "/Users/lucanardinocchi/Desktop/Network/Data/Transcripts"

ID = 0

FILEPATH_INDIVIDUALDATA = "/Users/lucanardinocchi/Desktop/Network/Data/People/People.csv"
FILEPATH_RELATIONSHIPDATA = f"/Users/lucanardinocchi/Desktop/Network/Data/Relationships/{ID}.csv"
FILEPATH_TRANSCRIPTDATA = f"/Users/lucanardinocchi/Desktop/Network/Data/Transcripts/{ID}.csv"

API_TOKEN = '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'



IndividualData = pd.read_csv("/Users/lucanardinocchi/Desktop/Network/Data/People/People.csv", sep=',', header=0, index_col=False)





'''Update Data'''

NumInsertsIndividual = int(input("How many people did you meet today?"))
x1 = 0
while x1 < int(NumInsertsIndividual):
    insert_individual(FILEPATH_INDIVIDUALDATA)
    x1 += 1

NumInsertsInteractions = int(input("How many people did you see today?"))

x2 = 0
while x2 < NumInsertsInteractions:
    ID = input(f'What is the Individual ID of interaction {x2}?')
    insert_interaction(f"/Users/lucanardinocchi/Desktop/Network/Data/Relationships/{ID}.csv")
    x2 += 1


print(len(IndividualData))

for i in range(len(IndividualData)):
    ID = i
    print(ID)
    update_daily_csv(f"/Users/lucanardinocchi/Desktop/Network/Data/Relationships/{ID}.csv")
    print(f"/Users/lucanardinocchi/Desktop/Network/Data/Relationships/{ID}.csv")





'''Generate Messages'''

for i in range(len(IndividualData)):
    
    ID = i
    
    infodict = combine_info(FILEPATH_INDIVIDUALDATA, f"/Users/lucanardinocchi/Desktop/Network/Data/Relationships/{ID}.csv", ID)
    print(infodict)

    dfID = pd.DataFrame([infodict])
    print(dfID)

    condition = select_action(dfID)

    create_temp_csv("/Users/lucanardinocchi/Desktop/Network/Messages/Temporary/temp.csv")

    action = get_action_prompt(condition)

    prompt = create_prompt(action, infodict)
    print(prompt)

    msg = generate_response(prompt, model="meta-llama/Llama-2-70b-chat-hf", token="API_TOKEN")
    print(msg)

    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    append_to_csv("/Users/lucanardinocchi/Desktop/Network/Messages/Temporary/temp.csv", time=time, reciever=infodict[PhoneNumber], message=msg)





'''Send Messages'''

process_messages("/Users/lucanardinocchi/Desktop/Network/Messages/Temporary/temp.csv")

date_str = datetime.now().strftime('%Y%m%d')
dfapproved = pd.read_csv(f"/Users/lucanardinocchi/Desktop/Network/Messages/Approved/Approved{date_str}.csv", sep=',', header=0, index_col=False)


for i in range(len(dftemp)):
    
    #check this index
    recipient_number = dfapproved[1][i]
    message = dfapproved[2][i]
    
    send_imessage(recipient_number, message, csv_r_path=None, csv_t_path=None)
    
    update_csv_r(#insert arguments)
    update_csv_t(#insert arguments)

delete_csv("/Users/lucanardinocchi/Desktop/Network/Messages/Approved/Approved{date_str}.csv")





'''Analyse Results'''

#print graph of inflow
#what are the plays I can make (ie levers)? and what are the mettrics they affect? print these metrics.



