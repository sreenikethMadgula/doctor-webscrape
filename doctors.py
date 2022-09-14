# scraping from credihealth.com
from doctest import DONT_ACCEPT_TRUE_FOR_1
from typing import List
from bs4 import BeautifulSoup
import requests
import re

# html_text = requests.get("https://www.credihealth.com/doctors/bangalore/cardiology").text
# print(html_text)
# soup = BeautifulSoup(html_text,'lxml')
# print(soup.prettify())
# doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
# print(doctors)

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
    "ent",
    "orthopedic",
    "opthalmology",
    "general surgery",
    "dental surgery",
    "neurology",
    "gastroenterology",
    "dermatology"
]


def get_experience(doctor_achievements) ->str:
    doctor_experience = doctor_achievements.find('span', class_ = '').text.strip()
    txt = doctor_experience
    mo = re.search(r'(\d+).*',txt)
    doctor_experience = mo.groups()[0]
    return doctor_experience

def get_awards(doctor_achievements) ->str:
    try:
        doctor_awards = doctor_achievements.find('span', class_ = "padding-r30").text.strip()
        txt = doctor_awards
        mo = re.search(r'(\d+).*',txt)
        doctor_awards = mo.groups()[0]
    except:
        doctor_awards = ''
    return doctor_awards


def get_record(doctor,specialization) -> List:
    record = []
    doctor_name = doctor.find('h2', class_ = "GA_doctors_docprof doc_titled_name").text.strip()
    record.append(doctor_name)
    

    doctor_degree = doctor.find('p', class_ = "sp-d-degree").text.strip()
    record.append(doctor_degree)
    
    record.append(specialization)
    

    doctor_hospital = doctor.find('div', class_ = "sp-d-hospital-aff").text.strip()
    record.append(doctor_hospital)
    

    doctor_achievements = doctor.find('div', class_ = "sp-achievements")
    doctor_awards = get_awards(doctor_achievements)
    record.append(doctor_awards)
    

    doctor_experience = get_experience(doctor_achievements)
    record.append(doctor_experience)
    # print(record)

    return record

def get_records_by_url(url:str, specialization:str)->List[List]:
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')
    records = []
    doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
    for doctor in doctors:
        record = get_record(doctor,specialization)
        records.append(record)
    return records


def generate_records():
    records = []
    i = 0
    for url in urls:
        for page in range(4):
            records += get_records_by_url(url+"?page="+str(page),specializations[i])
        i+=1
    
    f = open("doctors1.csv","a")
    f.write("\"name\",\"degree\",\"specialization\",\"hospital\",\"experience\",\"awards\"\n")

    for record in records:
        s = ""
        for i in range(len(record)-1):
            s+="\""+record[i]+"\""+","
        s+="\""+record[i+1]+"\""+"\n"
        f.write(s)
    
generate_records()

# print(generate_records())
