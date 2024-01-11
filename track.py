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

        get_event_id = cur.execute("SELECT id FROM events WHERE track_id = ?", (self.id)).fetchall()
        get_matching_event = cur.execute("SELECT * FROM events WHERE id = ?",(get_event_id)).fetchall()
        con.close()

        for event in get_matching_event:
            event_list.append(event)

        return event_list
    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
