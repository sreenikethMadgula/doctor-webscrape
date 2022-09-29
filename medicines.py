from bs4 import BeautifulSoup
import requests
import re

def get_record():
    return


def get_records_by_url(url:str):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text,'lxml')
    records = []
    # table = soup.find('tbody')
    # print(table)
    trs = soup.find_all("tr")
    print(trs.pop(0))
    for tr in trs:
        ths = tr.find_all('th')

        for i in range(len(ths)):
            ths[i] = ths[i].text.strip()
        
        ths.pop(0)
        ths.pop(0)
        # print(ths)
        # break
        records.append(ths)
    
    print(records[0])

    print("done")
    return records

# get_records_by_url("http://janaushadhi.gov.in/ProductList.aspx")


def generate_records():
    records = get_records_by_url("http://janaushadhi.gov.in/ProductList.aspx")
    j = 0
    
    f = open("patients.csv","w")

    for record in records:
        s = ""
        for i in range(len(record)-1):
            s+="\""+record[i]+"\""+","
        s+="\""+record[i+1]+"\""+"\n"
        f.write(s)
    
generate_records()