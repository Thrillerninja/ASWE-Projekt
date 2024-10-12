# Darf die Datei nicht calendar.py nennen, da es schon ein Modul mit dem Namen gibt
import json
import requests
from bs4 import BeautifulSoup
import re
import datetime


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



def create_calendar_from_rapla(url:str):
    seps_empty = ["week_smallseparatorcell", "week_emptycell", "week_separatorcell"]
    seps_block_head = ["week_smallseparatorcell", "week_block", "week_separatorcell"]
    seps_block_tail = ["week_smallseparatorcell", "week_separatorcell", "week_smallseparatorcell"]
    year = url.split("year=")[1].split("&")[0] if "year=" in url else str(datetime.datetime.now().year)
    
    cal = Calendar()
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Kurs (<h2 class="title">)
    course = soup.find("title").text

    # Wochenübersichten
    week_tables = soup.find_all("table", class_="week_table")

    for week_table in week_tables:

        # KW
        week_number = week_table.find("th", class_="week_number").text.replace("KW ", "")
        # Wochentage (Datum)
        week_dates = [td.text[3:] + year for td in week_table.find_all("td", class_="week_header")]
        # Einträge
        table_rows = week_table.find_all("tr")[2:]  # skip first 2 rows cause they are not needed

        for table_row in table_rows:
            # Einträge in einer row: separators & blocks
            table_data = table_row.find_all("td")

            td_index = 0
            for day in range(5):  # 5 days in a week
                try:
                    if td_index + 2 >= len(table_data):
                        break
                    td1 = table_data[td_index]
                    td2 = table_data[td_index + 1]
                    td3 = table_data[td_index + 2]
                    classes = [str(td.get("class")[0]).replace('_black', '') for td in [td1, td2, td3]]
                    # print(day, classes, end=" -> ")
                    if classes == seps_empty:
                        td_index += 3  # Skip empty dayrow
                    elif classes == seps_block_head:
                        # Blockanfang
                        time_start:str =  td2.text[:5]
                        assert re.match(r'^[0-9]{2}:[0-9]{2}$', time_start), f"Format Error: {time_start}"
                        time_end:str = td2.text[7:12]
                        assert re.match(r'^[0-9]{2}:[0-9]{2}$', time_end), f"Format Error: {time_end}"
                        vl:str = td2.find("a").text[12:]
                        room:str = td2.find_all("span", class_="resource")[-1].text
                        color:str = td2.get("style").split(":")[-1].strip()
                        assert re.match(r'^#[0-9a-fA-F]{6}$', color), f"Format Error: {color}"
                        date = week_dates[day]
                        assert re.match(r'^[0-9]{2}\.[0-9]{2}\.[0-9]{4}$', date), f"Format Error: {date}"
                        try:
                            lecturer = td2.find("span", class_="person").text
                        except:
                            lecturer = "-"
                        lecture = Lecture(vl, date, time_start, time_end, color, lecturer, room)
                        cal.appointments.append(lecture)
                        td_index += 3
                    elif classes == seps_block_tail:
                        # Blockende
                        td_index += 2  # dont skip over last td cause its already from the next day
                except Exception as e:
                    print(e)
    return cal
