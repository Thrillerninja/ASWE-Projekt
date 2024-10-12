# Darf die Datei nicht calendar.py nennen, da es schon ein Modul mit dem Namen gibt
import json


class Calendar:
    def __init__(self, appointments:list=[]) -> None:
        self.appointments = appointments

    def sort(self):
        self.appointments.sort(key=lambda x: str(x.date) + str(x.start))

    def __str__(self) -> str:
        self.sort()
        return "".join([str(appointment) for appointment in self.appointments])
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def toJSON(self):
        self.sort()
        return [appointment.toJSON() for appointment in self.appointments]
    
    
    def save(self, filepath:str):
        self.sort()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.toJSON(), f, indent=4, ensure_ascii=False)




class Appointment:
    def __init__(self, title:str='-', date:str='-', start:str='-', end:str='-', color:str='#000000') -> None:
        self.title = title
        self.date = date
        self.start = start
        self.end = end
        self.color = color

    def __str__(self):
        return f"{self.date} | {self.start} | {self.end} | {self.title} | {self.color}"
    
    def toJSON(self):
        return {
            'date': self.date,
            'start': self.start,
            'end': self.end,
            'title': self.title,
            'color': self.color,
        }




class Lecture(Appointment):
    def __init__(self, title, date, start, end, color, lecturer, room):
        super().__init__(title, date, start, end, color)
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
