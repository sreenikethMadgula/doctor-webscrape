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

hospitals = {}
hospital_count = 0


def get_hospital(hospital):
    hospital_name_mo = re.search(r"([^,]+),\s([^+]+)[+1 more]*([.+]*)",hospital)
    hospital_groups = hospital_name_mo.groups()
    hospital_name = hospital_groups[0]
    hospital_address = hospital_groups[1]
    print(hospital_groups,hospital_address)

    # hospital_address_mo = re.search(r"(.+)+\d(.+)",hospital_address)
    # if hospital_address_mo:
    #     hospital_address_groups = hospital_address_mo.groups()
    #     print(hospital_address_groups)
    # hospital_2_name_mo = re.search(r"(.+)+\d(.+)",hospital_address)
    # if hospital_2_name_mo:
    #     hospital_2_groups = hospital_2_name_mo.groups()
    #     print(hospital_2_groups)

    return hospital_name,hospital_address


def get_record(doctor,specialization) -> list:
    # record = {}
    global hospital_count
    try:
        doctor_hospital = doctor.find('div', class_ = "sp-d-hospital-aff").text.strip()

        print(doctor_hospital)
        hospital_name,hospital_address = get_hospital(doctor_hospital)

        doctor_hospital = hospital_name + hospital_address

        doctor_address = "Bangalore"
        # record.append(doctor_address)
        # record["address"] = doctor_address

        # doctor_specializations = []
        # doctor_specializations.append(specialization)
        # record["specializations"] = doctor_specializations

        if doctor_hospital in hospitals.keys():
            if specialization not in hospitals[doctor_hospital]["specializations"]:
                hospitals[doctor_hospital]["specializations"].append(specialization)
        else:
            hospital_count+=1
            hospitals[doctor_hospital] = {
                "id": hospital_count,
                "name": hospital_name,
                "address": hospital_address,
                "specializations": [],
                "labs":[],
                "licenses":[]
            }
            hospitals[doctor_hospital]["specializations"].append(specialization)

        record = hospitals[doctor_hospital]
        # print(record)

        # return record
    except Exception as e:
        print("\n\tERROR", e)
        pass

def get_records_from_files(specialization:str,page_count)->list[list]:
    f = open("page_%d.html" % page_count,"r")
    soup = BeautifulSoup(f,'lxml')
    # print("here")
    # records = []
    doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
    for doctor in doctors:
        # record = get_record(doctor,specialization)
        record = get_record(doctor,specialization)
        # if record:
        #     records.append(record)
    # return records

def generate_records():
    records = []
    i = 0

    for i in range(9):
        # record_list = get_records_from_files(i,i)
        get_records_from_files(i+1,i)
        # print(record_list)
        # records+=record_list
    for i in hospitals.keys():
        records.append(hospitals[i])
    with open("hospitals.json","w") as f:
        json.dump(records,f)
    
generate_records()


with open("hospital_names.json","w") as f:
    json.dump(hospitals,f)