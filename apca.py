#!/usr/bin/python

import os, sys, glob
import re
import matplotlib.pyplot as plt
from pylab import *
import numpy as np
import math
from array import array

def apca(data, N):
    RawData_len = len(data)
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

def apca_draw(fig, data, apca, index, total):
    #Draw the figure to show APCA Result
    seg_lx = []
    seg_rx = []
    seg_best = []

    i = 0
    for meta in apca:
        if i == 0:
            seg_best.append(float(meta))
        elif i%2 == 0:
            seg_best.append(float(meta))
        else:
            seg_rx.append(int(meta))
        i += 1

    N = i >> 1

    if index == 0:
        c = "blue"
    else:
        c = "green"
        

    seg_lx.append(0)
    seg_lx += ([x+1 for x in seg_rx[:-1]])

    for i in range(1, N):
        seg_lx[i] -= 1
        
    ax = fig.add_subplot(2*total+1,1,index*total+1)

    ax.set_title("Time Series Data") 
    plt.plot([x for x in range(len(data))],data,c)
    plt.subplots_adjust(hspace = 1)
    ax = fig.add_subplot(2*total+1,1,index*total+2)
    for i in range(N):
        plt.plot([j for j in range(seg_lx[i], seg_rx[i]+1)], [seg_best[i] for j in range(seg_lx[i], seg_rx[i]+1)],c)
        ax.set_title("APCA Representation") 
        if i != 0:
            plt.plot([seg_lx[i],seg_lx[i]], [seg_best[i-1],seg_best[i]],c)

def distance_fill(fig, x_merge, y_high, y_low, total_plot):
    ax = fig.add_subplot(total_plot,1,total_plot)
    ax.set_title("APCA Euclidean Distance") 
    for i in range(len(x_merge)-1):
        rect = matplotlib.patches.Rectangle((x_merge[i], y_low[i]), x_merge[i+1]-x_merge[i], y_high[i]-y_low[i], facecolor="grey")
        ax.add_patch(rect)


def distance_draw(fig, apca1, apca2, total_plot):
    #Draw the figure to show APCA Result
    for index in range (0,2):
        seg_lx = []
        seg_rx = []
        seg_best = []
        
        if index == 0:
            apca = apca1
            c = "blue"
        else:
            apca = apca2
            c = "green"

        i = 0
        for meta in apca:
            if i == 0:
                seg_best.append(float(meta))
            elif i%2 == 0:
                seg_best.append(float(meta))
            else:
                seg_rx.append(int(meta))
            i += 1

        N = i >> 1
        seg_lx.append(0)
        seg_lx += ([x+1 for x in seg_rx[:-1]])

        for i in range(1, N):
            seg_lx[i] -= 1

        ax = fig.add_subplot(total_plot,1,total_plot)
        
        for i in range(N):
            plt.plot([j for j in range(seg_lx[i], seg_rx[i]+1)], [seg_best[i] for j in range(seg_lx[i], seg_rx[i]+1)],c)
            if i != 0:
                plt.plot([seg_lx[i],seg_lx[i]], [seg_best[i-1],seg_best[i]],c)        

    
def euclidean_distance(fig, apca1, apca2, total_plot):
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

    distance_draw(fig, apca1, apca2, total_plot)
    distance_fill(fig, x_merge, y_high, y_low, total_plot)
        
    distance = sum([(x_merge[i+1]-x_merge[i])*(y_high[i]-y_low[i]) for i in range(len(x_merge)-1)])
    return distance
    

def main():
    args = sys.argv[1:]
    if not args:
        print('usage: [--filename] raw_date_filename: [--N] APCA points:')
        sys.exit(1)

    if len(args) != 2:
        print('Error number of arguments, usage: [--filename] raw_date_filename: [--N] APCA points:')
        sys.exit(1)
    
    RawDataFile = open(args[0], 'r')
    data = []
    for line in RawDataFile:
        data.append(int(line))
    RawDataFile.close()

    N = int(args[1])

    data1 = [1,5,4,2,9,11,21,8,21,32,12,3,8,12,18,23]
    data2 = [11,15,33,32,9,5,8,8,9,12,2,3,5,1,30,33]
    RawData_len = len(data)
    APCA_len = 2**(math.ceil(math.log(RawData_len, 2)))
 
    Step_APCA = int(args[1])

    apca1 = apca(data1, 4)
    apca2 = apca(data2, 4)

    fig = plt.figure()
    apca_draw(fig, data1, apca1, 0, 2)
    apca_draw(fig, data2, apca2, 1, 2)
    

    e_distance = euclidean_distance(fig, apca1, apca2, 5)
    print("The APCA euclidean distance of the two time series data is ",e_distance)
    distance = sum([abs((data1[i]-data2[i])) for i in range(len(data1))])
    print("The RAW Data euclidean distance of the two time series data is ", distance)
    

    show()
    
    
    


        

    
                             

if __name__ == '__main__':
    main()
