# coding=utf-8

import os
import json
import random
import traceback
import time
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, request
import requests
from datetime import datetime
import serial.tools.list_ports as sls


#TODO: remove pyduino dependency
try:
    from pyduino import *
    useuno = True
except ImportError:
    useuno = False

app = Flask(__name__, static_url_path="")

conn = sls.comports()
conn1 = False
conn2 = False
for port in conn:
    if 'ACM0' in port.name:
        conn2 = True
    elif 'USB0' in port.name:
        conn1 = True
if len(conn) > 0:
    app.logger.info("Find the device")
else:
    app.logger.info("did not find the device, no iot involved")
    useuno = False


if useuno:
# arduino control
    if conn1:
        a = Arduino(serial_port='/dev/ttyUSB0')
        time.sleep(3)
        app.logger.info("use /dev/ttyUSB0")
    if conn2:
        a = Arduino(serial_port='/dev/ttyACM0')
        time.sleep(3)
        app.logger.info("use /dev/ttyACM0")

    LED_PIN = 13
    a.set_pin_mode(LED_PIN, 'O')
    a.digital_write(LED_PIN, 0)
    app.logger.info('Arduino initialized')


@app.route("/startRent", methods=['GET', 'POST'])
def start_rent():
    res = {}
    res['errorMsg'] = ""
    try:
        # generate post body
        log = ""
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
        log += "start to add one transaction=========>\n"

        rentReq = requests.post(
            "http://168.1.144.159:31090/api/RentHouse", data=payload)
        app.logger.info( "Rent house return:%s " % rentReq.text)
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
            'flag': "true"
        }
        log += "start to transform ownership=========>\n"
        log += "the house's owner change: " + renter + " --> " + tenant + "\n"
        log += "start to add one transaction=========>\n"
        app.logger.info(log)
        transReq = requests.post(
            "http://168.1.144.159:31090/api/TransferOwnership", data=transFormPayLoad)
        print( "TransForm ownership return: %s" % transReq.text)
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
        app.logger.info(log)

    except Exception, e:
        app.logger.info(traceback.format_exc())
        app.logger.info("Rent Error!!!")

    return json.dumps(res)


@app.route("/Unlock", methods=['GET', 'POST'])
def unlock():
    log = ""
    res = {}
    start_time = time.time()
    param = request.get_json()
    houseId = param['houseId']
    renter = param['renter']
    tenant = param['tenant']
    payLoad = {
    'newOwner': tenant,
    'lock': houseId,
    'order': 'unlock'
    }
    r = requests.post("http://168.1.144.159:31090/api/LockOrder", data=payLoad)
    app.logger.info('%s'%r)
    if useuno:
        app.logger.info('Arduino Operation Started')
        a.digital_write(LED_PIN, 1) #set light on
    result = json.loads(r.text)
    if result.has_key('error'):
        log += str(result['error']['message']) + "\n"
        app.logger.info('%s'%result['error']['message'])
        log += "!!!!!!!!!!!   Unlock transaction operation failed   !!!!!!!!!!!\n"
        res['success'] = 0
        res['errorMsg'] = str(result['error']['message'])
    else:
        log += "Unlock transaction operation success\n"
        res['success'] = 1
        res['errorMsg'] = ""

    time.sleep(3)

    payLoad = {
    'newOwner': tenant,
    'lock': houseId,
    'order': 'lock'
    }
    r = requests.post("http://168.1.144.159:31090/api/LockOrder", data=payLoad)
    app.logger.info('%s'%r)
    if useuno:
        a.digital_write(LED_PIN, 0) #set light off
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

    return json.dumps(res)

@app.route("/AutoReturn", methods=['GET', 'POST'])
def auto_return():
    """
    Automatically return the house to renter
    """
    log = ""
    res = {}
    payLoad = {}

    start_time = time.time()
    if request.method == 'GET':
        print("GETTTTTTTTTTTTTTTTTTTTTTTTTTT")
        r = requests.get("http://168.1.144.159:31090/api/RentHouse")
        print(type(r))
        result = json.loads(r.content)
        app.logger.info('%s'%result)
        print type(result) #list
        for dic in result:
            for data in dic.keys():
                if data == 'timestamp':
                    print dic[data]
                    print dateutil.parser(datetime.utcfromtimestamp(dic[data]))

    elif request.method == 'POST':
        param = request.get_json()
        rentHouseId = param.get('rentHouseId', 'rent1')
        payment = param.get('payment', 10)
        house = param.get('house', 'house1')
        renter = param.get('renter', 'renter1')
        tenant = param.get('tenant', 'tenant1')
        payLoad = {
            "rentHouseId": rentHouseId,
            "payment": payment,
            "house": house,
            "renter": renter,
            "tenant": tenant,
        }

        r = requests.post("http://168.1.144.159:31090/api/RentHouse", data=payLoad)
        result = json.loads(r.text)
        app.logger.info('%s'%result)

        if result.has_key('error'):
            log += str(result['error']['message']) + "\n"
            log += "!!!!!!!!!!!   Lock transaction operation failed   !!!!!!!!!!!\n"
            res['success'] = 0
            res['errorMsg'] = str(result['error']['message'])
        else:
            log += "Lock transaction operation success\n"
            res['success'] = 1
            res['errorMsg'] = ""

    return json.dumps(res)


@app.route("/returnRent", methods=['GET', 'POST'])
def return_rent():
    res = {}
    res['errorMsg'] = ""
    try:
        # generate post body
        log = ""
        app.logger.info( "----")
        param = request.get_json()
        houseId = param['houseId']
        renter = param['renter']
        tenant = param['tenant']
        payload = {
            'returnHouseId': ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(16))),
            'house': houseId,
            'renter': renter,
            'tenant': tenant
        }
        # send post req
        log += "=========now start return house========\n"
        log += "renter: " + renter + "\n"
        log += "tenant: " + tenant + "\n"
        log += "start to add one transaction=========>\n"

        rentReq = requests.post(
            "http://168.1.144.159:31090/api/ReturnHouse", data=payload)
        print( "Return house return:%s " % rentReq.text)
        rentResult = json.loads(rentReq.text)
        if rentResult.has_key('error'):
            log += str(rentResult['error']['message']) + "\n"
            log += "!!!!!!!!!!!   Return transaction operation failed   !!!!!!!!!!!\n"
            res['success'] = 0
            res['errorMsg'] += str(rentResult['error']['message']) + "\n"
        else:
            log += "Return transaction operation success\n"


        transFormPayLoad = {
            'oldOwner': renter,
            'newOwner': tenant,
            'lock': houseId,
            'flag': "false"
        }
        log += "start to transform ownership=========>\n"
        log += "the house's owner change: " + renter + " --> " + tenant + "\n"
        log += "start to add one transaction=========>\n"
        app.logger.info(log)
        transReq = requests.post("http://168.1.144.159:31090/api/TransferOwnership", data=transFormPayLoad)
        print( "TransForm ownership return: %s" % transReq.text)
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
        app.logger.info(log)

    except Exception, e:
        app.logger.info(traceback.format_exc())
        app.logger.info("Return Error!!!")

    return json.dumps(res)


if __name__ == "__main__":
    handler = RotatingFileHandler('test.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
