import finnhub, numpy as np, time, datetime, os, sys, json

if len(sys.argv) != 4:
    print("----------------------------")
    print("Invalid number of arguments.")
    print("py datagen.py <NAME> <INTERVAL> <TIME_RANGE>")
    exit()

# Setup client
api_key_local = os.environ.get('FINN_API_KEY')
finnhub_client = finnhub.Client(api_key=api_key_local)

# Get data
def get_data(target_name, interval, time_range):
    # Parse range
    mindelta, hourdelta, daydelta = 0, 0, 0
    if time_range[0] == 'm':
        mindelta = int(time_range[1:])
    elif time_range[0] == 'h':
        hourdelta = int(time_range[1:])
    elif time_range[0] == 'd':
        daydelta = int(time_range[1:])
    else: 
        print("Invalid range formatting:")
        print("Example: m10 : 10 minutes, h50 : 50 hours, d1 : 1 day")
        exit()

    upperTime = datetime.datetime.now()
    subtractor = datetime.timedelta(minutes=mindelta, hours=hourdelta, days=daydelta)
    lowerTime = upperTime - subtractor
    upperUnix = int(time.mktime(upperTime.timetuple()))
    lowerUnix = int(time.mktime(lowerTime.timetuple()))

    # Stock candles
    return finnhub_client.stock_candles(target_name, interval, lowerUnix, upperUnix)

#Parse command line arguments
target_name = sys.argv[1]
interval = sys.argv[2]
time_range = sys.argv[3]

# Get the data
data = get_data(target_name, interval, time_range)

# Store data in file
script_dir = os.path.join(os.path.dirname(__file__), "../data") # directory of script

# Check if data folder exists, otherwise create it

if not os.path.isdir(script_dir):
    os.mkdir(script_dir)

if data['s'] == None:
    print("No data found.")
    exit()

file_name = target_name + "-" + interval + "-" + time_range + "-" + str(data['t'][-1]) + ".json"
file_dir = os.path.join(script_dir, file_name)

with open(file_dir, 'w') as outfile:
    json_out = json.dumps(data, indent = 4)
    outfile.write(json_out)
    outfile.close()