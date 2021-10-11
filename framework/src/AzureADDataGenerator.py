import json
from faker import Faker
import random
from DataGenUtil import *
import shutil

MODELS = ['null', 'Surface Go', 'TravelMate B311-31', 'OEMST Product Name DV', 'HP Stream 11 Pro G5', 'Virtual Machine', 'VivoBook_ASUS Laptop E410MA_L410MA', 'HP Stream Laptop 11-ak0xxx','Surface Pro 6']
OPERATING_SYSTEM = ['Windows', 'macOS', 'AndroidForWork', 'iOS/iPadOS', 'Windows Mobile', 'IPhone']

Users_file = open('Users.json', 'r')
Users = json.load(Users_file)

AzureAdIDs = []
Result = []
Final = {}

for values in Users:
    for data in values['value']:
        AzureAdIDs.append(data['id'])

class AzureAdDataGenerator:
    def __init__(self):
        self.faker = Faker('en-US')
        Faker.seed(1)

    def generator_data(self,writer):
        for Id in AzureAdIDs:
            Result.append({
                "id": Id,
                "deviceId": self.faker.uuid4().replace('-',''),
                "model": random.choice(MODELS),
                "operatingSystem":random.choice(OPERATING_SYSTEM)
            })
        writer.write(f'AzureAD/devicesInfo.json', obj_to_json(Final))

Final['@odata.context'] = "https://graph.microsoft.com/v1.0/$metadata#devices"
Final['value'] = Result

destination = 'tmp_generated_data'
if os.path.exists(destination): shutil.rmtree(destination)
os.makedirs(destination)

dg = AzureAdDataGenerator()
writer = FileWriter(destination)
dg.generate_data(writer)
