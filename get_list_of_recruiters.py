import json
import os
from os import listdir
from os.path import isfile, join
import geocoder
import time

import requests
from bs4 import BeautifulSoup


cwd = os.getcwd()
path = cwd + "\\data"
allfiles = [f for f in listdir(path) if isfile(join(path, f))]


# TODO Get address when company has many locations in dublin
# TODO Append to address to file
# TODO Deal with duplicates Bank of America vs Bank of America Meriyl Lynch Susquehanna International Group VS SIG


def get_recruiters():
    with open(cwd + '\\recruiters.json') as f:
        return json.load(f)


def update_recruiters_json(data):
    with open(cwd + '\\recruiters.json', 'w') as outfile:
        json.dump(data, outfile)

def get_address_from_google(company):
    baseurl = "https://www.google.com/search?client=firefox-b-ab&q="
    url = baseurl + "+" + company + "+" + "Dublin address"
    request_result = requests.get(url)
    soup = BeautifulSoup(request_result.content, "html.parser")
    result = soup.find_all("span", {"class": "A1t5ne"})

    try:
        print(company + " , " + result[0].contents[0].replace(",",""))
    except:
        print(company + ", NA")
    time.sleep(7.5)

def get_list_of_recruiters_from_irish_jobs():
    # Irish jobs allows us to query recruiters only, we get a list of recrutiers from here.
    path = cwd + "\\data"
    was_recruiters_updated = 0
    recruiter_files = [f for f in allfiles if "agency" in f]
    recruiters_json = get_recruiters()

    for file in recruiter_files:
        with open(path + "\\" + file, mode='r') as csv_file:
            for line in csv_file.readlines():
                if (line.split(",")[1] not in recruiters_json['recruiters']):
                    recruiters_json['recruiters'].append(line.split(",")[1])
                    was_recruiters_updated = 1

    if (was_recruiters_updated):
        update_recruiters_json(recruiters_json)


def get_hiring_companies():
    companies = []
    dont_search_companies = []

    for file in allfiles:
        with open(path + "\\" + file, mode='r') as csv_file:

            for line in csv_file.readlines():
                company = line.split(",")[1].strip()
                if (company not in get_recruiters()['recruiters']):
                    if (company not in companies):
                        companies.append(company)

    print(len(companies))

    with open(cwd + "\\" + "address.csv", mode='r') as csv_file:
        for line in csv_file.readlines():
            dont_search_companies.append(line.split(",")[0].strip())

    for company in companies:
        if company not in dont_search_companies:
            get_address_from_google(company.replace("ltd",""))

def main():
    get_list_of_recruiters_from_irish_jobs()
    get_hiring_companies()
    # get_company_geo_data()


main()
