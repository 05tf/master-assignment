import os
import sys
import json
import sqlite3

class Track:

    def __init__(self, id: int, name: str, city: str, country: str, outdoor=False, altitude=None) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.country = country
        self.outdoor = outdoor
        self.altitude = altitude

    def get_events(self):
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        event_list = []

        get_event_ids = cur.execute("SELECT id FROM events WHERE track_id = ?", (self.id,)).fetchall()

        for event_id in get_event_ids:
            select_events = cur.execute("SELECT * FROM events WHERE id = ?", (event_id[0],)).fetchall()
            event_list.extend(select_events)

        con.close()
        return event_list


    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))