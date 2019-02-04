import datetime
import re
from multiprocessing.pool import Pool

import requests
from bs4 import BeautifulSoup

import generateDailyMaster


# vjs-content


def find_jobs_ie(job):
    print("--------")
    print("JOB : " + job)
    print("--------")
    csv_contents = []

    url = "https://www.jobs.ie/Jobs.aspx?hd_searchbutton=true&Categories=4&Regions=63&Keywords={{}}&job-search=true"
    url = url.replace("{{ROLE}}", job)
    result = requests.get(url)
    soup = BeautifulSoup(result.content, "html.parser")

    titles = soup.find_all("article", {"class": re.compile(r"job-list-item")})
    for title in titles:
        role = title.contents[3].contents[1].text.replace("\n", "")
        company = title.contents[5].contents[3].text.replace("\n", "")
        url = title.contents[3].contents[1].contents[1].attrs['href'].replace("\n", "")
        companyLocation = title.contents[7].text.replace("\n", "")
        csv_line = role + ", " + company + " , " + url + "," + companyLocation
        csv_contents.append(csv_line)


def create_pool(jobs):
    pool = Pool(processes=8)
    pool.map(find_jobs_ie, jobs)
    pool.close()
    pool.join()


def main():
    jobs = ["java+developer", "junior+java+developer", "junior+android+developer", "android+developer",
            "junior+ios+developer", "ios+developer", "junior+devops", "devops", "junior+.net+developer",
            ".net+developer",
            "junior+full+stack", "full+stack", "junior+ai+software+engineer",
            "ai+software+engineer", "junior+web+developer", "web+developer", "junior+data+scientist", "data+scientist",
            "junior+scrum+master", "scrum+master"]

    print("START : " + str(datetime.datetime.now()))
    create_pool(jobs)
    print("END : " + str(datetime.datetime.now()))

    generateDailyMaster.createDailyMasterFile()


if __name__ == '__main__':
    main()
