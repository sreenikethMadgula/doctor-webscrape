# scraping from credihealth.com
from bs4 import BeautifulSoup
import requests
import re
import json

# html_text = requests.get("https://www.credihealth.com/doctors/bangalore/cardiology").text
# print(html_text)
# soup = BeautifulSoup(html_text,'lxml')
# print(soup.prettify())
# doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
# print(doctors)
page_count = 0
urls = [
    "https://www.credihealth.com/doctors/bangalore/cardiology",
    "https://www.credihealth.com/doctors/bangalore/ent",
    "https://www.credihealth.com/doctors/bangalore/orthopedics",
    "https://www.credihealth.com/doctors/bangalore/ophthalmology",
    "https://www.credihealth.com/doctors/bangalore/general-surgery",
    "https://www.credihealth.com/doctors/bangalore/dental-surgery",
    "https://www.credihealth.com/doctors/bangalore/neurology",
    "https://www.credihealth.com/doctors/bangalore/gastroenterology",
    "https://www.credihealth.com/doctors/bangalore/dermatology",
]

specializations = [
    "cardiology",
    # "ent",
    # "orthopedic",
    # "opthalmology",
    # "general surgery",
    # "dental surgery",
    # "neurology",
    # "gastroenterology",
    # "dermatology"
]

# with open("hospital_names.json") as hospital_file:
#     hospital_nanes = json.load(hospital_file)

with open("hospitals.json") as hospital_file:
    hospitals = json.load(hospital_file)

def get_hospital(hospital):
    hospital_name_mo = re.search(r"([^,]+),\s([^+]+)[+1 more]*([.+]*)",hospital)
    hospital_groups = hospital_name_mo.groups()
    hospital_name = hospital_groups[0]
    hospital_address = hospital_groups[1]
    # print(hospital_groups,hospital_address)

    return hospital_name,hospital_address

def get_experience(doctor_achievements) ->str:
    doctor_experience = doctor_achievements.find('span', class_ = '').text.strip()
    txt = doctor_experience
    mo = re.search(r'(\d+).*',txt)
    doctor_experience = mo.groups()[0]
    return doctor_experience

def get_awards(doctor_achievements) ->str:
    print("this")
    try:
        doctor_awards = doctor_achievements.find('span', class_ = "padding-r30").text.strip()
        txt = doctor_awards
        mo = re.search(r'(\d+).*',txt)
        doctor_awards = mo.groups()[0]
    except:
        doctor_awards = "0"
    return doctor_awards


def get_record(doctor,specialization) -> list:

    try:
        # record = []
        record = {}
        doctor_name = doctor.find('h2', class_ = "doc_titled_name").text.strip()
        # record.append(doctor_name)
        record["name"]=doctor_name
        
        doctor_address = "Bangalore"
        # record.append(doctor_address)
        record["address"] = doctor_address


        doctor_age = "50"
        # record.append(doctor_age)
        record["age"]=doctor_age


        doctor_gender = "M"
        # record.append(doctor_gender)
        record["gender"]=doctor_gender

        doctor_mobile = "999999999"
        # record.append(doctor_mobile)
        record["mobile"]=doctor_mobile

        doctor_email = "abc@xyz.com"
        # record.append(doctor_address)
        record["email"] = doctor_email



        doctor_degree = doctor.find('p', class_ = "sp-d-degree").text.strip()
        # record.append(doctor_degree)
        record["degree"]=doctor_degree
        
        doctor_achievements = doctor.find('div', class_ = "sp-achievements")

        doctor_experience = get_experience(doctor_achievements)
        # record.append(doctor_experience)
        record["experience"]=doctor_experience

        doctor_awards = get_awards(doctor_achievements)
        # record.append(doctor_awards)
        record["awards"]=doctor_awards
        
        # record.append(str(specialization))
        doctor_specializations = []
        doctor_specializations.append(specialization)
        record["specializations"] = doctor_specializations

        # doctor_hospital_id = "0"
        # record.append(doctor_hospital_id)
        record["hospitals"] = list()
        doctor_hospital = doctor.find('div', class_ = "sp-d-hospital-aff").text.strip()
        hospital_name,hospital_address = get_hospital(doctor_hospital)
        
        hospital_id = -1
        for i in hospitals:
            if i["name"] == hospital_name and i["address"] == hospital_address:
                hospital_id = i["id"]
                break
        record["hospitals"].append(hospital_id)
        if hospital_id == -1:
            record = {}
        print(record)
        return record
    
    except Exception as e:
        print("\n\tERROR",e)
        pass


def get_records_from_files(specialization:str,page_count)->list[list]:
    # html_text = requests.get(url).text
    f = open("page_%d.html" % page_count,"r")
    soup = BeautifulSoup(f,'lxml')
    print("here")
    records = []
    doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
    for doctor in doctors:
        record = get_record(doctor,specialization)
        if record:
            records.append(record)
    return records

def generate_records():
    records = []
    i = 0
    # f = open("doctors.csv","w")
    # for url in urls:
    #     # for page in range(4):
    #     records+=get_records_by_url(url,i,i)
    #     i+=1

    for i in range(9):
        records+=get_records_from_files(i+1,i)
    with open("doctors2.json","w") as f:
        json.dump(records,f)
    
generate_records()
