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

    # doctor_hospital = doctor.find('div', class_ = "sp-d-hospital-aff").text.strip()
    doctor_hospital_id = "0"
    # record.append(doctor_hospital_id)
    record["hospitals"] = list()
    
    print(record)

    return record

def get_records_by_url(url:str, specialization:str,page_count)->list[list]:
    html_text = requests.get(url).text
    f = open("page_%d.html" % page_count,"w")
    f.write(html_text)

    soup = BeautifulSoup(html_text,'lxml')
    records = []
    doctors = soup.find_all('div', class_ = "row padding-20 box-shadow common_shadow_radius full-width")
    for doctor in doctors:
        record = get_record(doctor,specialization)
        records.append(record)
    return records


# def generate_records():
#     records = []
#     i = 0
#     for url in urls:
#         for page in range(4):
#             records += get_records_by_url(url+"?page="+str(page),specializations[i])
#         i+=1
    
#     f = open("doctors.csv","w")
#     # f.write("\"name\",\"degree\",\"specialization\",\"hospital\",\"experience\",\"awards\"\n")

#     for record in records:
#         s = ""
#         for i in range(len(record)-1):
#             s+="\""+record[i]+"\""+","
#         s+="\""+record[i+1]+"\""+"\n"
#         f.write(s)


def generate_records():
    records = []
    i = 0
    # f = open("doctors.csv","w")
    for url in urls:
        # for page in range(4):
        records+=get_records_by_url(url,i,i)
        i+=1
    
    # f.write("name,address,age,gender,mobile,email,degree,experience,awards,specializaitons/0,hospitals/0\n")
    # for record in records:
    #     s = ""
    #     for i in range(len(record)-1):
    #         s+="\""+record[i]+"\""+","
    #     s+="\""+record[i+1]+"\""+"\n"
    #     f.write(s)

    with open("doctors.json","w") as f:
        json.dump(records,f)
    
generate_records()
