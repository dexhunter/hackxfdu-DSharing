import requests
from random import *
import json

class Setup(object):
    def __init__(self):
        self.base_url = "http://168.1.144.159:31090/api/"
        self.first_name_list = ['Bob','Peter', 'Jane', 'Kelly', 'Easter', 'Addison', 'Fred', 'Alex', 'Ryan', 'Aidan', 'Kylie', 'Tommy','Willion', 'James', 'Solomon', 'Leon', 'Barry', 'Benson', 'Albert', 'Bruce']
        self.last_name_list = ['Black', 'Queen', 'Brown', 'Ryan', 'Butler', 'Murry']
        self.city_list = ['Shanghai', 'Beijing', 'Wuhan', 'Shenzhen', 'Nanjing']
        self.headers = {'Content_Type': 'application/json'}

    def generate_renter(self):
        print("generating renters...")
        for i in range(11):
            url = self.base_url + "Renter"
            data = {"renterId": "renter"+str(i),
                    "balance": str(randint(10,150)),
                    "firstName": self.first_name_list[randint(0,len(self.first_name_list)-1)],
                    "lastName": self.last_name_list[randint(0,len(self.last_name_list)-1)],
                    "descriptions": "no description",
            }
            if i==10:
                data = {"renterId": "None",
                    "balance": str(0),
                    "firstName": "None",
                    "lastName": "None",
                    "descriptions": "no description",
                }
            print(json.dumps(data))
            print(type(json.dumps(data)))
            break
            page = requests.post(url, headers = self.headers, data = json.dumps(data))
            print(str(i)+':   '+page.text+'\n')
        print("generating renters completed")

    def generate_tenant(self):
        print("generating tenants...")
        for i in range(10):
            url = self.base_url + "Tenant"
            data = {"tenantId": "tenant"+str(i),
                    "balance": str(randint(10,150)),
                    "firstName": self.first_name_list[randint(0,len(self.first_name_list)-1)],
                    "lastName": self.last_name_list[randint(0,len(self.last_name_list)-1)],
                    "descriptions": "no description",
            }
            page = requests.post(url, headers = self.headers, data = data)
            print(str(i)+':   '+page.text+'\n')
        print("generating tenants completed")

    def generate_house(self):
        print("generating houses...")
        for i in range(10):
            url = self.base_url + 'House'

            data = {"houseId": "house"+str(i),
                    "details": {
                        "address": {
                            "city": self.city_list[randint(0, len(self.city_list)-1)],
                            "street": 'STREET',
                            "detail": str(randint(100,800)),
                            "id": "default",
                        },
                        "area": str(randint(60,200)),
                        "id": "default",
                    },
                    "gas": str(0),
                    "price": str(2),
                    "owner": "render"+str(i),
                    "user": "None",
                    "descriptions": "no description"
            }
            print(type(data))
            print(data)
            print(data['details'])
            print(data['details']['address'])
            headers = {'content-type': 'application/json'}
            page = requests.post(url, data=json.dumps(data), headers=headers)
            print(str(i)+":  "+page.text+'\n')
        print("generating houses completed")




test = Setup()
test.generate_renter()
test.generate_tenant()
test.generate_house()


