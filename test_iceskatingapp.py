from skater import Skater
from event import Event
from track import Track
from datetime import datetime, date
import pytest

# Test to check if the age of a skater is correct based on the date_of_birth
def test_age_of_skater():
    agetester = Skater(None, None, None, None, None, date(2000, 9, 15))

    expected_result = datetime.now().date().year - date(2000, 9, 15).year
    assert agetester.get_age() == expected_result

test_age_of_skater()
# Test to check if the amount of events for a specific skater is returned correctly
def test_amount_of_events_of_skater():
    raise NotImplementedError()

# Test to check if the amount of events for a specific track is returned correctly
def test_amount_of_events_of_track():
    raise NotImplementedError()

# Test to check if the returned date matches the specified format for that event date
def test_event_date_conversion():
    raise NotImplementedError()

# Test to check if the duration is converted from 1H19 to the specified format
def test_event_duration_conversion():
    raise NotImplementedError()

# Test to check the amount of skaters on a specified event
def test_amount_of_skaters_on_event():
    raise NotImplementedError()

# Test to validate if the given track of a specified event is correct
def test_track_on_event():
    raise NotImplementedError()
