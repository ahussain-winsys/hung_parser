import sys
import os
import datetime
import csv
from tkinter import filedialog as fd

class file:
    def __init__(self, filepath):
        self.filepath = filepath
        self.line = dict ([('index', 0), ('timestamp', ''), ('delta_S', 0), ('pass', False)])
        self.lines = []
        self.minDelta_S = 230
        self.maxDelta_S = 250
        self.csvpath = ""
        self.createCSVPath()
        self.openFile()

    def createCSVPath(self):
        base_name, _ = os.path.splitext(self.filepath)
        self.csvpath = base_name + ".csv"

    def openFile(self):
        numLines = 5
        timeFormat = "%I:%M:%S.%f"
        previousTimestamp = datetime.time
        dummyDate = datetime.datetime(2024,1,1)

        f = open(self.filepath)
        content = f.readlines()

        for i in range(0, len(content), numLines):
            chunk = content[i:i+numLines]
            print("--------------------------------")
            dictline = self.line
            dictline['index'] = int(chunk[1])
            dictline['timestamp'] = datetime.datetime.strptime(chunk[2].split()[3][:-1],timeFormat).time()
            
            if dictline['index'] <= 1:
                dictline['delta_S'] = 0.0
            else:
                dictline['delta_S'] = ( datetime.datetime.combine(dummyDate,dictline['timestamp']) - datetime.datetime.combine(dummyDate,previousTimestamp) ).total_seconds()
            previousTimestamp = dictline['timestamp']
            dictline['timestamp'] = dictline['timestamp'].strftime('%I:%M:%S.%f')[:-3]
            if dictline['delta_S'] < 0:
                dictline['delta_S'] = dictline['delta_S'] + 43200
            if (dictline['delta_S'] <= self.maxDelta_S) and (dictline['delta_S'] >= self.minDelta_S):
                dictline['pass'] = True
            else:
                dictline['pass'] = False
            print(chunk)
            print(dictline)
            self.lines.append(dictline.copy())
        #print(self.lines)

    def saveCSV(self):
        fields = self.lines[0].keys()
        with open(self.csvpath, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=fields)
            writer.writeheader()
            writer.writerows(self.lines)

def main():
    filename = fd.askopenfilename(filetypes=[('Text Files','*.txt')])
    f = file(filename)
    f.saveCSV()

if __name__ == '__main__':
    sys.exit(main())