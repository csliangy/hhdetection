#!/usr/bin/python

import os, sys, glob
import re
import matplotlib.pyplot as plt
from pylab import *

smooth_threshold_data = []

def apca(raw_data):
    N = 16
    RawData_len = len(raw_data)
    APCA_len = 2**(math.ceil(math.log(RawData_len, 2)))
    data = [0] * APCA_len
    data[0:RawData_len] = raw_data[0:RawData_len]

    left_x = []
    for i in range(0, len(data), 2):
        left_x.append(i)
        
    right_x = []
    right_x = left_x[:]
    for i in range(len(right_x)):
        right_x[i] += 1
    number_of_segments = len(left_x)

    seg_lx = []
    seg_rx = []
    seg_mc = []
    for i in range(number_of_segments):
        seg_lx.append(left_x[i])
        seg_rx.append(right_x[i])
        seg_mc.append(sys.maxsize)

    
    for i in range(number_of_segments-1):
        coef = np.polyfit([j for j in range(seg_lx[i], seg_rx[i+1]+1)], [data[index] for index in [j for j in range(seg_lx[i], seg_rx[i+1]+1)]], 0)
        seg_mc[i] = sum(math.pow((item-coef[0]),2) for item in data[seg_lx[i]:seg_rx[i+1]+1])

    while number_of_segments > N:
        min_index = seg_mc.index(min(seg_mc))
        
        #Any item not the first one, not the last and 2nd last one
        if min_index > 0 and min_index < number_of_segments-2:
            coef = np.polyfit([j for j in range(seg_lx[min_index], seg_rx[min_index+2]+1)], [data[index] for index in [j for j in range(seg_lx[min_index], seg_rx[min_index+2]+1)]], 0)
            seg_mc[min_index] = sum(math.pow((item-coef[0]),2) for item in data[seg_lx[min_index]:seg_rx[min_index+2]+1])
            del seg_mc[min_index+1]
            seg_rx[min_index] = seg_rx[min_index+1]
            del seg_lx[min_index+1]
            del seg_rx[min_index+1]

            #Update mc of the previous node
            
            Pre_index = min_index - 1
            coef = np.polyfit([j for j in range(seg_lx[Pre_index], seg_rx[Pre_index+1]+1)], [data[index] for index in [j for j in range(seg_lx[Pre_index], seg_rx[Pre_index+1]+1)]], 0)
            seg_mc[Pre_index] =  sum(math.pow((item-coef[0]),2) for item in data[seg_lx[Pre_index]:seg_rx[Pre_index+1]+1])

        #First node, merge with the 2nd one
        elif min_index == 0:
            coef = np.polyfit([j for j in range(seg_lx[min_index], seg_rx[min_index+2]+1)], [data[index] for index in [j for j in range(seg_lx[min_index], seg_rx[min_index+2]+1)]], 0)
            seg_mc[min_index] = sum(math.pow((item-coef[0]),2) for item in data[seg_lx[min_index]:seg_rx[min_index+2]+1])
            del seg_mc[min_index+1]
            seg_rx[min_index] = seg_rx[min_index+1]
            del seg_lx[min_index+1]
            del seg_rx[min_index+1]

        #2nd last node, merge with the last one
        #The last node has the maximum value, so the last node will NOT be the mimimum one
        else:
            seg_rx[min_index] = seg_rx[min_index+1]
            seg_mc[min_index] = sys.maxsize
            del seg_mc[min_index+1]
            del seg_lx[min_index+1]
            del seg_rx[min_index+1]
            
            Pre_index = min_index - 1
            coef = np.polyfit([j for j in range(seg_lx[Pre_index], seg_rx[Pre_index+1]+1)], [data[index] for index in [j for j in range(seg_lx[Pre_index], seg_rx[Pre_index+1]+1)]], 0)
            seg_mc[Pre_index] =  sum(math.pow((item-coef[0]),2) for item in data[seg_lx[Pre_index]:seg_rx[Pre_index+1]+1])
            
        number_of_segments -= 1

    sig_best = []
    apca = []
    for i in range(0, N):
        coef = np.polyfit([j for j in range(seg_lx[i], seg_rx[i]+1)], [data[index] for index in [j for j in range(seg_lx[i], seg_rx[i]+1)]], 0)
        sig_best.append(coef[0])
        apca.append(sig_best[i])
        apca.append(seg_rx[i])
    return apca

def euclidean_distance(apca_raw1, apca_raw2):
    apca1 = apca(apca_raw1)
    apca2 = apca(apca_raw2)
    x1 = []
    x2 = []
    x1_value = []
    x2_value = []
    x_merge = []
    x_merge.append(0)
    for i in range(0, len(apca1)):
        if i%2 == 0:
            x1_value.append(apca1[i])
        else:
            x1.append(apca1[i])
    for i in range(0, len(apca2)):
        if i%2 == 0:
            x2_value.append(apca2[i])
        else:
            x2.append(apca2[i])


    x_merge += ([element for element in x1])
    x_merge += ([element for element in x2])
    x_merge.sort()
    x_merge = x_merge[:-1]


    x1_cur_value = x1_value[0]
    x2_cur_value = x2_value[0]
    y_high = []
    y_low = []
    for x in x_merge[:-1]:
        if x in x1:
            x1_cur_value = x1_value[x1.index(x)+1]
        if x in x2:
            x2_cur_value = x2_value[x2.index(x)+1]
        if x1_cur_value > x2_cur_value:
            y_high.append(x1_cur_value)
            y_low.append(x2_cur_value)       
        else:
            y_high.append(x2_cur_value)
            y_low.append(x1_cur_value)

        
    distance = sum([(x_merge[i+1]-x_merge[i])*(y_high[i]-y_low[i]) for i in range(len(x_merge)-1)])
    return distance

def smoothing_thresholding(RawArray, K, T):
    global smooth_threshold_data
    M = sys.maxsize
    SmoothingArray = []
    for i in range(int(len(RawArray)/K)):
        for j in range(K):
            if RawArray[i*K+j] < M:
                M = RawArray[i*K+j]
        SmoothingArray.append(M)
        M = sys.maxsize
    return SmoothingArray;
       


def export_apca_distance(raw1, raw2, K, T):
    apca_raw1 = []
    apca_raw2 = []   
    apca_raw1 = smoothing_thresholding(RawArray1, K, T) 
    apca_raw2 = smoothing_thresholding(RawArray2, K, T) 

#Step 6: APCA Transform
    apca1 = apca(apca_raw1)
    apca2 = apca(apca_raw2)
    print(apca1)
    print(apca2)

    distance = euclidean_distance(apca1, apca2)
    return distance
 
def main():

    data = [0, 131453278, 131421852, 131973792, 131660696, 131743056, 131713148, 131784236, 66140280, 197762832, 65970360, 131710112, 131782200, 131858360, 132033480, 131695158, 131721384, 131563382, 131547684, 131954382, 131564738, 131512519, 131838206, 131619516, 131781520, 131806780, 131820862, 132064260, 132403454, 132199718, 131578336, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    data1 = [x/1000 for x in data]
    testapca = apca(data1)
    print(testapca)
  

def main_test():
    global smooth_threshold_data
    args = sys.argv[1:]


    if not args:
        print('usage: [--filename1] raw_date_filename_1: [--filename2] raw_date_filename_2: [--K nearest neighbor] K: [-- Threshold] ' )
        sys.exit(1)

    K = int(args[2])
    T = int(args[3])


#Remove the existing Windowing files
    files = []
    for name in os.listdir('.'):
        m = re.search(r'Window',name)
        if m:
            files.append(name)
    
    for name in files:
        print(name)
        try:
            os.remove(name)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

#Preprea Raw Data Array
    RawData1 = open(args[0],'r')
    RawArray1 = []
    for line in RawData1:
        RawArray1.append(int(line) >> 10)
    RawData1.close()

    RawData2 = open(args[1],'r')
    RawArray2 = []
    for line in RawData2:
        RawArray2.append(int(line) >> 10)
    RawData2.close()

   
    apca_raw1 = []
    apca_raw2 = []   
    smoothing_thresholding(RawArray1, K, T) 
    apca_raw1[:] = smooth_threshold_data[:]
    smooth_threshold_data = []

    smoothing_thresholding(RawArray2, K, T) 
    apca_raw2[:] = smooth_threshold_data[:]

#Step 6: APCA Transform
    apca1 = []
    apca1 = apca(apca_raw1)
    apca2 = apca(apca_raw2)
    print(apca1)
    print(apca2)

    distance = euclidean_distance(apca1, apca2)
    print("FINAL DISTANCE is "+str(distance))


    
if __name__ == '__main__':
    data = [12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54,
    12,32,43,54,76,87,545,353,54,65,76,343,34,12,34,54]

    main()
    

