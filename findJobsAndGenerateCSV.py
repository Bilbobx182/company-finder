import datetime
import re

import requests
from bs4 import BeautifulSoup


def removeSpecial(inputString):
    return re.sub(r'\W+', '', inputString)


def writeToCSV(filename, csvContents):
    if (len(csvContents) > 0):
        with open(filename, 'w') as f:
            for csv_line in csvContents:
                f.write(csv_line + "\n")


def findIrishJobs(title, type, outputFile):
    print("DOING Irish : " + title + " " + type)
    csvContents = []
    baseurl = "https://www.irishjobs.ie"
    url = baseurl + "/ShowResults.aspx?Keywords=" + title + type
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "lxml")
    titles = soup.find_all("div", {"class": re.compile(r"module job-result")})

    for title in titles:
        job_and_company = title.contents[1].contents[3].text.replace("\n\n\n", " ").replace("\n\n", "")

        company = title.contents[1].contents[3].text.split("\n\n\n")[2].split("\n")[0]

        if "company reviews" in job_and_company:
            job_and_company = job_and_company.split("company reviews")
            job = job_and_company[0].split("company reviews")[0].split(company)[0]
        else :
            if("\n" in job_and_company):
                job_and_company.split("\n")[0].replace(company, "")
            else:
                job = job_and_company.replace(company,"")


        csv_line = job + "," + company + ", " + baseurl + title.contents[1].contents[9].contents[3].attrs['href']
        if (csv_line not in csvContents):
            csvContents.append(csv_line)
    writeToCSV(outputFile, csvContents)


def findIndeed(job, outputFile):
    print("DOING INDEED : " + job)
    page_number = 0
    csv_contents = []

    while page_number < 100:
        url = "https://ie.indeed.com/jobs?q={{ROLE}}&l={{LOCATION}}" + "&start={{START}}"
        url = url.replace("{{ROLE}}", job).replace("{{LOCATION}}", "Dublin")
        url = url.replace("{{START}}", str(page_number))
        result = requests.get(url)
        soup = BeautifulSoup(result.content, "lxml")

        titles = soup.find_all("div", {"class": re.compile(r"company")})
        for title in titles:
            name = re.sub(r'([^\s\w]|_)+', '', str(str(title.text.split(" ")[8:]).split("\\")[:1]))
            role = re.sub(r'([^\s\w]|_)+', '', str(title.parent.text.split("\n")[2]))
            job_url = url + "&vjk=" + title.parent.attrs['data-jk']
            csv_line = role + + ", " + name + " , " + job_url

            if csv_line not in csv_contents:
                csv_contents.append(csv_line)
        page_number += 10

    writeToCSV(outputFile, csv_contents)


jobs = ["java+developer", "junior+java+developer", "junior+android+developer", "android+developer",
        "junior+ios+developer", "ios+developer", "junior+devops", "devops", "junior+.net+developer", ".net+developer",
        "junior+full+stack", "full+stack", "junior+ai+software+engineer",
        "ai+software+engineer", "junior+web+developer", "web+developer", "junior+system administrator",
        "system administrator", "junior+data+scientist", "data+scientist", "junior+scrum+master", "scrum+master",
        "junior+product+owner", "product+owner"]

for job in jobs:
    findIrishJobs(job,
                  "&autosuggestEndpoint=%2Fautosuggest&Location=102&Category=3&Recruiter=Company&btnSubmit=+",
                  "irishJobs-companies" + job + str(datetime.datetime.today().strftime('%Y-%m-%d')) + ".csv")
    findIrishJobs("junior+java+developer",
                  "&autosuggestEndpoint=%2Fautosuggest&Location=102&Category=3&Recruiter=Agency&btnSubmit=+",
                  "irishJobs-agency" + job + str(datetime.datetime.today().strftime('%Y-%m-%d')) + ".csv")

    findIndeed(job, "indeed" + job + str(datetime.datetime.today().strftime('%Y-%m-%d')) + ".csv")
