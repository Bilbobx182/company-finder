import datetime
import os
from os import listdir
from os.path import isfile, join
import platform

def createDailyMasterFile():
    allJobs = []
    today = str(datetime.datetime.today().strftime('%Y-%m-%d'))

    if platform.system() == 'Linux':
        totalFolder = os.getcwd() + "/totalFolder/"
        if not os.path.exists(totalFolder):
            os.makedirs(totalFolder)
        todayFolder = os.getcwd() + "/" + today + "/"
        totalFolder = os.getcwd() + "/totalFolder/"
    else:
        totalFolder = os.getcwd() + "\\totalFolder\\"
        if not os.path.exists(totalFolder):
            os.makedirs(totalFolder)
        todayFolder = os.getcwd() +"\\" + today + "\\"


    onlyfiles = [f for f in listdir(todayFolder) if isfile(join(todayFolder, f))]

    for file in onlyfiles:
        with open(todayFolder + file) as f:
            content = f.readlines()
            for line in content:
                if line not in allJobs:
                    allJobs.append(line)

    with open(totalFolder + "totalFile" +  str(datetime.datetime.today().strftime('%Y-%m-%d')) + ".csv", 'w') as f:
        for line in allJobs:
            f.write(line)
