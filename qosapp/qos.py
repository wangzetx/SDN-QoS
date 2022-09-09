from imp import source_from_cache
import json
import base64
import http
import statistics
from tkinter import N
from tkinter.messagebox import NO
import traceback
from turtle import home
from unittest import result
from wsgiref.handlers import read_environ
from xml.dom.minicompat import NodeList
from .models import Flow, Meter
from django.forms.models import model_to_dict
def pre_get(url):
    try:
        userandpwd = 'admin:admin'
        auth = base64.b64encode(userandpwd.encode('utf-8'))
        headers = {"Authorization": "Basic " + str(auth, 'utf-8'), "Content-Type": "application/json" }
        conn = http.client.HTTPConnection('192.168.201.128:8181', timeout=3)
        conn.request(method="GET", url=url, headers = headers)
        response = conn.getresponse()
        if response.status in [200, 201]:
            print(response.status)
            data = json.loads(response.read())
            return {'status': 1, 'data': data}
        else:
            print(response.status)
            return {'status': 0}
    except Exception as e:
        import traceback
        traceback.print_exc


def get_flow():
    url = "/restconf/operational/opendaylight-inventory:nodes/node/openflow:1/table/0"
    result = pre_get(url)
    if(result['status'] == 0):
        return result
    print(result)
    flow = result['data']['flow-node-inventory:table'][0]['flow'] 
    for i in range(len(flow)):
        id = flow[i]['id']
        idle_timeout= flow[i]['idle-timeout']
        flags = flow[i]['flags']
        hard_timeout = flow[i]['hard-timeout']
        priority = flow[i]['priority']
        basic = {'id': id, 'idle-timeout': idle_timeout, 'flags': flags, 'hard-timeout': hard_timeout, 'priority': priority}  # 将id、idle-timeout...priorty等信息组成Basic字段存放到表flowtable中
        match = flow[i]['match']
        instructions = flow[i].get('instructions')
        statistics = flow[i].get('opendaylight-flow-statistics:flow-statistics')
        try:
            newflow = Flow(id = i+1, basic = basic, match = match, instructions = instructions, statistics = statistics)
            newflow.save()
        except:
            return {'status': 0}
    return {'status': 1}        

def refresh_flow():
    Flow.objects.all().delete()
    result = get_flow()
    if(result['status'] == 0):
        return result
    try:
        flowlist = Flow.objects.all().values()
        flowlist = [entry for entry in flowlist]
    except:
        return {'status': 0}
    return {"status": 1, "data": flowlist}   
    
def pre_put(url, body):
    try:
        auth = base64.b64encode('admin:admin'.encode())
        headers = {"Authorization": "Basic " + str(auth, 'utf-8'), "Content-Type": "application/json" }
        conn = http.client.HTTPConnection('192.168.201.128:8181', timeout=50)    
        conn.request("PUT", url, body, headers)
        response = conn.getresponse() 
        if response.status in [200,201]:
            return {"status": "success"}
        else:
            return {"status": "failure"}
    except Exception as e:
        import traceback
        traceback.print_exc()
def put_flow(flowInfo):
    switchID = flowInfo['switchID']
    flowSet = flowInfo['flowSet']
    body = json.dumps({'flow':flowSet})
    url = "/restconf/config/opendaylight-inventory:nodes/node/" + switchID + "/flow-node-inventory:table/0/flow/" + flowSet['id']
    result = pre_put(url, body)
    return result

def pre_delete(url):
    try:
        userandpwd = 'admin:admin'
        auth = base64.b64encode(userandpwd.encode('utf-8'))
        headers = {"Authorization": "Basic " + str(auth, 'utf-8'), "Content-Type": "application/json" }
        conn = http.client.HTTPConnection('192.168.201.128:8181', timeout=3)
        conn.request(method="DELETE", url=url, headers = headers)
        response = conn.getresponse()
        if response.status in [200,201]:
            print (response.status)
            print ('delete success')
            return {"status": 1}
        else:
            print (response.status)
            print ('delete failure')
            return {"status": 0}
    except Exception as e:
        import traceback
        traceback.print_exc
        return {'status': 0}    

def delete_flow(flowID, switchID):
    url = "/restconf/config/opendaylight-inventory:nodes/node/" + switchID + "/flow-node-inventory:table/0/flow/" + flowID
    result = pre_delete(url)
    return result

def refresh_meter():
    Meter.objects.all().delete()
    result = get_meter()
    if(result['status'] == 0):
        return result
    try:
        meterlist = Meter.objects.all().values()
        meterlist = [entry for entry in meterlist]
    except:
        return {'status': 0}
    return {"status": 1, "data": meterlist}

def get_meter():
    url = "/restconf/config/opendaylight-inventory:nodes/node/openflow:1/flow-node-inventory:meter/1"
    result = pre_get(url)
    if(result['status'] == 0):
        return result
    meter = result['data']['flow-node-inventory:meter'][0]
    Meter.objects.all().delete()
    basic = {'meter-id': meter['meter-id'], 'meterName': meter['meter-name'], 'flags': meter['flags']}
    meterBandHeaders = meter['meter-band-headers']
    try:
        newmeter = Meter(basic = basic, meterBandHeaders = meterBandHeaders, meterStatistics = None)
        newmeter.save()
        return {'status': 1}
    except:
        return {'status': 0}     
       
def put_meter(meterInfo):
    switchID = meterInfo['switchID']
    meterSet = meterInfo['meterSet']
    body = json.dumps({'meter':meterSet})
    url = "/restconf/config/opendaylight-inventory:nodes/node/" + switchID + "/flow-node-inventory:meter/1"
    result = pre_put(url, body)
    return result

def delete_meter(ID, switchID):
    url = "/restconf/config/opendaylight-inventory:nodes/node/" + switchID + "/flow-node-inventory:meter/1"
    result = pre_delete(url)
    return result

def refresh_topo():
    url = "/restconf/operational/network-topology:network-topology/topology/flow:1"
    result = pre_get(url)
    print(result)
    nodesList = result['data']['topology'][0]['node']
    linksList = result['data']['topology'][0]['link']
    nodes = list()
    links = list()
    for i in range(len(nodesList)):
        print(nodesList[i])
        nodei = {'node-id': nodesList[i]['node-id']}
        if('host' in nodei['node-id']):
            nodei['type'] = 'host'
        elif('openflow' in nodei['node-id']):
            nodei['type'] = 'switch'
        nodes.append(nodei)
    for i in range(len(linksList)):
        sourcei = linksList[i]['source']['source-node']
        desti = linksList[i]['destination']['dest-node']
        flag = 0
        for i in range(len(links)):
            if(links[i]['source-node'] == sourcei or links[i]['dest-node'] == sourcei):
                flag = 1
                break
        if(flag == 0):
            linki = {'source-node': sourcei, 'dest-node': desti}
            links.append(linki)
    data = {'nodes': nodes, 'links': links}
    result = {'status': 1, 'data': data}
    return result