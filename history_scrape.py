import sqlite3
import csv
import os
from datetime import datetime, timedelta

def getChromeHistory():
    data_path = os.path.expanduser('~')+"\AppData\Local\Google\Chrome\User Data\Default"    # WINDOWS file path
    history_db = os.path.join(data_path, 'history')
    # data_path = os.path.expanduser('~')+"/Library/Application Support/Google/Chrome/Default"  # MAC file path
    # history_db = os.path.join(data_path, 'history')
    try:
        conn = sqlite3.connect(history_db)
    except:
        print "There is a problem with your browser history file path. Please check your path and modify the 'data_path' variable according to that path.."
    conn.text_factory = str
    c = conn.cursor()
    output_file = open('chrome_history.csv', 'wb')
    csv_writer = csv.writer(output_file)
    headers = ('Url', 'Title', 'Visit Count', 'Date (GMT)')
    csv_writer.writerow(headers)
    epoch = datetime(1601, 1, 1)
    for row in (c.execute("select url, title, visit_count, last_visit_time from urls")):
        row = list(row)
        if row[3] != 0:
            row[3] = datetime.fromtimestamp(float(row[3])/1000000-11644473600).strftime("%Y-%m-%d %H:%M:%S")
        csv_writer.writerow(row)
    output_file.close()
    print 'Chrome history stored successfully..'

def getFirefoxHistory():
    data_path = os.path.expanduser('~')+"\AppData\Local\Mozilla\Firefox\Profiles\default"   # WINDOWS file path
    history_db = os.path.join(data_path, 'places.sqlite')
    # data_path = os.path.expanduser('~')+"/Library/Application Support/Firefox/Profiles/vdmhgkah.default"  # MAC file path
    # history_db = os.path.join(data_path, 'places.sqlite')
    try:
        conn = sqlite3.connect(history_db)
    except:
        print "There is a problem with your browser history file path. Please check your path and modify the 'data_path' variable according to that path.."
    conn.text_factory = str
    c = conn.cursor()
    output_file = open('firefox_history.csv', 'wb')
    csv_writer = csv.writer(output_file)
    headers = ('Url', 'Title', 'Visit Count', 'Date (GMT)')
    csv_writer.writerow(headers)
    epoch = datetime(1601, 1, 1)
    for row in (c.execute("select url, title, visit_count, last_visit_date from moz_places")):
        row = list(row)
        if row[3] is not None:
            row[3] = datetime.fromtimestamp(row[3]/1000000)
        csv_writer.writerow(row)
    output_file.close()
    print 'Firefox history stored successfully..'

if __name__ == '__main__':
    getChromeHistory()
    getFirefoxHistory()
    # getIEHistory()
