from datetime import datetime
import sqlite3


class Event:

    def __init__(self, id: int, name: str, track_id: int, date: datetime, distance: int, duration: float, laps: int, winner: str, category: str):
        self.id = id
        self.name = name
        self.track_id = track_id
        self.date = date
        self.distance = distance
        self.duration = duration
        self.laps = laps
        self.winner = winner
        self.category = category

    def add_skater(self, skater_id: int):
        from skater import Skater
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        check_if_exists = cur.execute("SELECT * FROM event_skaters WHERE skater_id = ? AND event_id = ?", 
                                      (skater_id, self.id)).fetchone()

        if not check_if_exists:
            add_skater = cur.execute("INSERT INTO event_skaters (skater_id, event_id) VALUES (?, ?)", 
                                     (skater_id, self.id)).commit().close()
            return True
        else:
            con.close()
            return False

    def get_skaters(self) -> list:
        from skater import Skater
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        skater_ids = cur.execute("SELECT skater_id FROM event_skaters WHERE event_id = ?", 
                                 (self.id,)).fetchall()

        for skater_id in skater_ids:
            skater_data = cur.execute("SELECT * FROM skaters WHERE id = ?", 
                                      (skater_id[0],)).fetchone()
            con.close()
            return [Skater(*skater_data)]

    def get_track(self):
        from track import Track
        con = sqlite3.connect('iceskatingapp.db')
        cur = con.cursor()

        track_data = cur.execute("SELECT * FROM tracks WHERE id = ?", 
                                 (self.track_id,)).fetchone()
        con.close()
        return [Track(*track_data)] if track_data else []

    def convert_date(self, to_format: str) -> str:
        givendate = datetime.strptime(self.date, "%Y-%m-%d")
        return givendate.strftime(to_format)

    def convert_duration(self, to_format: str) -> str:
        pass

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
