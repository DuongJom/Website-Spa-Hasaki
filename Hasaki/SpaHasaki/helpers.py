import datetime
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

from .models import Customer, Appointment, Service, Employee, Feedback

def get_appointment():
    appointments = Appointment.objects.all().values()

    times = [i for i in range(9,21)]
    data = dict()
    for t in times:
        key = datetime.time(hour=t).strftime("%H:%M")
        data[key] = []
        for appointment in appointments:
            if appointment['start_time'].hour == t:
                data[key].append(appointment)
    return data

def read_data(sheet_name:str):
    # Define the scope for the API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    script_dir = os.path.dirname(os.path.realpath(__file__))
    authen_path = script_dir.replace("\\", "/").split("/SpaHasaki")[0] + "/static/resources/spahasaki-bbf24db11c1e.json"
    print(authen_path)
    # Provide the path to the downloaded JSON credentials file
    creds = ServiceAccountCredentials.from_json_keyfile_name(authen_path, scope)

    # Authenticate the client
    client = gspread.authorize(creds)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1-QVApqHuWnbNZdfcsnWRDXsJT8qjMqkUtHyuOC2oFKg/edit?usp=sharing").worksheet(sheet_name)
    data = sheet.get_all_records()
    return data