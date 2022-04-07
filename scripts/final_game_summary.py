#!/usr/bin/env python3

import json
import sys
import argparse


def print_summary(fname):
    data = []
    
    with open(fname) as file:
        data=json.load(file)
    controlers=""
    for key in data["powers"]: 
#        controlers = controlers + key + '-'
        for v in data["powers"][key]['controller'].values():
            controlers = controlers +  v + '-'
        controlers = controlers[:-1] 
        controlers = controlers +'|'
    controlers = controlers[:-1] 

    if data['phase'] != "COMPLETED":
        sys.stderr.write("Game file not completed " + fname)
        return
    draw = ',' in data['note']

    last_season = data['outcome'][0]

    centers = data['state_history'][last_season]['centers']
    center_string = ""
    for key in centers.keys():
        center_string = center_string +str(len(centers[key]))+","
    if len(center_string) != 0:
        center_string = center_string[:-1]


    print(data['game_id'] +"|" + controlers + '|' + data['phase'] + "|" + last_season +"|"+center_string +"|" + str(draw) + "|" + data['note'])

def print_header():
    print("game_id|austria_controler|england_controler|france_controler|germany_controler|italy_contrler|russia_controler|turkey_contrler|game_state|last_season|austria_centers|england_centers|france_centers|germany_centers|italy_centers|russia_centers|turkey_centers|is_draw|note")

def main():
    parser = argparse.ArgumentParser(description="print outcome of diplomacy game")
    parser.add_argument('inputFileNames',nargs='+',help="input diplomacy game json file. - for STDIN")
    args=parser.parse_args()
    print_header()
    for f in args.inputFileNames:
        print_summary(f)

if __name__ == "__main__":
    main()
