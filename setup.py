import requests
import csv
from datetime import datetime


def process():
    try:
        url = settings["url_csv"]
    except KeyError:
        raise ImporterException('Please, set variable "url_csv" in settings!')

    r = requests.get(url)
    reader = csv.DictReader(r.text.splitlines(), delimiter=',')

    return put_items_into_datastore(reader)


def put_items_into_datastore(reader):
    for item in reader:
        if item['Quantity'] == "N/A" or item['Quantity'] == "":
            item['Quantity'] = 0
        sid = datastore.sid(item['Product'], item['Flow'], item['Country'])
        date_object = datetime.strptime(item['Date'], '%b%Y')
        datastore.put_points(sid, [Point(date_object, item['Quantity'])])
        datastore.put_fields(sid, {'Code': item['Code'], 'Country': item['Country']})

    return True


def trigger():
    return False