from bs4 import BeautifulSoup
import requests
import re


def get_doctor_table(doctor_data):
    doctor_table = doctor_data.find('table', class_='table-bordered table-striped table-condensed cf').text.strip()

def get_record(doctor):
    record = []
    doctor_name = doctor.find('td', class_='Name')
    doctor_name = doctor.find('td', class_='Name')
    doctor_name = doctor.find('td', class_='Name')
    doctor_name = doctor.find('td', class_='Name')
    doctor_name = doctor.find('td', class_='Name')
    doctor_name = doctor.find('td', class_='Name')
    
def get_doctor_records(doctor_table):
    records = []
    doctors = doctor_table.find_all('tr')
    for doctor in doctors:
        record = get_record(doctor)
        records.append()


def get_doctor_details(url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')