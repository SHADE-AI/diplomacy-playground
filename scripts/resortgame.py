#!/usr/bin/env python3

#######################################
#
# resortgame.py - takes the JSON gamestate
# file and sorts it by season rather than 
# message, state, orders, and results
# to show the whole process of the game
#
# also includes looking at the DAIDE
# messages for PRP and finding the 
# responce to that and logging that
# with the original message showing
# YES or REJ
#
###########################################


import json
import argparse
import sys

def reformat(inFile,outFile):
    data=[]
    if inFile == '-':
        data=json.load(sys.stdin)
    else:
        with open(inFile) as file:
            data=json.load(file)

    game_id=data['game_id']
    messages={}
    for season in data['message_history'].keys():
        messages[season]=data['message_history'][season]
    orders={}
    for season in data['order_history'].keys():
        orders[season]=data['order_history'][season]
    results={}
    for season in data['result_history'].keys():
        results[season]=data['result_history'][season]
    states={}
    for season in data['state_history'].keys():
        states[season]=data['state_history'][season]

    history={}
    history["game_id"]=game_id

    for season in data['message_history'].keys():
        history[season]={}
        messages[season]=indexMessages(messages[season])
        history[season]["messages"]=messages[season]
        history[season]["orders"]=orders[season]
        history[season]["results"]=results[season]
        history[season]["states"]=states[season]
    if outFile == '-':
        json.dump(history,sys.stdout,indent=2)
    else:
        with open(outFile,'w+') as file:
            json.dump(history,file,indent=2)

def indexMessages(messages):
    
    for message in messages:
        if str(message['message']).startswith("PRP ("):
            for resp in messages:
                if message['message'] in resp['message']:
                    id=messages.index(message)
                    messages[id]['response']=resp['message']
    return messages

def main():
    parser = argparse.ArgumentParser(description="sort diplomacy file by season")
    parser.add_argument('inputFileName',help="input diplomacy game json file. - for STDIN")
    parser.add_argument('outputFileName',help="output sorted diplomacy game json file. - for STDOUT")
    args=parser.parse_args()
    reformat(args.inputFileName,args.outputFileName)

if __name__ == "__main__":
    main()
