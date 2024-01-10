from datetime import datetime

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

    def add_skater(self):
        pass
    def get_skaters(self) -> list:
        pass
    def get_track(self):
        pass
    def convert_date(self) -> str:
        pass
    def convert_duration(self) -> str:
        pass
    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
