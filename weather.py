
from template_root import BASE_ROOT

import requests
import json

def get_json_data():
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?Authorization=rdec-key-123-45678-011121314"
    req = requests.get(url)
    json_content = req.content.decode('utf-8')
    return json.loads(json_content)

def total_city(location_json):

    city_set = set()
    for location in location_json:
        city_set.add(location['parameter'][0]['parameterValue'])

    return city_set

def total_town(location_json, city_name):

    town_set = set()
    for location in location_json:
        if location['parameter'][0]['parameterValue'] != city_name:
            continue

        town_set.add(location['parameter'][2]['parameterValue'])
    return town_set

def find_from_city_and_town(location_json, city_name=None, town_name=None):

    return_list = []
    for location in location_json:
        城市 = location['parameter'][0]['parameterValue']
        區 = location['parameter'][2]['parameterValue']

        if city_name and city_name != 城市: continue
        if town_name and town_name != 區: continue

        觀測時間 = location['time']['obsTime']
        觀測站 = location['locationName']
        氣溫 = location['weatherElement'][3]['elementValue']
        風向 = location['weatherElement'][1]['elementValue']
        風速 = location['weatherElement'][2]['elementValue']
        return_list.append((觀測時間, 觀測站, 氣溫, 風向, 風速))

    return return_list

class root(BASE_ROOT):
    def run_start(self):

        if not self.root_cmds:
            jason_dict = get_json_data()
            location_json = jason_dict['records']['location']
            self.var_dict['location_json'] = location_json
            return

        root_cmds = set(self.root_cmds[0])
        if "help" in root_cmds:
            self.push_return_str(f"歡迎來到天氣查詢!\n")
            self.push_return_str(f"下面是函數說明:\n")
            self.push_return_str(f"***********************\n")
            self.push_return_str(f"city: 設定所在城市名, exp:桃園市\n")
            self.push_return_str(f"town: 設定所在地區名, exp:八德區\n")
            self.push_return_str(f"city_ls: 查詢所有城市名(無輸入)\n")
            self.push_return_str(f"town_ls: 查詢所有地區名(需先設定城市名,無輸入)\n")
            self.push_return_str(f"show: 查詢天氣(無輸入)\n")
            self.push_return_str(f"***********************\n")

        jason_dict = get_json_data()
        location_json = jason_dict['records']['location']
        self.var_dict['location_json'] = location_json

def city(call, cmd):
    call.var['city'] = cmd

def town(call, cmd):
    call.var['town'] = cmd

def city_ls(call, cmd):
    city_set = total_city(call.var['location_json'])
    call.push_return("城市名單如下:\n")
    for city in city_set:
        call.push_return(f"{city}\n")
    call.push_return("\n")

def town_ls(call, cmd):
    if "city" not in call.var:
        call.push_return("請先設定所在城市\n")
        return

    city = call.var["city"]
    town_set = total_town(call.var['location_json'], call.var["city"])

    call.push_return(f"{city}的地區名單如下:\n")
    for town in town_set:
        call.push_return(f"{town}\n")
    call.push_return("\n")

def show(call, cmd):
    city = call.var["city"] if "city" in call.var else None
    town = call.var["town"] if "town" in call.var else None
    location_json = call.var['location_json']
    weather_list = find_from_city_and_town(location_json, city, town)

    if len(weather_list) == 0:
        call.push_return(f"city:{city} town:{town} 查無結果\n")
        return

    call.push_return(f"city:{city} town:{town}\n")
    call.push_return(f"...........................\n")
    for weather in weather_list:
        觀測時間, 觀測站, 氣溫, 風向, 風速 = weather
        call.push_return(f"觀測時間: {觀測時間}\n")
        call.push_return(f"觀測站: {觀測站}\n")
        call.push_return(f"氣溫: {氣溫}\n")
        call.push_return(f"風向: {風向}\n")
        call.push_return(f"風速: {風速}\n")
        call.push_return(f"\n")

    return