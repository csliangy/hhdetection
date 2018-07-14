import os, sys, glob
import re
import json
import threading
import queue

import requests
import ProcessData

from time import sleep

gswitchid = [0]*12
gportindex = [0]*12
gporttrafficflag = [0]*12
gporttables =  [[] for i in range(12)]
gportabsolutetraffic = [x[:] for x in [[0]*256]*12]
gporttraffic = [x[:] for x in [[0]*256]*12]
gindexMapping = {}
gcount = 0
gindex = 0


class Switch(object):
    def __init__(self,switchID, count):
        self.switchID = switchID
        self.count = count
        self.flowentries = []
        self.trafficdata = []

    def getPortsList(self):
        portsList = []
        matches = []
        for item in self.flowentries:
            actions = dict(item)['ACTION']
            for action in actions:
                m = re.match(r'OUTPUT:\d+', str(action))
                if m:
                    port = (action.split(':'))[1]
                    if (int(port) not in portsList) and (int(port) <= 128):
                        portsList.append(int(port))
        portsList.sort()
        return portsList

    def addflowentries(self, flowentry):
        self.flowentries.append(flowentry)

    def addtrafficdata(self, porttraffic):
        self.trafficdata.append(porttraffic)

    def getPortMatches(self, portindex):
        matches = []
        for item in self.flowentries:
            actions = dict(item)['ACTION']
            for action in actions:
                m = re.match(r'OUTPUT:\d+', str(action))
                if m:
                    port = (action.split(':'))[1]
                    if portindex == int(port):
                        matches.append(dict(item)['MATCH'])
        return matches;                
                

def hhdetection(stop_event):
    while not stop_event.is_set():
        stop_event.wait(5)
        num_distance = 0
        array_i = []
        array_j = []
        distance = []
        sum_distance = 0
        max_avg = 0
        sum_avg = 0
        print()
        print()
        print("=====================================================")
        print("NOW HH DETECTION!!!!")

        for i in range(int(len(gportindex))):
            if sum(gporttraffic[i])/len(gporttraffic[i])  > max_avg:
                max_avg = sum(gporttraffic[i])/len(gporttraffic[i])
            sum_avg += sum(gporttraffic[i])/len(gporttraffic[i])
        avg_avg = sum_avg/len(gportindex)

        for i in range(len(gportindex)):
            if sum(gporttraffic[i])/len(gporttraffic[i]) > avg_avg: 
                for j in range(len(gportindex)):
                    if sum(gporttraffic[j])/len(gporttraffic[j]) > avg_avg:     
                        if gswitchid[i] != gswitchid[j]:
                            dis = ProcessData.euclidean_distance(gporttraffic[i], gporttraffic[j])
                            array_i.append(i)
                            array_j.append(j)
                            distance.append(dis)
                            sum_distance += dis
                            num_distance += 1

        if num_distance != 0:
            average_distance = sum_distance/num_distance
            sort_dis = sorted(range(len(distance)), key=lambda k: distance[k])
            for i in range(len(sort_dis)):
                k = sort_dis[i]
                print("distance[k] is "+str(distance[k]))
                #if distance[k] > average_distance:
                print("Hevey Hitter is "+ str(array_i[k]) + " "+str(array_j[k]))
                print("Distance is "+str(distance[k]))
                print(gporttables[array_i[k]])
                print(gporttables[array_j[k]])
        else:
            print("NO HH DETECTED!!!")
            



def DataRetrieve(switchID, input_queue, stop_event):
    global gcount
    gcount = 0

    while not stop_event.is_set():
        stop_event.wait(2)
        #threading.Timer(3.0, DataRetrieve, [switchID, stop_event]).start()

        for x in switchID:

            switchdata =  Switch(int(x), gcount)
            r = requests.get("http://103.10.233.113:8080/stats/flow/" + str(x))
            table = (r.json())[str(x)]
            if 0:

                print('****************************************************************************')
                print('****************************************************************************')
                print('SWITCH ID: '+ str(x))
                print('Number of flows: '+str(len(table)))

                print('------------------------------------------------------------------------')

            for flow in table:
                fte = {}
                if 0:
                   print('MATCH: ', end="  ")
                   print(flow['match'], end="|  ")
                   print('ACTIONS: ', end="  ")
                   print(flow['actions'], end="|  ")
                   print('PRIORITY: ', end="  ")
                   print(flow['priority'])
                fte['MATCH'] = flow['match']
                fte['ACTION'] =  flow['actions']
                switchdata.addflowentries(fte)


            r = requests.get("http://103.10.233.113:8080/stats/port/" + str(x))

            data = (r.json())[str(x)]
            for meta in data:
                traffic = {}
                if (int(meta['port_no'])) < 128:
                    if 0:
                        print('PORT: ', end="  ")
                        print(meta['port_no'])
                        print('TX PACKETS: ', end="  ")
                        print(meta['tx_packets'])
                        print('RX PACKETS: ', end="  ")
                        print(meta['rx_packets'])
                        print('TX BYTES: ', end="  ")
                        print(meta['tx_bytes'])
                        print('RX BYTES: ', end="  ")
                        print(meta['rx_bytes'])
                    traffic['PORT'] = (meta['port_no'])
                    traffic['TX_BYTES'] = meta['tx_bytes']
                    switchdata.addtrafficdata(traffic)
            if 0:        
                print('------------------------------------------------------------------------')
                print('****************************************************************************')
                print('****************************************************************************')
            input_queue.put(switchdata)
        print()
        print()
        gcount += 1
        gcount = gcount%256

def logData(input_queue, stop_event):
    global gindex
    global gswitchid
    global gportindex
    global gporttables
    global gporttraffic 
    global gporttrafficflag
    global gindexMapping
    while not stop_event.is_set():
        data = input_queue.get()
        if data is None:
            input_queue.task_done()
            return
        else:
            for port in list(data.getPortsList()):
                if 0:
                    print("PORT INDEX "+str(port))
                    print("SWITCH ID"+str(data.switchID))
                indexofList = data.switchID*1000+port
                if indexofList in gindexMapping.keys():
                    i = gindexMapping[indexofList]
                else:
                    gindexMapping[gindex] = indexofList
                    gindexMapping[indexofList] = gindex
                    i = gindex
                    gindex += 1
                gswitchid[i] = data.switchID
                gportindex[i] = port
                gporttables[i] = data.getPortMatches(int(port))

            for item in data.trafficdata:
                index_traffic = data.switchID*1000 + int(item['PORT'])
                gportabsolutetraffic[gindexMapping[index_traffic]][data.count] = int(item['TX_BYTES'])

                if data.count == 0:
                    gporttraffic[gindexMapping[index_traffic]][0] = \
                        (gportabsolutetraffic[gindexMapping[index_traffic]][0] - \
                        gportabsolutetraffic[gindexMapping[index_traffic]][255])/100000
                    print(gportabsolutetraffic[gindexMapping[index_traffic]])
                else:
                    gporttraffic[gindexMapping[index_traffic]][data.count] = \
                        (gportabsolutetraffic[gindexMapping[index_traffic]][data.count] - \
                        gportabsolutetraffic[gindexMapping[index_traffic]][data.count-1])/100000 

                if gporttrafficflag[gindexMapping[index_traffic]] == 0:
                    gporttraffic[gindexMapping[index_traffic]][0] = 0
                    gporttrafficflag[gindexMapping[index_traffic]] = 1
                    
                    
            for i in range(len(gportindex)):
                if 1:
                    print()
                    print()
                    print("===================================================FINAL DATA===================================================")
                    print("SWITCH ID:", end="  ")
                    print(gswitchid[i])  
                    print("OUTPUT PORT:", end="  ")
                    print(gportindex[i])
                    print()
                    print("FLOW TABLE ENTRY MATCHES:")
                    print(gporttables[i])
                    print()
                    print("TX BYTES OF THE PORT:")
                    print(gporttraffic[i])
                    print("=================================================FINAL DATA END=================================================")
                    print()
                    print()
 

def main():
    input_queue = queue.Queue()
    switchID = []
    stop_event = threading.Event() # used to signal termination to the threads

    r = requests.get("http://103.10.233.113:8080/stats/switches")
    responseContent = r.text[1:-1]
    [switchID.append(x.strip()) for x in responseContent.split(',')]

    collection_thread = threading.Thread(target=DataRetrieve, args=(switchID, input_queue, stop_event))
    collection_thread.start()

    logging_thread = threading.Thread(target = logData, args=(input_queue, stop_event))
    logging_thread.start()

    hhdetection_thread = threading.Thread(target = hhdetection, args=(stop_event, ))
    hhdetection_thread.start()

    try:
        sys.stdin.read()

    except (KeyboardInterrupt, SystemExit):
        # stop data collection. Let the logging thread finish logging everything in the queue
        stop_event.set()

if __name__ == '__main__':
    main()


