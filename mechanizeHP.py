import mechanize
import lxml.html 
import csv
import sys
import os

url = "http://h10025.www1.hp.com/ewfrf/wc/weInput?cc=us&lc=en"

def getWarranty(url, inputItem):
    #Create Browser instance
    b = mechanize.Browser()
    #Disable loading robots.txt (via mechanize)
    b.set_handle_robots(False)
    #Load the Page
    b.open(url)
    #Select form
    b.select_form(name="entitleinput")

    splitItem = inputItem.split(",")
    splitItem[1].rstrip("\n")
    print "... processing: ", splitItem[0] + ", " + splitItem[1],

    #Fill out the form
    b['tmp_weCountry'] = ['us',]
    b['tmp_weSerial'] = splitItem[0] #format 'ABC01234D5'
    b['tmp_weProduct'] = splitItem[1] #format 'AB012CD' 

    #submit
    b.submit()
    #browser response
    response = b.response()
    #save the response as a string
    strResponse = str(response.read())
    #filter w/ lxml, grab our class
    tree = lxml.html.fromstring(strResponse)
    #find matching class <td>
    elements = tree.find_class("bottomSpaceBig")
    #get just the contents of the tags
    warrantyList = [item.text_content() for item in elements]
    #convert to ascii
    warrantyList = [i.encode("ascii", "ignore") for i in warrantyList]
   
    #serial / product not found
    if warrantyList[0].startswith('We were unable to find any results that match'):
        warrantyDict = {1: "No matches found",
                        2: "n/a",
                        3: splitItem[0],
                        4: splitItem[1],
                        5: "n/a"}
                       
    else:
        #remove trailing (YYYY-MM-DD)
        warrantyList[9] = warrantyList[9][:-12]
        #turn our list into a dict (keep keys for future ref?)
        warrantyDict = dict([(k, v) for k,v in zip (warrantyList[::2], warrantyList[1::2])])
    try:
        myfile = open("./output/results.csv", "ab+")
    except IOError as (errno, strerror):
        print "Could not open /output/results.csv: I/O error({0}): {1}".format(errno, strerror)
        print "Exiting ..."
        sys.exit()
    wr = csv.writer(myfile)
    csvOut = []
    for value in dict.values(warrantyDict):
        csvOut.append(value)
    wr.writerow(csvOut)
    myfile.close()

#creates the /output directory
def makeDir():
    try:
        os.makedirs("./output")
        print "... created directory: /output" 
    except OSError as e:
        print "%s: %s" % (e.strerror, e.filename)

#checks if results.csv exists already
def outputCheck():
    exists = os.path.exists(r"./output/results.csv")
    if exists == True:
        pass
    if exists == False:
        makeDir()
        myfile = open("./output/results.csv", "ab+")
        wr = csv.writer(myfile)
        titles = ["Warranty End Date",
                  "Warranty Status",
                  "Serial number",
                  "Product number",
                  "Warranty Category"]
        wr.writerow(titles)

try:
    f = open("hpinput.txt", "r")
    hpList = []
    for i in f:
        hpList.append(i)
except IOError as e:
    print "%s: %s" % (e.strerror, e.filename)
    print "Please ensure hpinput.txt in current directory"
    print "Exiting ..."
    sys.exit()

#main
outputCheck()
for i, val in enumerate(hpList):
    getWarranty(url, hpList[i])

