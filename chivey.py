#!/usr/bin/python

############################
#
# Created by BostonGeorge
# August 7, 2013
# Within Chaos...There is Profit
#
############################

import urllib2
import os
import datetime

# Some variables. Im sure there is a better way, but deal with it or change it yourself.
pic = 1
_path = []
currentDir = os.getcwd()
error = 0
year = datetime.datetime.now().strftime("%Y")
month = datetime.datetime.now().strftime("%M")
_time = 6
MAX_ERROR = 10
MIN_MONTH = 01
pathCount = 0

# The main categories. There are extras that are limited to one, not continual $
category=['fit-girls-','sexy-bikinis-','burn-bra-','chesty-girls-flbp-','mirror-girls-','hump-day-','girls-lingerie-','russian-brides-','mind-the-gap-','redheaded-chivettes-','tan-lines-','sexy-chivers-']

# Display a menu for the user
def menu():
    print 'Select a category to copy:'
    print
    print '[0] Fit Girls    	  [6] Girls lingerie' 	
    print '[1] Sexy Bikinis	  [7] Russian Brides'
    print '[2] Burn Bra		  [8] Mind the Gap'
    print '[3] Chesty Girls	  [9] Redheads'
    print '[4] Mirror Girls	  [10] Tan Lines'
    print '[5] Hump Day		  [11] Sexy Chivers'
    print
    print '[12] Custom'
    print
    selection = int(raw_input('Selection: '))
    print
    
    if selection == 12:
        print 'Format: sexy-bikinis-'
        print 'Make sure you include the dashes!!'
        print 'Hint: click the picture you want until only the picture is showing'
        print 'Look at the url...it should be /sexy-bikinis-01'
        print
        customSelection = raw_input('Custom: ')
	print
        category.append(customSelection)

    return selection

# Get user input
year = int(raw_input("[+] Enter starting year: "))
month = int(raw_input("[+] Enter starting month: "))
_time = int(raw_input("[+] How many months back should I scrape? "))

# Get current Time
timenow = "chivey-" + datetime.datetime.now().strftime("%H-%M-%S")

# Make backups for writing files the easy way
monthbak = month
yearbak = year
_timebak = _time

# Add the first YYYYMM to the list
_path.append(str(year) + str('%02d' % month))

# Add the additional YYYMM to the list
if _time > 1:
    while _time != 0:
        if month == 1:
            month=13
            year-=1
        month-=1
        _path.append(str(year) + str('%02d' % month))
        _time-=1

# Display the menu
selection = menu()

# Create main folder name chivey-HH-MM-SS
if not os.path.exists(timenow):
    os.makedirs(timenow)

os.chdir(str(currentDir) + "/" + str(timenow) + "/")
# Create folders for the pics
for yr in _path:
    if not os.path.exists(yr): 
        os.makedirs(yr)

# Get the pics
while _time >= 0:        
    
    #URL String and file dir.
    url=str("http://thechive.files.wordpress.com/" + str(yearbak) + "/" + str('%02d' % monthbak + "/" + category[selection] + str(pic) + ".jpg"))
    fileName=str(category[selection] + str(pic) + ".jpg")
    os.chdir(str(currentDir) + "/" + str(timenow) + "/" + str(yearbak) + str('%02d' % monthbak))

    # Try for a 202, and count the 404s so we can go to the next batch of pictures
    try:
        u = urllib2.urlopen(url)
    except urllib2.URLError, e:
        if e.code == 404:
	    print "No file detected at URL: " + str(pic)
            error+=1
            pic+=1
    else:
    	# Save the file if it is a 202
        f = open(fileName, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (fileName, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()
        print "W00tW00t!! Another photo you say!! That makes " + str(pic) + "!"
        error=0
        pic+=1
    
    # Iterate through the files and do it all over again.
    if error == MAX_ERROR:
        _timebak-=1
        if monthbak == MIN_MONTH:
            monthbak=13
            yearbak-=1
        monthbak-=1
        error=0
        pic=1
        pathCount+=1
