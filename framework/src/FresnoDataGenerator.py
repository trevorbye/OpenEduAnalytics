from ctypes import windll
from faker import Faker
import string
import random
import shutil
from DataGenUtil import *

DEVICE_DATA = [
    {
        'Make': 'Dell',
        'Model': ['Vostro 15 3501','Vostro 5410','Latitude 15 5520']
    },
    {
        'Make': 'Lenovo',
        'Model': ['ThinkBook 14s Yoga','Yoga Slim 7','X1 Titanium Yoga']
    },
    {
        'Make': 'HP',
        'Model': ['ENVY Laptop 14-eb0019TX','Pavilion Laptop 14-ec0007AX','Spectre x360 14-ea0542TU']
    }
]

WIN_TYPES = ['Pro','Home','Enterprise']
ARCH_TYPES = ['64 bit','32 bit']
MONITOR_TYPES = [('1080','768'),('1920','1080')]
ISP = ['AT&T', 'Verizon', 'Comcast', 'Vodafone']

class FresnoDataGenerator:
    def __init__(self, number_of_records = 100):
        self.number_of_records = number_of_records
        self.faker = Faker('en_US')
        Faker.seed(1)

    def generate_data(self,writer):
        fresno_data = []
        device = random.choice(DEVICE_DATA)
        monitor_width,monitor_height = random.choice(MONITOR_TYPES)
        for _ in range(self.number_of_records):
            fresno_data.append({
                'IPAddress': self.faker.ipv4(),
                'MacAddress':self.faker.mac_address(),
                'Make':device['Make'],
                'Model':random.choice(device['Model']),
                'Serial Number':''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(7)]),
                'Download Speed':round(random.uniform(5,150),4),
                'Upload Speed':round(random.uniform(5,300),4),
                'Latency':round(random.uniform(0,30),1),
                'Computer User': self.faker.first_name(),
                'Host Name': self.faker.first_name(), # This needs to be verified.
                'OS':'Microsoft Windows 10 {}'.format(random.choice(WIN_TYPES)),
                'Arch':random.choices(ARCH_TYPES,weights=[80,20])[0],
                'IEVer':'9.11.{}.0'.format(str(self.faker.random_number(digits=5))),
                'Monitors':  '\"[{\""Width"\": \""'+ str(monitor_width)+'"\",\""Height":\""'+ str(monitor_height)+'"\"}]\"',
                'Long': 100 + round(random.uniform(0,10),4),
                'Lat': 50 + round(random.uniform(0,10),4),
                'ISP':random.choice(ISP),
                'ClientIp': self.faker.ipv4(),
                'NetworkInterface':'Wireless 80211',
                'Datetime':str(self.faker.date_time_between(start_date='-1m', end_date='now'))
            })
        writer.write(f'Fresno/Activity.csv',list_of_dict_to_csv(fresno_data))


destination = 'tmp_generated_data'
if os.path.exists(destination): shutil.rmtree(destination)
os.makedirs(destination)

dg = FresnoDataGenerator()
writer = FileWriter(destination)
dg.generate_data(writer)


