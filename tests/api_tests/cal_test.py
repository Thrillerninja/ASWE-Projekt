import pytest
import datetime
import json

from api.calendar_api.cal import Calendar, Appointment, Lecture

# Testdaten
now = datetime.datetime.now()
future_appointment = Appointment("Future Meeting", now + datetime.timedelta(days=1), now + datetime.timedelta(days=2))
past_appointment = Appointment("Past Meeting", now - datetime.timedelta(days=1), now)

# Test für die Calendar-Klasse

def test_calendar_initialization():
    calendar = Calendar()
    assert calendar.appointments == []

def test_calendar_repr_and_str():
    calendar = Calendar([future_appointment])
    assert str(calendar) == repr(calendar)
    assert str(calendar) == str(future_appointment)


def test_calendar_add_appointments():
    calendar = Calendar()
    calendar.add_appointments([future_appointment])
    assert len(calendar.appointments) == 1
    assert calendar.appointments[0] == future_appointment


def test_calendar_sort():
    calendar = Calendar([future_appointment, past_appointment])
    calendar.sort()
    assert calendar.appointments[0] == past_appointment  # Erstes Element sollte das vergangene Meeting sein


def test_calendar_toJSON():
    calendar = Calendar([future_appointment])
    expected_json = [future_appointment.toJSON()]
    assert calendar.toJSON() == expected_json


def test_calendar_save(tmp_path):
    calendar = Calendar([future_appointment])
    file_path = tmp_path / "calendar.json"
    print("filepath:", file_path)
    calendar.save(file_path)
    with open(file_path, "r") as f:
        data = f.read()
    expected_json = json.dumps(calendar.toJSON(), indent=4, ensure_ascii=False)
    assert data == expected_json


def test_calendar_get_next_appointment():
    calendar = Calendar([past_appointment, future_appointment])
    next_appointment = calendar.get_next_appointment(now)
    assert next_appointment == future_appointment


def test_calendar_get_next_appointment_no_future():
    calendar = Calendar([past_appointment])
    next_appointment = calendar.get_next_appointment(now)
    assert next_appointment is None




# Test für die Appointment-Klasse


def test_appointment_initialization():
    appointment = Appointment("Test Meeting", now, now + datetime.timedelta(hours=1))
    assert appointment.title == "Test Meeting"
    assert appointment.datetime_start == now
    assert appointment.datetime_end == now + datetime.timedelta(hours=1)


def test_appointment_toJSON():
    appointment = Appointment("Test Meeting", now, now + datetime.timedelta(hours=1))
    expected_json = {
        'start': appointment.datetime_start.strftime("%Y-%m-%d_%H:%M:%S"),
        'end': appointment.datetime_end.strftime("%Y-%m-%d_%H:%M:%S"),
        'title': appointment.title,
        'color': appointment.color,
    }
    assert appointment.toJSON() == expected_json




# Test für die Lecture-Klasse


def test_lecture_initialization():
    lecture = Lecture("Math Lecture", now, now + datetime.timedelta(hours=2), "#FFFFFF", "Dr. Smith", "Room 101")
    assert lecture.title == "Math Lecture"
    assert lecture.lecturer == "Dr. Smith"
    assert lecture.room == "Room 101"

def test_lecture_str():
    lecture = Lecture("Math Lecture", now, now + datetime.timedelta(hours=2), "#FFFFFF", "Dr. Smith", "Room 101")
    assert str(lecture) == f"{now} | {now + datetime.timedelta(hours=2)} | Math Lecture | #FFFFFF | Room 101 | Dr. Smith"


def test_lecture_toJSON():
    lecture = Lecture("Math Lecture", now, now + datetime.timedelta(hours=2), "#FFFFFF", "Dr. Smith", "Room 101")
    expected_json = {
        'start': lecture.datetime_start.strftime("%Y-%m-%d_%H:%M:%S"),
        'end': lecture.datetime_end.strftime("%Y-%m-%d_%H:%M:%S"),
        'title': lecture.title,
        'color': lecture.color,
        'room': lecture.room,
        'lecturer': lecture.lecturer,
    }
    assert lecture.toJSON() == expected_json
