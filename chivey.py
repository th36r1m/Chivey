#!/usr/bin/python

import urllib2
import os

pic = 1
_path = []
currentDir = os.getcwd()
error = 0
year = 2013
month = 7
_time = 6
MAX_ERROR = 10
MIN_MONTH = 01
pathCount = 0

def menu():
    print 'Select a category to copy:'
    print
    print '[0] Fit Girls    [6] Girls lingerie' 	
    print '[1] Sexy Bikinis	  [7] Russian Brides'
    print '[2] Burn Bra		  [8] Mind the Gap'
    print '[3] Chesty Girls	  [9] Redheads'
    print '[4] Mirror Girls	  [10] Tan Lines'
    print '[5] Hump Day		  [11] Sexy Chivers'
    print
    selection = int(raw_input('Selection: '))
    print
    return selection

year = int(raw_input("[+] Enter starting year: "))
month = int(raw_input("[+] Enter starting month: "))
_time = int(raw_input("[+] How many months back should I scrape? "))
monthbak = month
yearbak = year
_timebak = _time

_path.append(str(year) + str('%02d' % month))

if _time > 1:
    while _time != 0:
        if month == 1:
            month=13
            year-=1
        month-=1
        _path.append(str(year) + str('%02d' % month))
        _time-=1

selection = menu()

category=['fit-girls-','sexy-bikinis-','burn-bra-','chesty-girls-flbp-','mirror-girls-','hump-day-','girls-lingerie-','russian-brides-','mind-the-gap-','redheaded-chivettes-','tan-lines-','sexy-chivers-','custom']

for yr in _path:
    if not os.path.exists(yr): os.makedirs(yr)

while _time >= 0:        

    url=str("http://thechive.files.wordpress.com/" + str(yearbak) + "/" + str('%02d' % monthbak + "/" + category[selection] + str(pic) + ".jpg"))
    fileName=str(category[selection] + str(pic) + ".jpg")
    os.chdir(str(currentDir) + "/" + str(yearbak) + str('%02d' % monthbak))

    try:
        u = urllib2.urlopen(url)
    except urllib2.URLError, e:
        if e.code == 404:
	    print "No file detected at URL: " + str(pic)
            error+=1
            pic+=1
    else:
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
    
    if error == MAX_ERROR:
        _timebak-=1
        if monthbak == MIN_MONTH:
            monthbak=13
            yearbak-=1
        monthbak-=1
        error=0
        pic=1
        pathCount+=1
