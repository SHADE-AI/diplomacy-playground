#!/usr/bin/env python3

import json
import sys
import argparse
import os
import mariadb

table_schema = {
        "game_id":"VARCHAR(255)",
        "austria_controler":"VARCHAR(255)",
        "england_controler":"VARCHAR(255)",
        "france_controler":"VARCHAR(255)",
        "germany_controler":"VARCHAR(255)",
        "italy_contrler":"VARCHAR(255)",
        "russia_controler":"VARCHAR(255)",
        "turkey_contrler":"VARCHAR(255)",
        "game_state":"VARCHAR(255)",
        "last_season":"VARCHAR(255)",
        "austria_centers":"INT",
        "england_centers":"INT",
        "france_centers":"INT",
        "germany_centers":"INT",
        "italy_centers":"INT",
        "russia_centers":"INT",
        "turkey_centers":"INT",
        "is_draw":"BOOLEAN",
        "note":"VARCHAR(255)",
}

def print_summary(fname):
    data = []
    
    with open(fname) as file:
        data=json.load(file)
    controlers=""
    for key in data["powers"]: 
#        controlers = controlers + key + '-'
        controlers = controlers + "'";
        for v in data["powers"][key]['controller'].values():
            controlers = controlers +  v + '-'
        controlers = controlers[:-1] 
        controlers = controlers + "',"
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
    note = data['note'].replace(',',' -')

    return("('"+data['game_id'] +"'"+"," + controlers + ',' + "'"+data['phase'] +"'"+ "," + "'"+last_season +"'"+","+center_string +"," + str(draw) + "," + "'"+note+"')")

def create_table(table_name):
    statement = "create table "+ table_name +"("
    for column in table_schema.keys():
        statement = statement + column + " " + table_schema[column] +" ,"
    statement = statement[:-1] + ")"
    return statement

def get_insert(table_name):
    cmd = "insert into "+table_name+" ( "
    for k in table_schema.keys():
        cmd = cmd + k +","

    cmd = cmd[:-1] + ")"
    return cmd


def main():
    parser = argparse.ArgumentParser(description="print outcome of diplomacy game")
    parser.add_argument('host',help="database hostaname to work with")
    parser.add_argument('database',help="database to work with")
    parser.add_argument('table',help="table to insert into")
    parser.add_argument('--create',help="create new table",action="store_true")
    parser.add_argument('--drop',help="drop old table and create new table",action="store_true")
    parser.add_argument('inputFileNames',nargs='+',help="input diplomacy game json files.")
    args=parser.parse_args()

    user = os.getenv("DB_USER")
    passwd = os.getenv("DB_PASSWORD")
    if not user or not passwd:
        print("DB_USER and DB_PASSWORD must be set as environment variables for database access")
        sys.exit(1)
    host = args.host
    db = args.database
    conn = None
    try:
        conn = mariadb.connect(
            user=user,
            password=passwd,
            host=host,
            port=3306,
            database=db
    
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    first = True
    table = args.table
    cur = conn.cursor()
    if args.drop:
#        print("drop table " + table)
        try:
            cur.execute("drop table " + table)
        except mariadb.Error as e:
            print(f"Error: {e}")
            exit(1)
    if args.create or args.drop:
#        print(create_table(table))
        try:
            cur.execute(create_table(table))
        except mariadb.Error as e:
            print(f"Error: {e}")
            exit(1)
    cmd = get_insert(table)
    cmd = cmd + " values "
    for f in args.inputFileNames:
        line = print_summary(f)
        if not first:
            cmd = cmd + ','+line
        else:
            cmd = cmd + line
            first=False
    cmd = cmd +';'
#    print(cmd)
    try:
        cur.execute(cmd)
    except mariadb.Error as e:
        print(f"Error: {e}")
    print(f"{cur.rowcount}, details inserted")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
