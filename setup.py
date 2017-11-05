import requests
from random import *
import json

serial = 0
class Setup(object):
    def __init__(self):
        self.base_url = "http://168.1.144.159:31090/api/"
        self.first_name_list = ['Bob','Peter', 'Jane', 'Kelly', 'Easter', 'Addison', 'Fred', 'Alex', 'Ryan', 'Aidan', 'Kylie', 'Tommy','Willion', 'James', 'Solomon', 'Leon', 'Barry', 'Benson', 'Albert', 'Bruce']
        self.last_name_list = ['Black', 'Queen', 'Brown', 'Ryan', 'Butler', 'Murry']
        self.city_list = ['Shanghai', 'Beijing', 'Wuhan', 'Shenzhen', 'Nanjing']
        self.headers = {'Content-Type': 'application/json'}
        
    def generate_renter(self):
        print("generating renters...")
        for i in range(11):
            url = self.base_url + "Renter"
            data = {"renterId": "renter"+str(i+serial),
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
            page = requests.post(url, headers = self.headers, data = data)
            print(str(i+serial)+':   '+page.text+'\n')
        print("generating renters completed")
        
    def generate_tenant(self):
        print("generating tenants...")
        for i in range(10):
            url = self.base_url + "Tenant"
            data = {"tenantId": "tenant"+str(i+serial),
                    "balance": str(randint(10,150)),
                    "firstName": self.first_name_list[randint(0,len(self.first_name_list)-1)],
                    "lastName": self.last_name_list[randint(0,len(self.last_name_list)-1)],
                    "descriptions": "no description",
            }
            page = requests.post(url, headers = self.headers, data = data)
            print(str(i+serial)+':   '+page.text+'\n')
        print("generating tenants completed")

    def generate_house(self):
        print("generating houses...")
        url = self.base_url + 'House'
        for i in range(10):
            data = {"houseId": "house"+str(i+serial),
                    "details": {
                        "address": {
                            "city": self.city_list[randint(0, len(self.city_list)-1)],
                            "street": "STREET",
                            "detail": str(randint(serial,800)),
                            "id": "default",
                        },
                        "area": str(randint(60,200)),
                        "id": "default",
                    },
                    "gas": str(0),
                    "price": str(randint(5,10)),
                    "owner": "renter"+str(i+serial),
                    "user": "None",
                    "descriptions": "no description"
            }
            page = requests.post(url, headers = self.headers, data = json.dumps(data))
            print(str(i+serial)+":  "+page.text+'\n')
        print("generating houses completed")

    def generate_order(self):
        print("generating orders...")
        url = self.base_url + 'Order'
        data = {"orderId": "lock", "oneOrder": "LOCK"}
        page = requests.post(url, headers = self.headers, data = data)
        print(page.text + '\n')
        data = {"orderId": "unlock", "oneOrder": "UNLOCK"}
        page = requests.post(url, headers = self.headers, data = data)
        print(page.text + '\n')
        print("generating orders completed")

    def generate_lock(self):
        print("generating locks...")
        url = self.base_url + 'Lock'
        for i in range(10):
            data = {"lockId": "house"+str(i+serial),
                    "userKey": "None",
                    "masterKey": "renter"+str(i+serial),
                    "enable": "false",
                    "status": "true",
                }
            page = requests.post(url, headers = self.headers, data = json.dumps(data))
            print(str(i+serial)+":   "+page.text+'\n')
        print("generating locks completed")
        
    def generate_all(self):
        self.generate_renter()
        self.generate_tenant()
        self.generate_house()
        self.generate_order()
        self.generate_lock()

if __name__ == '__main__':
    test = Setup()        
    test.generate_all()
