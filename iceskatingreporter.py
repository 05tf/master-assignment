from track import Track
from event import Event
from skater import Skater
from datetime import datetime
import sqlite3

class Reporter:

    # How many skaters are there? -> int
    def total_amount_of_skaters(self) -> int:   
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()
        
        cur.execute("SELECT * FROM skaters")
        skaters_table = cur.fetchall()

        con.close()

        return len(skaters_table)
    
    # What is the highest track? -> Track
    def highest_track(self) -> Track:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        #fetch alle altitudes
        altitudes_row = cur.execute("SELECT altitude FROM tracks").fetchall()

        max_altitude = None
        for row in altitudes_row:
            altitude = row[0]
            if max_altitude is None or altitude > max_altitude:
                max_altitude = altitude

        # Fetch row die matched met de max altitude 
        max_altitude_row = cur.execute("SELECT id, name, city, country, outdoor, altitude FROM tracks WHERE altitude = ?", (max_altitude,)).fetchone()
        con.close()

        max_altitude_track = Track(id=max_altitude_row[0], name=max_altitude_row[1], city=max_altitude_row[2], country=max_altitude_row[3], outdoor=max_altitude_row[4], altitude=max_altitude_row[5])
        return(max_altitude_track)

    # What is the longest and shortest event? -> tuple[Event, Event]
    def longest_and_shortest_event(self) -> tuple[Event, Event]:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()
        
        events_db = cur.execute("SELECT * FROM events").fetchall()
        longest_event = None
        shortest_event = None

        for x in events_db:
            if longest_event is None or x[5] > longest_event:
                longest_event = x[5]

        for y in events_db:
            if shortest_event is None or y[5] < shortest_event:
                shortest_event = y[5]
        
        longest_event_row = cur.execute("SELECT id, name, track_id, date, distance, duration, laps, winner, category FROM events WHERE duration = ?", (longest_event,)).fetchone()
        shortest_event_row = cur.execute("SELECT id, name, track_id, date, distance, duration, laps, winner, category FROM events WHERE duration = ?", (shortest_event,)).fetchone()
        con.close()

        longest_event_obj = Event(id=longest_event_row[0], name=longest_event_row[1], track_id=longest_event_row[2], date=longest_event_row[3], distance=longest_event_row[4], duration=longest_event_row[5], laps=longest_event_row[6], winner=longest_event_row[7], category=longest_event_row[8])
        shortest_event_obj = Event(id=shortest_event_row[0], name=shortest_event_row[1], track_id=shortest_event_row[2], date=shortest_event_row[3], distance=shortest_event_row[4], duration=shortest_event_row[5], laps=shortest_event_row[6], winner=shortest_event_row[7], category=shortest_event_row[8])

        longest_shortest_tuple = (longest_event_obj, shortest_event_obj)
        return longest_shortest_tuple
    
    # Which event has the most laps for the given track_id -> tuple[Event, ...]
    def events_with_most_laps_for_track(self, track_id: int) -> tuple[Event, ...]:
        pass

    # Which skaters have made the most events -> tuple[Skater, ...]
    # Which skaters have made the most succesful events -> tuple[Skater, ...]
    def skaters_with_most_events(self, only_wins: bool = False) -> tuple[Skater, ...]:
        pass

    # Which track has the most events -> Track
    def tracks_with_most_events(self) -> tuple[Track, ...]:
        pass

    # Which track had the first event? -> Event
    # Which track had the first outdoor event? -> Event
    def get_first_event(self, outdoor_only: bool = False) -> Event:
        pass

    # Which track had the latest event? -> event
    # Which track had the latetstoutdoor event? -> event
    def get_latest_event(self, outdoor_only: bool = False) -> Event:
        pass

    # Which skaters have raced track Z between period X and Y? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters on Track Z between X and Y.csv`
    # example: `Skaters on Track Kometa between 2021-03-01 and 2021-06-01.csv`
    # date input always in format: YYYY-MM-DD
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_that_skated_track_between(self, track: Track, start: datetime, end: datetime, to_csv: bool = False) -> tuple[Skater, ...]:
        pass

    # Which tracks are located in country X? ->tuple[Track, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Tracks in country X.csv`
    # example: `Tracks in Country USA.csv`
    # otherwise it should just return the value as tuple(Track, ...)
    # CSV example (this are also the headers):
    #   id, name, city, country, outdoor, altitude
    def get_tracks_in_country(self, country: str, to_csv: bool = False) -> tuple[Track, ...]:
        pass

    # Which skaters have nationality X? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters with nationality X.csv`
    # example: `Skaters with nationality GER.csv`
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_with_nationality(self, nationality: str, to_csv: bool = False) -> tuple[Skater, ...]:
        pass
