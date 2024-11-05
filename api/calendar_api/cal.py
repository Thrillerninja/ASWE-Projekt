# Darf die Datei nicht calendar.py nennen, da es schon ein Modul mit dem Namen gibt

import json
import datetime



class Calendar:
    def __init__(self, appointments:list=[]) -> None:
        self.appointments = appointments
        if len(appointments) > 0:
            self.sort()

    def sort(self):
        def sort_func(appointment:Appointment):
            return appointment.datetime_start.astimezone(tz=None)
        self.appointments.sort(key=sort_func)

    def add_appointments(self, appointments:list):
        self.appointments += appointments
        self.sort()

    def __str__(self) -> str:
        self.sort()
        return "".join([str(appointment) for appointment in self.appointments])
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def toJSON(self):
        return [appointment.toJSON() for appointment in self.appointments]
    
    
    def save(self, filepath:str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.toJSON(), f, indent=4, ensure_ascii=False)

    def get_next_appointment(self, now:datetime.datetime):
        '''
        - ``now``: datetime: current time
        - return: Appointment: next appointment after ``now`` or None if there is no appointment
        '''
        for appointment in self.appointments:
            if now < appointment.datetime_start:
                return appointment
        return None




class Appointment:
    def __init__(self, title, datetime_start, datetime_end, color:str='#000000') -> None:
        self.title = title
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end
        self.color = color

    def __str__(self):
        return f"{self.datetime_start} | {self.datetime_end} | {self.title} | {self.color}"
    
    def toJSON(self):
        return {
            'start': self.datetime_start.strftime("%Y-%m-%d_%H:%M:%S"),
            'end': self.datetime_end.strftime("%Y-%m-%d_%H:%M:%S"),
            'title': self.title,
            'color': self.color,
        }




class Lecture(Appointment):
    def __init__(self, title, datetime_start, datetime_end, color, lecturer, room):
        super().__init__(title, datetime_start, datetime_end, color)
        self.room = room
        self.lecturer = lecturer

    def __str__(self):
        return f"{super().__str__()} | {self.room} | {self.lecturer}"
    
    def toJSON(self):
        js = super().toJSON()
        js.update({
            'room': self.room,
            'lecturer': self.lecturer
            })
        return js

