# # -*- coding: utf-8 -*-
import sys
import csv
from pyproj import Proj, transform
import time

t0 = time.time()
if (len(sys.argv)==3):
    try:
        with open(sys.argv[1],'r') as csvinput:
            with open(sys.argv[2], 'w') as csvoutput:
                writer = csv.writer(csvoutput, lineterminator='\n')
                reader = csv.reader(csvinput)

                all = []
                blank = ""
                row = next(reader)
                try:
                    x = row.index("X") # find X column
                    y = row.index("Y") # find Y column
                except ValueError:
                    print "Can not find X or Y Column!"
                    exit
                else:
                    row.append('Latitude')  # Add Latitude column
                    row.append('Longtitude')# Add Longtitud column
                    all.append(row)
                    #print("Found X and Y Column!")
                    print("Starting convert X,Y to Lat,Lon...")
                    for row in reader:
                        if (row[x] != "" and row[y] != ""):
                            newcol = transform(Proj(init='epsg:3857'), Proj(init='epsg:4326'), row[x], row[y])
                            newcol = '%s %s' % newcol
                            newcol = newcol.split()
                            row.append(newcol[0])
                            row.append(newcol[1])
                            #print(newcol[0]+","+newcol[1])
                            all.append(row)
                        else:
                            row.append(blank)
                            row.append(blank)
                            all.append(row)

                    writer.writerows(all)
                    t1 = time.time()
                    print("Done! total time usage: ") + str(t1-t0)
    except:
        print("Input file not found!")
else:
    print("Usage: python mea.py <inputfile> <outputfile>")
