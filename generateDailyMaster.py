import datetime
import os
from os import listdir
from os.path import isfile, join
import platform

def createDailyMasterFile():
    os.getcwd()
    allJobs = []
    today = str(datetime.datetime.today().strftime('%Y-%m-%d'))
    todayFolder = os.getcwd() + today

    onlyfiles = [f for f in listdir(todayFolder) if isfile(join(todayFolder, f))]

    if platform.system() == 'Linux':
        filePath = todayFolder + "/"
    else:
        filePath = todayFolder + "\\"

    for file in onlyfiles:
        with open(filePath + file) as f:
            content = f.readlines()
            for line in content:
                if line not in allJobs:
                    print(line)
                    allJobs.append(line)

    with open("totalFile" + today + ".csv", 'w') as f:
        for line in allJobs:
            f.write(line)
