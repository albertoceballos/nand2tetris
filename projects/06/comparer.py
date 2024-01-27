import sys

filename = sys.argv[1]

filename2 = sys.argv[2]

with open(filename,"r") as f:
    with open(filename2,"r") as f2:
        while True:
            d1 = f.readline()

            if len(d1) == 0:
                break

            d2 = f2.readline()

            if d1 != d2:
                print("different")