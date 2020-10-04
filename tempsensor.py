import Adafruit_DHT
import datetime
import time
import pandas as pd
import numpy as np

def main():
    print()
    print('*' * 50)
    print('*' + (' ' * 48) + '*')
    print("*       Running temperature sensor program!      *")
    print('*' + (' ' * 48) + '*')
    print('*' * 50)
    print()
    sensor = Adafruit_DHT.DHT22
    pin = 17
    numReadings = 5
    while True:
        humList = []
        tempList = []
        print('*' * 50)
        currentdatetime = datetime.datetime.now()
        print('*')
        print(f'*     Current time: {currentdatetime.strftime("%H:%M:%S")}')
        print('*')
        for reading in range(numReadings + 1):
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            print(f'*         Reading {reading + 1} (tempC, hum%): {round(temperature, 2)}, {round(humidity, 2)}')
            humList.append(humidity)
            tempList.append(temperature)
        print('*')
        tempAvg = np.average(tempList)
        tempSD = np.std(tempList)
        humAvg = np.average(humList)
        humSD = np.std(humList)
        # print("Creating dataframe...")
        logRow = pd.DataFrame([currentdatetime.strftime("%Y/%m/%d"), currentdatetime.strftime("%H:%M:%S"), tempAvg, tempSD, humAvg, humSD],
            index=['date', 'time', 'tempAvg', 'tempSD', 'humAvg', 'humSD'],
        ).T
        print("*     Current values:")
        print(logRow)
        print('*')
        # print("Logging to CSV now...")
        logRow.to_csv(
            './tempData.tsv',
            sep='\t',
            header=['date', 'time', 'tempAvg', 'tempSD', 'humAvg', 'humSD'],
            columns=['date', 'time', 'tempAvg', 'tempSD', 'humAvg', 'humSD'],
            index=False,
            mode='a',
            encoding='utf-8',
        )
        newTime = datetime.datetime.now()
        print(f"*     Time after logging: {newTime.strftime('%H:%M:%S')}")
        minutesToSleep = 1 - (newTime.minute % 2)
        secondsToSleep = 60 - newTime.second
        # if newTime.minute % 5 < 3:
        #     secondsToSleep -= 30
        print(f"*     Sleeping {minutesToSleep} minutes and {secondsToSleep} seconds before next log...")
        print('*')
        print('*' * 50)
        print()
        time.sleep((minutesToSleep * 60) + secondsToSleep)

if __name__ == '__main__':
    main()
