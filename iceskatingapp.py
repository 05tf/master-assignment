import os
import sys
import json
import sqlite3

from skater import Skater
from track import Track
from event import Event

# with open('events.json', 'r') as json_file:
#     ice_skating_data = json.load(json_file)

# con = sqlite3.connect('iceskatingapp.db')
# cur = con.cursor()

def empty_db(con, cur):

    cur.execute("DELETE FROM skaters")
    cur.execute("DELETE FROM events")
    cur.execute("DELETE FROM tracks")
    cur.execute("DELETE FROM event_skaters")
    con.commit()


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

def fill_events_db(con, cur, ice_skating_data):
    for event in ice_skating_data:
        for result in event["results"]:

            #minutes.seconds.miliseconds --> seconds.miliseconds
            time_str = event['results'][0]['time']
            try:
                minutes, seconds = map(float, time_str.split(":"))
                min_to_sec = minutes * 60
                converted_time = round(min_to_sec + seconds, 3)
            except:
                pass

            cur.execute("INSERT OR IGNORE INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (event['id'],
                        event['title'],
                        event['track']['id'],
                        event['start'],
                        event['distance']['distance'],
                        converted_time,
                        event['distance']['lapCount'],
                        result['skater']['firstName'] + " " + result['skater']['lastName'],
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

    with open('events.json', 'r') as json_file:
        ice_skating_data = json.load(json_file)

    con = sqlite3.connect('iceskatingapp.db')
    cur = con.cursor()

    empty_db(con, cur)
    fill_tracks_db(con, cur, ice_skating_data)
    fill_events_db(con, cur, ice_skating_data)
    fill_skaters_db(con, cur, ice_skating_data)
    fill_event_skaters_db(con, cur, ice_skating_data)

    con.close()

    
if __name__ == "__main__":
    main()
