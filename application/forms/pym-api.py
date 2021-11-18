import json
import requests

BASE_URL = "https://api.pym.nl"
HEADERS = {
    "Authorization": "Token token=7a6e5ab65982d676bab67a7e909e963abaff3366, timestamp=1597683672, guid=964aa6d9c60279c0, secret=b5c04bd7-b6cb-4750-af48-acaf082c4f64",
    "x-pym-version": "2.3.2",
    "x-pym-platform": "android",
    "x-pym-timezone": "GMT+01:00",
    "x-pym-approved-gdpr": "false",
    "Content-Type": "application/json; charset=UTF-8"
    }   

r = requests.get(BASE_URL + "/v1/pym/restore", headers=HEADERS) 
print(r.text)
response_data = r.json()
print(response_data)

# with open('response1.txt') as json_file:
#     data = json.load(json_file)
#     for photo in data['photos']:
#         comment = photo['comment']
#         filename = photo['fileName']
#         id = photo['id']
#         location = photo['location']
#         takenAt = photo['takenAt']
#         url = photo['url']
#         uuid = photo['uuid']
#         print("comment: {}\nfilename: {}\nid: {}\nurl: {}\n".format(comment, filename, id, url))