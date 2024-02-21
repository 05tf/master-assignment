from track import Track
from event import Event
from skater import Skater
from datetime import datetime
import sqlite3
import csv

class Reporter:

    # How many skaters are there? -> int
    def total_amount_of_skaters(self) -> int:   
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()
        
        skaters_table = cur.execute("SELECT * FROM skaters").fetchall()
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

        for events_data_longest in events_db:
            if longest_event is None or events_data_longest[5] > longest_event:
                longest_event = events_data_longest[5]

        for events_data_shortest in events_db:
            if shortest_event is None or events_data_shortest[5] < shortest_event:
                shortest_event = events_data_shortest[5]
        
        longest_event_row = cur.execute("SELECT id, name, track_id, date, distance, duration, laps, winner, category FROM events WHERE duration = ?", (longest_event,)).fetchone()
        shortest_event_row = cur.execute("SELECT id, name, track_id, date, distance, duration, laps, winner, category FROM events WHERE duration = ?", (shortest_event,)).fetchone()
        con.close()

        longest_event_obj = Event(id=longest_event_row[0], name=longest_event_row[1], track_id=longest_event_row[2], date=longest_event_row[3], distance=longest_event_row[4], duration=longest_event_row[5], laps=longest_event_row[6], winner=longest_event_row[7], category=longest_event_row[8])
        shortest_event_obj = Event(id=shortest_event_row[0], name=shortest_event_row[1], track_id=shortest_event_row[2], date=shortest_event_row[3], distance=shortest_event_row[4], duration=shortest_event_row[5], laps=shortest_event_row[6], winner=shortest_event_row[7], category=shortest_event_row[8])

        longest_shortest_tuple = (longest_event_obj, shortest_event_obj)
        return longest_shortest_tuple

    # Which event has the most laps for the given track_id -> tuple[Event, ...]
    def events_with_most_laps_for_track(self, track_id: int) -> tuple[Event, ...]:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        non_tuple_list = []
        
        desc_events = cur.execute("SELECT laps FROM events WHERE track_id = ? ORDER BY laps DESC"  , (track_id,)).fetchone()
        extra_laps_events = cur.execute("SELECT * FROM events WHERE laps = ? AND track_id = ? ", (desc_events[0] , track_id) ).fetchall()

        con.close()

        for event in extra_laps_events:
            event_obj = Event(*event)
            non_tuple_list.append(event_obj)

        tuple_list = tuple(non_tuple_list)
        return(tuple_list)

    # Which skaters have made the most events -> tuple[Skater, ...]
    # Which skaters have made the most succesful events -> tuple[Skater, ...]
    def skaters_with_most_events(self, only_wins: bool = False):
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        if only_wins:

            skater_most_wins = cur.execute("SELECT winner, COUNT(*) AS win_count FROM events WHERE winner IS NOT NULL GROUP BY winner ORDER BY win_count DESC ").fetchone()
            succesful_skater = skater_most_wins[0]
            skater_full = cur.execute("SELECT * FROM skaters WHERE id = ?", (succesful_skater,)).fetchone()
            skater_obj = Skater(*skater_full)
            skater_list = [skater_obj]
            con.close()
            return print(tuple(skater_list))

        else:
            skater_most_events = cur.execute("SELECT skater_id, COUNT(*) AS event_count FROM event_skaters GROUP BY skater_id ORDER BY event_count DESC ").fetchone()
            skater_id = skater_most_events[0]
            skater_full = cur.execute("SELECT * FROM skaters WHERE id = ?", (skater_id,)).fetchone()
            skater_obj = Skater(*skater_full)
            skater_list = [skater_obj]
            con.close()
            return print(tuple(skater_list))

    # Which track has the most events -> Track
    def tracks_with_most_events(self) -> tuple[Track, ...]:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        get_trackId_most_events = cur.execute("SELECT track_id, COUNT(*) AS event_count FROM events GROUP BY track_id ORDER BY event_count DESC LIMIT 1").fetchone()
        track_id = get_trackId_most_events[0]
        select_track = cur.execute("SELECT * FROM tracks WHERE id = ?", (track_id,)).fetchone()

        track_obj = [Track(*select_track)]
        track_obj_tuple = tuple(track_obj)
        return track_obj_tuple
    
    # Which track had the first event? -> Event
    # Which track had the first outdoor event? -> Event
    def get_first_event(self, outdoor_only: bool = False):
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        if outdoor_only:
            first_event_true = cur.execute("SELECT events.* FROM events JOIN tracks ON events.track_id = tracks.id WHERE 1 AND tracks.outdoor = 1 ORDER BY events.date LIMIT 1;").fetchone()
            track_id_first =(first_event_true[2])
            first_track = cur.execute("SELECT * FROM tracks WHERE id = ?", (track_id_first,)).fetchone()
            con.close()
            first_eventtrack_obj = Track(*first_track)
            return first_eventtrack_obj

        else:
            first_event_false = cur.execute("SELECT events.* FROM events JOIN tracks ON events.track_id = tracks.id WHERE 1 ORDER BY events.date LIMIT 1;").fetchone()
            track_id_first =(first_event_false[2])
            first_track = cur.execute("SELECT * FROM tracks WHERE id = ?", (track_id_first,)).fetchone()
            con.close()
            first_eventtrack_obj = Track(*first_track)
            return first_eventtrack_obj

    # Which track had the latest event? -> event
    # Which track had the latetstoutdoor event? -> event
    def get_latest_event(self, outdoor_only: bool = False) -> Event:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        if outdoor_only:
            latest_event_true = cur.execute("SELECT events.* FROM events JOIN tracks ON events.track_id = tracks.id WHERE 1 AND tracks.outdoor = 1 ORDER BY events.date DESC;").fetchone()
            track_id_latest =(latest_event_true[2])
            latest_track = cur.execute("SELECT * FROM tracks WHERE id = ?", (track_id_latest,)).fetchone()
            con.close()
            latest_eventtrack_obj = Track(*latest_track)
            return latest_eventtrack_obj

        else:
            latest_event_false = cur.execute("SELECT events.* FROM events JOIN tracks ON events.track_id = tracks.id WHERE 1 ORDER BY events.date DESC;").fetchone()
            track_id_latest =(latest_event_false[2])
            latest_track = cur.execute("SELECT * FROM tracks WHERE id = ?", (track_id_latest,)).fetchone()
            con.close()
            latest_eventtrack_obj = Track(*latest_track)
            return latest_eventtrack_obj

    # Which skaters have raced track Z between period X and Y? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters on Track Z between X and Y.csv`
    # example: `Skaters on Track Kometa between 2021-03-01 and 2021-06-01.csv`
    # date input always in format: YYYY-MM-DD
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    # id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_that_skated_track_between(self, track: Track, start: datetime, end: datetime, to_csv: bool = False) -> tuple[Skater, ...]:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        endtime = end.strftime("%Y-%m-%d")
        starttime = start.strftime("%Y-%m-%d")
        header = "id, first_name, last_name, nationality, gender, date_of_birth"
        file_name = f'Skaters on Track {track.name} between {starttime} and {endtime}.csv'


        #skaters die meededen op track between start and end date
        #pak unique rows skaters.all from skaters
        #join die rows van event_skaters met skaters.id
        #join rows id van event met event.id van event_skaters
        #waar event.track_id = track.id en event.date met BETWEEN en AND
        get_Skaters = cur.execute("SELECT DISTINCT skaters.* FROM skaters JOIN event_skaters ON skaters.id = event_skaters.skater_id JOIN events ON events.id = event_skaters.event_id WHERE events.track_id = ? AND events.date BETWEEN ? AND ? ORDER BY skaters.id ASC", 
                                  (track.id, starttime, endtime)).fetchall()

        if to_csv:
            with open(file_name, 'w') as csv_file:
                csv_file.write(header + '\n')
                for skater in get_Skaters:
                    csv_file.write(','.join(map(str, skater)) + '\n')
        else:
            return print(tuple(Skater(*skater) for skater in get_Skaters))
        
    # trek = Track(id=15, name="Ritten Arena", city="Callalbo", country="ITA", outdoor=1, altitude=1198)

    # get_skaters_that_skated_track_between(self=None, track=trek, start=datetime.strptime("2000-11-20", "%Y-%m-%d"), end=datetime.strptime("2022-11-21", "%Y-%m-%d"), to_csv=True)
    # get_skaters_that_skated_track_between(self=None, track=trek, start=datetime.strptime("2022-11-20", "%Y-%m-%d"), end=datetime.strptime("2022-11-21", "%Y-%m-%d"), to_csv=False)

    # Which tracks are located in country X? ->tuple[Track, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Tracks in country X.csv`
    # example: `Tracks in Country USA.csv`
    # otherwise it should just return the value as tuple(Track, ...)
    # CSV example (this are also the headers):
    #id, name, city, country, outdoor, altitude
    def get_tracks_in_country(self, country: str, to_csv: bool = False) -> tuple:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()
        header = "id, name, city, country, outdoor, altitude"
        file_name = f'Tracks in country {country}.csv'
        #get track ids
        select_track = cur.execute("SELECT * FROM tracks WHERE country = ?", (country,)).fetchall()
        con.close()
        if to_csv:
            with open(file_name, 'w') as csv_file:
                csv_file.write(header + '\n')
                for track in select_track:
                    csv_file.write(','.join(map(str, track)) + '\n')
        else:
            return tuple(Track(*track) for track in select_track)

    # Which skaters have nationality X? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters with nationality X.csv`
    # example: `Skaters with nationality GER.csv`
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    # id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_with_nationality(self, nationality: str, to_csv: bool = False) -> tuple:
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()
        header = "id, first_name, last_name, nationality, gender, date_of_birth"
        file_name = f'Skaters with nationality {nationality}.csv'

        #pak all van skaters met nationality
        select_skaters = cur.execute("SELECT * FROM skaters WHERE nationality = ?", (nationality,)).fetchall()
        con.close()
        if to_csv:
            with open(file_name, 'w') as csv_file:
                csv_file.write(header + '\n')
                for skater in select_skaters:
                    csv_file.write(','.join(map(str, skater)) + '\n')
        else:
            return tuple(Skater(*skater) for skater in select_skaters)