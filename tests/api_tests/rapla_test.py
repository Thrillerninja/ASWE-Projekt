import datetime
import unittest
import unittest.mock
from unittest.mock import patch, MagicMock

from api.calendar_api.cal import Calendar, Lecture, Appointment
from api.calendar_api.rapla import create_calendar_from_rapla



class TestCreateCalendarFromRapla(unittest.TestCase):

    def setUp(self):
        self.VALID_URL = "https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22A&day=30&month=9&year=2024&pages=20"
        self.INVALID_URL = "https://example.com/invalid"

    def test_create_calendar_from_rapla_valid_url(self):
        calendar = create_calendar_from_rapla(self.VALID_URL)
        self.assertIsInstance(calendar, Calendar)
        self.assertGreater(len(calendar.appointments), 0)
        # Überprüfen, ob die Termine richtig sortiert sind
        for i in range(1, len(calendar.appointments)):
            self.assertLessEqual(calendar.appointments[i-1].datetime_start.astimezone(tz=None), calendar.appointments[i].datetime_start.astimezone(tz=None))
        # Überprüfen, ob die Termine gültige Daten haben
        for appointment in calendar.appointments:
            self.assertIsInstance(appointment, (Lecture, Appointment))
            self.assertIsInstance(appointment.datetime_start, datetime.datetime)
            self.assertIsInstance(appointment.datetime_end, datetime.datetime)
            self.assertLess(appointment.datetime_start, appointment.datetime_end)
            self.assertTrue(appointment.color.startswith("#"))
            self.assertRegex(appointment.color, r'^#[0-9a-fA-F]{6}$')


    @patch('api.calendar_api.rapla.logger')
    def test_create_calendar_from_rapla_invalid_url(self, mock_logger):
        # Dieser Test erwartet, dass die URL einen Fehler zurückgibt
        mock_logger.error = MagicMock()
        create_calendar_from_rapla(self.INVALID_URL)
        mock_logger.error.assert_called_once()


    def test_create_calendar_from_rapla_partial_data(self):
        partial_data_url = "https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22A"
        calendar = create_calendar_from_rapla(partial_data_url)
        self.assertIsInstance(calendar, Calendar)
        self.assertGreater(len(calendar.appointments), 0)
        for appointment in calendar.appointments:
            self.assertIsInstance(appointment, (Lecture, Appointment))
            self.assertIsInstance(appointment.datetime_start, datetime.datetime)
            self.assertIsInstance(appointment.datetime_end, datetime.datetime)
            self.assertLess(appointment.datetime_start, appointment.datetime_end)
            self.assertTrue(appointment.color.startswith("#"))
            self.assertRegex(appointment.color, r'^#[0-9a-fA-F]{6}$')



    if __name__ == '__main__':
        unittest.main()