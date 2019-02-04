import datetime
import re
from multiprocessing.pool import Pool

import requests
from bs4 import BeautifulSoup

import generateDailyMaster


# vjs-content



def create_pool(jobs):
    pool = Pool(processes=8)
    pool.map(find_computer_jobs, jobs)
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
