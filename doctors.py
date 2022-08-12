# scraping from credihealth.com
from doctest import DONT_ACCEPT_TRUE_FOR_1
from typing import List
from bs4 import BeautifulSoup
import requests
import re

html_text = requests.get("https://www.credihealth.com/doctors/bangalore/cardiology").text
# print(html_text)
soup = BeautifulSoup(html_text,'lxml')
# print(soup.prettify())
# doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
# print(doctors)

urls = [
    # "https://www.credihealth.com/doctors/bangalore/cardiology",
    # "https://www.credihealth.com/doctors/bangalore/ent",
    # "https://www.credihealth.com/doctors/bangalore/orthopedics",
    # "https://www.credihealth.com/doctors/bangalore/ophthalmology",
    # "https://www.credihealth.com/doctors/bangalore/general-surgery",
    # "https://www.credihealth.com/doctors/bangalore/dental-surgery",
    # "https://www.credihealth.com/doctors/bangalore/neurology",
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


def get_record(doctor) -> List:
    record = []
    doctor_name = doctor.find('h2', class_ = "GA_doctors_docprof doc_titled_name").text.strip()
    record.append(doctor_name)
    # print(doctor_name)
    # txt = str(doctor_name)
    # mo = re.search(r'>(.+)<',txt)
    # name = mo.groups()[0]
    # print(name)

    doctor_degree = doctor.find('p', class_ = "sp-d-degree").text.strip()
    record.append(doctor_degree)
    # print(doctor_degree)
    # txt = str(doctor_degree)
    # mo = re.search(r'>(.+)<',txt)
    # degree = mo.groups()[0]
    # # print(degree)

    doctor_specialization = doctor.find('p', class_ = "sp-d-speciality").text.strip()
    record.append(doctor_specialization)
    # print(doctor_specialization)
    # txt = str(doctor_specialization)
    # mo = re.search(r'>(.+)<',txt)
    # specialization = mo.groups()[0]
    # print(specialization)

    doctor_hospital = doctor.find('div', class_ = "sp-d-hospital-aff").text.strip()
    record.append(doctor_hospital)
    # print(doctor_hospital)
    # hospital_name = doctor_hospital.find('a', class_ = 'color-black')
    # txt = str(hospital_name)
    # mo = re.search(r'>(.+)<',txt)
    # hospital = mo.groups()[0]
    # print(hospital)


    doctor_achievements = doctor.find('div', class_ = "sp-achievements")
    doctor_awards = get_awards(doctor_achievements)
    record.append(doctor_awards)
    # try:
    #     doctor_awards = doctor_achievements.find('span', class_ = "padding-r30").text.strip()
    #     txt = doctor_awards
    #     mo = re.search(r'(\d+).*',txt)
    #     doctor_awards = mo.groups()[0]
    # except:
    #     doctor_awards = ''
    # record.append(doctor_awards)
    # print(doctor_awards)
    # txt = str(doctor_awards)
    # mo = re.search(r'>\s(\d+).*\s',txt)
    # awards = mo.groups()[0]
    # print(awards)

    doctor_experience = get_experience(doctor_achievements)
    record.append(doctor_experience)
    print(record)

    # doctor_experience = doctor_achievements.find('span', class_ = '').text.strip()
    # txt = doctor_experience
    # mo = re.search(r'(\d+).*',txt)
    # doctor_experience = mo.groups()[0]
    # record.append(doctor_experience)
        # print(doctor_experience)
    # txt = str(doctor_experience)
    # mo = re.search(r'>\s(\d+).*\s<',str(doctor_experience))
    # if(mo):
    #     experience = mo.groups()[0]
        # print(experience)
    return record

def get_records_by_url(url:str)->List[List]:
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')
    records = []
    doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
    for doctor in doctors:
        record = get_record(doctor)
        records.append(record)
    return records


def generate_records():
    records = []
    for url in urls:
        records += get_records_by_url(url)
    
    f = open("doctors.csv","a")
    f.write("\"name\",\"degree\",\"specialization\",\"hospital\",\"experience\",\"awards\"\n")

    for record in records:
        s = ""
        for i in range(len(record)-1):
            s+="\""+record[i]+"\""+","
        s+="\""+record[i+1]+"\""+"\n"
        f.write(s)
    
generate_records()

# print(generate_records())
