import pytest
import datetime
import json
import unittest
from unittest.mock import patch

from api.calendar_api.cal import Calendar, Appointment, Lecture


class TestNewsAPI(unittest.TestCase):

    def setUp(self):
        # Testdaten
        self.now = datetime.datetime.now()
        self.future_appointment = Appointment("Future Meeting", self.now + datetime.timedelta(days=1), self.now + datetime.timedelta(days=2))
        self.past_appointment = Appointment("Past Meeting", self.now - datetime.timedelta(days=1), self.now)

    # ============================
    # Test für die Calendar-Klasse
    # ============================

    def test_calendar_initialization(self):
        calendar = Calendar()
        self.assertEqual(calendar.appointments, [])

    def test_calendar_repr_and_str(self):
        calendar = Calendar([self.future_appointment])
        self.assertEqual(repr(calendar), str(calendar))
        self.assertEqual(repr(calendar), str(self.future_appointment))


    def test_calendar_add_appointments(self):
        calendar = Calendar()
        calendar.add_appointments([self.future_appointment])
        self.assertEqual(len(calendar.appointments), 1)
        self.assertEqual(calendar.appointments[0], self.future_appointment)


    def test_calendar_sort(self):
        calendar = Calendar([self.future_appointment, self.past_appointment])
        calendar.sort()
        self.assertEqual(calendar.appointments[0], self.past_appointment)  # Erstes Element sollte das vergangene Meeting sein


    def test_calendar_toJSON(self):
        calendar = Calendar([self.future_appointment])
        expected_json = [self.future_appointment.toJSON()]
        self.assertEqual(calendar.toJSON(), expected_json)


    def test_calendar_save(self, tmp_path):
        calendar = Calendar([self.future_appointment])
        file_path = tmp_path / "calendar.json"
        print("filepath:", file_path)
        calendar.save(file_path)
        with open(file_path, "r") as f:
            data = f.read()
        expected_json = json.dumps(calendar.toJSON(), indent=4, ensure_ascii=False)
        self.assertEqual(data, expected_json)


    def test_calendar_get_next_appointment(self):
        calendar = Calendar([self.past_appointment, self.future_appointment])
        next_appointment = calendar.get_next_appointment(self.now)
        self.assertEqual(next_appointment, self.future_appointment)


    def test_calendar_get_next_appointment_no_future(self):
        calendar = Calendar([self.past_appointment])
        next_appointment = calendar.get_next_appointment(self.now)
        self.assertEqual(next_appointment, None)



    # ============================
    # Test für die Appointment-Klasse
    # ============================


    def test_appointment_initialization(self):
        appointment = Appointment("Test Meeting", self.now, self.now + datetime.timedelta(hours=1))
        self.assertEqual(appointment.title, "Test Meeting")
        self.assertEqual(appointment.datetime_start, self.now)
        self.assertEqual(appointment.datetime_end, self.now + datetime.timedelta(hours=1))


    def test_appointment_toJSON(self):
        appointment = Appointment("Test Meeting", self.now, self.now + datetime.timedelta(hours=1))
        expected_json = {
            'start': appointment.datetime_start.strftime("%Y-%m-%d_%H:%M:%S"),
            'end': appointment.datetime_end.strftime("%Y-%m-%d_%H:%M:%S"),
            'title': appointment.title,
            'color': appointment.color,
        }
        self.assertEqual(appointment.toJSON(), expected_json)



    # ============================
    # Test für die Lecture-Klasse
    # ============================


    def test_lecture_initialization(self):
        lecture = Lecture("Math Lecture", self.now, self.now + datetime.timedelta(hours=2), "#FFFFFF", "Dr. Smith", "Room 101")
        self.assertEqual(lecture.title, "Math Lecture")
        self.assertEqual(lecture.lecturer, "Dr. Smith")
        self.assertEqual(lecture.room, "Room 101")

    def test_lecture_str(self):
        lecture = Lecture("Math Lecture", self.now, self.now + datetime.timedelta(hours=2), "#FFFFFF", "Dr. Smith", "Room 101")
        expected_str = f"{self.now} | {self.now + datetime.timedelta(hours=2)} | Math Lecture | #FFFFFF | Room 101 | Dr. Smith"
        self.assertEqual(str(lecture), expected_str)


    def test_lecture_toJSON(self):
        lecture = Lecture("Math Lecture", self.now, self.now + datetime.timedelta(hours=2), "#FFFFFF", "Dr. Smith", "Room 101")
        expected_json = {
            'start': lecture.datetime_start.strftime("%Y-%m-%d_%H:%M:%S"),
            'end': lecture.datetime_end.strftime("%Y-%m-%d_%H:%M:%S"),
            'title': lecture.title,
            'color': lecture.color,
            'room': lecture.room,
            'lecturer': lecture.lecturer,
        }
        self.assertEqual(lecture.toJSON(), expected_json)


if __name__ == '__main__':
    unittest.main()