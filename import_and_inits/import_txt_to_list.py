#!/bin/python
all_inst = []
with open("inst.txt",'r') as f:
    for line in f:
        if line not in all_inst:
            print line
            all_inst.append(line)