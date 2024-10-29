import pytest
import datetime
import re

from api.calendar_api.cal import Calendar, Lecture, Appointment
from api.calendar_api.rapla import create_calendar_from_rapla

VALID_URL = "https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22A&day=30&month=9&year=2024&pages=20"
INVALID_URL = "https://example.com/invalid"


def test_create_calendar_from_rapla_valid_url():
    calendar = create_calendar_from_rapla(VALID_URL)
    assert isinstance(calendar, Calendar)
    assert len(calendar.appointments) > 0
    # Überprüfen, ob die Termine richtig sortiert sind
    for i in range(1, len(calendar.appointments)):
        assert calendar.appointments[i-1].datetime_start.astimezone(tz=None) <= calendar.appointments[i].datetime_start.astimezone(tz=None)
    # Überprüfen, ob die Termine gültige Daten haben
    for appointment in calendar.appointments:
        assert isinstance(appointment, (Lecture, Appointment))
        assert isinstance(appointment.datetime_start, datetime.datetime)
        assert isinstance(appointment.datetime_end, datetime.datetime)
        assert appointment.datetime_start < appointment.datetime_end
        assert appointment.color.startswith("#")
        assert re.match(r'^#[0-9a-fA-F]{6}$', appointment.color)


def test_create_calendar_from_rapla_invalid_url():
    # Dieser Test erwartet, dass die URL einen Fehler zurückgibt
    with pytest.raises(Exception) as excinfo:
        create_calendar_from_rapla(INVALID_URL)
    assert "Error:" in str(excinfo.value)  # Überprüfe, dass die Fehlermeldung die erwartete Struktur hat

