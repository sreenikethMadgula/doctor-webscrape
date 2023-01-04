import requests
import json

with open("hospitals.json") as hospital_file:
    hospitals = json.load(hospital_file)

url = "https://test-env.eba-f22ptdic.ap-south-1.elasticbeanstalk.com/hospitals"

for obj in hospitals:
    x = requests.get(url,json=obj)
    print(x.text)
    # print(obj)

# x = requests.post(url,json=hospitals[0])
# print(x.text)
