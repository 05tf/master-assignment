from event import Event
from datetime import datetime, date
import os
import sys
import sqlite3

class Skater:

    #initialiseren van de attributes
    def __init__(self, id: int, first_name: str, last_name: str, nationality: str, gender: str, date_of_birth: date) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.date_of_birth = date_of_birth

    #pakt de datum van nu en berekent (year.now - birth.year) = age
    def get_age(self, date: datetime=None):
        if date is None:
            date = datetime.now().year
        age_year = date - self.date_of_birth.year
        return age_year
    
    def get_events(self):
        events = []

        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        select_event_ids = cur.execute("SELECT event_id FROM event_skaters WHERE skater_id = ?", (self.id,)).fetchall()

        for event_id in select_event_ids:
            select_events = cur.execute("SELECT * FROM events WHERE id = ?", (event_id[0],)).fetchall()
            events.extend([Event(*event) for event in select_events])

        return events


    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
