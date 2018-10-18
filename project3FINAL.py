def main():

import re
import sys
import operator
import os.path
from urllib.request import urlretrieve
from datetime import datetime

# download the file ansd save just ONE time
URL_PATH = 'https://s3.amazonaws.com/tcmg476/http_access_log'
LOCAL_FILE = 'localcopy.log'
ERRORS = []

# Add counters for future work 
t300_count = 0
t400_count = 0
total_count = 0

# Add storage for direct counts... 
COUNT_REQS_MON = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
STORE_REQS_MON = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []}

# check to see if we can use a cached copy // file succesfuly saved
if not os.path.isfile(LOCAL_FILE):
    print("Downloading file from URL...")
    local_file, headers = urlretrieve(URL_PATH, LOCAL_FILE, lambda x,y,z: print('.', end='', flush=True) if x % 100 == 0 else False)
    print("\nFile retrieved and saved to disk: {}".format(LOCAL_FILE))

# Open file
fh = open(LOCAL_FILE)

#prepare the RegEx //this is how we split code 
regex = re.compile(".*\[([^:]*):(.*) \-[0-9]{4}\] \"([A-Z]+) (.+?)( HTTP.*\"|\") ([2-5]0[0-9]) .*")

# tell the user what's happening. Now we pars 
print("Parsing log file...")

# Loop through each line of the file //this is how we get to loop just once for each line *saves memory and time
for line in fh:
    # split the line into parts 
    parts = regex.split(line)

    # sanity check the parts list
    if not parts or len(parts) < 7:
        #print("Error parsing line! Log entry added to ERRORS[] list...")
        ERRORS.append(line)
        continue

    # total count plus 1
    total_count += 1

    # if statement to find ??
    if parts[6][0] == '3':
        t300_count += 1
    
    if parts[6][0] == '4':
        t400_count += 1
    
    # parse the date into a date object
    r_date = datetime.strptime(parts[1], "%d/%b/%Y")

    # track the counts by month plus one 
    COUNT_REQS_MON[r_date.month] += 1
    STORE_REQS_MON[r_date.month].append(line)


# write out the log files separate into month files, inside this loop we get month digit and value for each month 
print("Writing all log entries into separate files per month...")
for key, val in STORE_REQS_MON.items():
    mon_fname = "{}.log".format(key)
    print("  ...writing {}".format(mon_fname))
    mon_fh = open(mon_fname, 'w')
    mon_fh.writelines(val)
    mon_fh.close()


# Finally we print out the info for the project... 
print("Total requests: {}".format(total_count))
print("40x errors: {}".format(t400_count))
print("30x errors: {}".format(t300_count))
print("Total requests by month: {}".format(COUNT_REQS_MON))
print("# errors seen in log file: {}".format(len(ERRORS)))

main()