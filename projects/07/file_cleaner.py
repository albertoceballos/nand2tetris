import sys

# get cmd args
n = len(sys.argv)

if n < 0:
    raise Exception("Missing arguments. pass filename.asm as argument")

if n > 2:
    raise Exception("Too many arguments")

# get filename
filename = sys.argv[1]

filename2 = f"{filename[0:len(filename)-4]}.cleaned_asm"

with open(filename,"r") as f:
    for data in f:
        if data[0] == "/":
            continue

        if len(data) == 1:
            continue

        with open(filename2,"a+") as f2:
            f2.write(data)