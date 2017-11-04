# coding=utf-8

import os
import json
import random
import traceback
from flask import Flask, request
import requests
app = Flask(__name__, static_url_path="")


@app.route("/startRent", methods=['GET', 'POST'])
def start_rent():
    res = {}
    res['errorMsg'] = ""
    try:
        # generate post body
        log = ""
        print "----"
        print request.get_json()
        param = request.get_json()
        houseId = param['houseId']
        renter = param['renter']
        tenant = param['tenant']
        money = param['money']
        payload = {
            'rentHouseId': ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(16))),
            'payment': money,
            'house': houseId,
            'renter': renter,
            'tenant': tenant
        }
        # send post req
        log += "=========now start rent house========\n"
        log += "renter: " + renter + "\n"
        log += "tenant: " + tenant + "\n"
        log += "payment: " + str(money) + "\n"
        log += "strat to add one transaction=========>\n"

        rentReq = requests.post(
            "http://168.1.144.159:31090/api/RentHouse", data=payload)
        print "Rent house return: " + rentReq.text
        rentResult = json.loads(rentReq.text)
        if rentResult.has_key('error'):
            log += str(rentResult['error']['message']) + "\n"
            log += "!!!!!!!!!!!   Rent transaction operation failed   !!!!!!!!!!!\n"
            res['success'] = 0
            res['errorMsg'] += str(rentResult['error']['message']) + "\n"
        else:
            log += "Rent transaction operation success\n"

        transFormPayLoad = {
            'oldOwner': renter,
            'newOwner': tenant,
            'lock': houseId,
            'flag': True
        }
        log += "start to transform ownership=========>\n"
        log += "the house's owner change: " + renter + " --> " + tenant + "\n"
        log += "strat to add one transaction=========>\n"
        print log
        transReq = requests.post(
            "http://168.1.144.159:31090/api/TransferOwnership", data=transFormPayLoad)
        print "TransForm ownership return: " + transReq.text
        transformResult = json.loads(transReq.text)
        if transformResult.has_key('error'):
            log += str(transformResult['error']['message']) + "\n"
            log += "!!!!!!!!!!!   TransForm transaction operation failed   !!!!!!!!!!!\n"
            res['success'] = 0
            res['errorMsg'] = str(transformResult['error']['message'])
        else:
            log += "TransForm transaction operation success\n"
            res['success'] = 1
            res['errorMsg'] = ""

        res['Log'] = log
        print log

    except Exception, e:
        print(traceback.format_exc())
        print "Rent Error!!!"

    return json.dumps(res)


@app.route("/openLock", methods=['GET', 'POST'])
def open_lock():
    res = {}
    try:
        log = ""
        param = request.get_json()
        houseId = param['houseId']
        renter = param['renter']
        tenant = param['tenant']
        payLoad = {
            'newOwner': tenant,
            'lock': houseId,
            'order': 'lock'
        }
        log += "=========now start lock house========\n"
        log += "renter: " + renter + "\n"
        log += "tenant: " + tenant + "\n"
        log += "houseId: " + houseId + "\n"
        log += "strat to add one transaction=========>\n"
        r = requests.post(
            "http://168.1.144.159:31090/api/LockOrder", data=payLoad)
        print "open lock return: " + r.text
        result = json.loads(r.text)
        if result.has_key('error'):
            log += str(result['error']['message']) + "\n"
            log += "!!!!!!!!!!!   Lock transaction operation failed   !!!!!!!!!!!\n"
            res['success'] = 0
            res['errorMsg'] = str(result['error']['message'])
        else:
            log += "Lock transaction operation success\n"
            res['success'] = 1
            res['errorMsg'] = ""
    except Exception:
        print(traceback.format_exc())
        print "open lock Error!!!"
        pass
    # if the first time, start timing

    res['Log'] = log

    return json.dumps(res)


@app.route("/closeLock", methods=['GET', 'POST'])
def close_lock():
    r = requests.post("")
    res = {'message': r.text}
    return json.dumps(res)


@app.route("/search", methods=['GET', 'POST'])
def search_house():
    res = {
        "success": 1,
        "errorMsg": "",
        "houseNum": random.randint(1, 10)
    }
    return json.dumps(res)

if __name__ == "__main__":
    app.run(debug=True)
