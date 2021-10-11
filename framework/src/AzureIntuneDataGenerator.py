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
OS_TYPES = ['Windows','Android','iOS/iPadOS','macOS']
class AzureIntuneDataGenerator:
    def __init__(self, number_of_records = 100):
        self.number_of_records = number_of_records
        self.faker = Faker('en_US')
        Faker.seed(1)

    def generate_data(self,writer):
        intune_data = []
        device = random.choice(DEVICE_DATA)
        for _ in range(self.number_of_records):
            user = self.faker.first_name()
            intune_data.append({
                'DeviceId': self.faker.uuid4(),
                'Model': '{} {}'.format(device['Make'],random.choice(device['Model'])), 
                'LastContact': str(self.faker.date_time_between(start_date='-30y', end_date='now')),
                'UPN': '{}@{}'.format(user,self.faker.free_email_domain()),
                'OS': random.choice(OS_TYPES)
            })
        writer.write(f'Intune/Activity.csv',list_of_dict_to_csv(intune_data))


destination = 'tmp_generated_data'
if os.path.exists(destination): shutil.rmtree(destination)
os.makedirs(destination)

dg = AzureIntuneDataGenerator()
writer = FileWriter(destination)
dg.generate_data(writer)


