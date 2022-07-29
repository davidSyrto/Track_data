import csv
import datetime
from typing import List
from unicodedata import name
import requests
from requests.structures import CaseInsensitiveDict
import json
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate


from dataclasses import dataclass

@dataclass
class GPSPoint:
    latitude: float
    longitude: float
    altitude: float
    time: datetime
    satellites: int





class Animal :
    def __init__(self,id : str) :
        self.id = id
        self.position = []
    
    def addPositionFromJSON(self,json : dict) :
        if len(self.getTime()) > 0: 
            if not json['timestamp'] == self.getTime()[-1] :
                self.position.append(GPSPoint(json['lat'],json['lng'],json['altitude'],json['timestamp'],json['satellites']))
        else :
            self.position.append(GPSPoint(json['lat'],json['lng'],json['altitude'],json['timestamp'],json['satellites']))

    def getLatitude(self) :
        return [point.latitude for point in self.position]

    def getLongitude(self) :
        return [point.longitude for point in self.position]

    def getAltitude(self) :
        return [point.altitude for point in self.position]

    def getTime(self) :
        return [point.time for point in self.position]

    def exportAsCSV(self,filename : str) :
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow(['latitude','longitude','altitude','time','satellites'])
            for point in self.position :
                writer.writerow([point.latitude,point.longitude,point.altitude,point.time,point.satellites])


def gatherInfo(animals : List) :

    with open('adnexoActivateDeactivate.csv', ) as csv_file:
        csv_reader = csv.reader(csv_file, quotechar='"', delimiter=',')
        line_count = 0
        ID = ""
        DEVEUI = ""
        identifier = ""
        active = ""
        username = "alptracker"
        password = "Ae0)2]g7"
        for row in csv_reader:
            ID = str(row[0])
            DEVEUI = str(row[1])
            identifier = str(row[2])
            active = str(row[3])
            
            int_id = int(ID)
            if int_id not in animals :
                animals[int_id] = Animal(int_id)

            TOKEN_URL = "https://api.sheep.srv.adnexo.ch/api/token/"
            auth_data = {
                'username': username,
                'password': password
            }
            ax_track_response = requests.post(TOKEN_URL, data=auth_data)
            ax_token = ax_track_response.json()['access']
            print(f'Start {line_count}')
            print(ax_token)
            
            url = f'https://api.sheep.srv.adnexo.ch/api/v1/trackers/{ID}/'
            data = {
            
                    'identifier': identifier,
                    'deveui': DEVEUI,
                    'active': active
                }
            print(url)
            print(data)
            line_count += 1
            response = requests.patch(url, data=data, headers={'Authorization': f'JWT {ax_token}'})
            msg = json.loads(response.content)

            animals[int_id].addPositionFromJSON(msg['last_gps_measurement'])
            
            print(response.reason)
            print('Ax Track response ', response.status_code)
            #resp = requests.post(url, headers=headers, data=data)
            #print(resp.status_code)
            #print(resp._content)


if __name__ == "__main__":
    animals = {}
    gatherInfo(animals)
    a = animals[2102]
    gatherInfo(animals)
    a = animals[2102]
    fig = go.Figure([go.Scatter(x=[a.getTime()], y=a.getLatitude())])
    fig.show()