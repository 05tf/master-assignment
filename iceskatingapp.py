import os
import sys
import json
import sqlite3

from skater import Skater
from track import Track
from event import Event
        

def fill_tracks_db(con, cur, ice_skating_data):

    for event in ice_skating_data:
        track = event["track"]
        cur.execute("INSERT OR IGNORE INTO tracks VALUES (?, ?, ?, ?, ?, ?)", 
                        (track['id'],
                        track['name'],
                        track['city'],
                        track['country'],
                        track['isOutdoor'],
                        track['altitude']))
    con.commit()
def time_converter(time_string):
    minutes, seconds = map(float, time_string.split(":"))
    return round((minutes * 60) + seconds, 2)

def fill_events_db(con, cur, ice_skating_data):

    for event in ice_skating_data:
        cur.execute("INSERT OR IGNORE INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (event['id'],
                        event['title'],
                        event['track']['id'],
                        event['start'],
                        event['distance']['distance'],
                        time_converter(event['results'][0]['time']),
                        event['distance']['lapCount'],
                        event['results'][0]['skater']['firstName'] + \
                        " " + event['results'][0]['skater']['lastName'],
                        event['category'],))
    con.commit()

def fill_skaters_db(con, cur, ice_skating_data):

    for event in ice_skating_data:
        for result in event["results"]:
            skater = result["skater"]
            cur.execute("INSERT OR IGNORE INTO skaters VALUES (?, ?, ?, ?, ?, ?)", 
                        (skater['id'],
                        skater['firstName'],
                        skater['lastName'],
                        skater['country'],
                        skater['gender'],
                        skater['dateOfBirth']))
    con.commit()

def fill_event_skaters_db(con, cur, ice_skating_data):
    for event in ice_skating_data:
        id_event = event['id']
        for result in event["results"]:
            skater = result["skater"]['id']
            cur.execute("INSERT OR IGNORE INTO event_skaters VALUES (?, ?)",
                        (skater, id_event))
    con.commit()
def main():

    with open('mini_events.json', 'r') as json_file:
        ice_skating_data = json.load(json_file)

    con = sqlite3.connect('iceskatingapp.db')
    cur = con.cursor()

    fill_tracks_db(con, cur, ice_skating_data)
    fill_events_db(con, cur, ice_skating_data)
    fill_skaters_db(con, cur, ice_skating_data)
    fill_event_skaters_db(con, cur, ice_skating_data)
    con.close()

    
if __name__ == "__main__":
    main()
