import Adafruit_DHT
import datetime
import time
import pandas as pd
import numpy as np

def main():
    sensor = Adafruit_DHT.DHT22
    pin = 11
    while True:
        humList = []
        tempList = []
        currentDate = datetime.date.now()
        currentTime = datetime.time.now()
        for reading in range(6):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            humList.append(humidity)
            tempList.append(temperature)
        tempAvg = np.average(tempList)
        tempSD = np.std(tempList)
        humAvg = np.average(humList)
        humSD = np.std(humList)
        logRow = pd.Series([currentDate, currentTime, tempAvg, tempSD, humAvg, humSD])
        logRow.to_csv(
            './tempData.tsv',
            sep='/t',
            header=['date', 'time', 'tempAvg', 'tempSD', 'humAvg', 'humSD'],
            index=False,
            mode='a',
            encoding='utf-8',
        )
        newTime = datetime.datetime.now()
        minutesToSleep = (newTime.minute % 5) - (newTime.minute % 2)
        secondsToSleep = 60 - newTime.second
        time.sleep((minutesToSleep * 60) + secondsToSleep)

if __name__ == '__main__':
    main()
