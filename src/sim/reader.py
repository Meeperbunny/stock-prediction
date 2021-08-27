import json, sys

# File to open and read json file into an object

if len(sys.argv) != 2:
    print("----------------------------")
    print("Invalid number of arguments.")
    print("py reader.py <FILE_NAME>")
    exit()

file_name = sys.argv[1]
infile = open(file_name, 'r')
data = json.load(infile)
print(data['h'])