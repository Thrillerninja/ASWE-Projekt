import json
import requests
from bs4 import BeautifulSoup
import re
import datetime
from loguru import logger

from api.calendar_api.cal import Calendar, Lecture, Appointment



def create_calendar_from_rapla(url:str, cal:Calendar=Calendar()):
    '''
    - ``url``: str: rapla url
    - return: Calendar: Calendar object with all lectures sorted by ``datetime_start`` (ascending)
    '''
    seps_empty = ["week_smallseparatorcell", "week_emptycell", "week_separatorcell"]
    seps_block_head = ["week_smallseparatorcell", "week_block", "week_separatorcell"]
    seps_block_tail = ["week_smallseparatorcell", "week_separatorcell", "week_smallseparatorcell"]
    year = url.split("year=")[1].split("&")[0] if "year=" in url else str(datetime.datetime.now().year)
    
    cal = Calendar()
    logger.info(f"Fetching data from URL: {url}")
    res = requests.get(url)
    if res.status_code != 200:
        logger.error(f"Failed to fetch data from URL: {url} with status code: {res.status_code}")
        return None
    soup = BeautifulSoup(res.text, 'html.parser')

    
    # Wochenübersichten
    for week_table in soup.find_all("table", class_="week_table"):
        # Wochentage (Datum)
        week_dates = [td.text[3:] + year for td in week_table.find_all("td", class_="week_header")]
        # Zeilen
        for table_row in week_table.find_all("tr")[2:]:  # skip first 2 rows cause they are not needed
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
                        datetime_start = datetime.datetime.strptime(f"{date} {time_start}", "%d.%m.%Y %H:%M").astimezone(tz=None)
                        datetime_end = datetime.datetime.strptime(f"{date} {time_end}", "%d.%m.%Y %H:%M").astimezone(tz=None)
                        try:
                            lecturer = td2.find("span", class_="person").text
                        except:
                            lecturer = "-"
                        lecture = Lecture(vl, datetime_start, datetime_end, color, lecturer, room)
                        cal.appointments.append(lecture)
                        logger.info(f"Added lecture: {lecture}")
                        td_index += 3
                    elif classes == seps_block_tail:
                        # Blockende
                        td_index += 2  # dont skip over last td cause its already from the next day
                except Exception as e:
                    logger.error(f"Error processing table row: {e}")
    return cal


# if __name__ == "__main__":
#     url = "https://rapla.dhbw.de/rapla/internal_calendar?user=doelker%40verwaltung.ba-stuttgart.de&file=22A&day=30&month=9&year=2024&pages=20"
#     cal = create_calendar_from_rapla(url)
#     for appointment in cal.appointments:
#         print(appointment)
