from datetime import datetime, date

class Skater:

    def __init__(self, id, first_name, last_name, nationality, gender, date_of_birth) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.date_of_birth = date_of_birth

    def get_age(self, specific_date=None):
        if specific_date is None:
            specific_date = datetime.now().date() #pakt de alleen datum van nu (zonder tijd)
        age_year = specific_date - self.date_of_birth
        pass
    
    def get_events(self):
        pass

    
    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))
