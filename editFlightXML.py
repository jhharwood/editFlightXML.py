import os, glob, sys, re
from lxml import etree
from xml.etree import cElementTree as ET
from xml.parsers.expat import ExpatError
###>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.XML.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###
def editFlightXML(xml):

    """

    :param xml:
    :return:
    """

    #-------- Parse the XML file: --------#
    try:
        #Parse the given XML file:
        doc = etree.parse(xml)                                                      # use etree from lxml package
    except ExpatError as e:                                                         # use this to proof read xml
        print "[XML] Error (line %d): %d" % (e.lineno, e.code)
        print "[XML] Offset: %d" % (e.offset)
        raise e
    except IOError as e:                                                            # prints the associate error
        print "[XML] I/O Error %d: %s" % (e.errno, e.strerror)
        raise e
    else:
        # Change the GpsToUtcOffset tag value from -15 to 0
        find_gps_ts = doc.find('GpsToUtcOffset')                                    # this ask to find the element tag
        find_gps_ts.set('offsetSec','0')                                            # once found we set the new value

        # now go find the longitutde value using xpath; ahh so nice!!!
        find_long = doc.xpath('//sessions//session//project//flight_plan//line//frame//longitude')
        i = 0;                                                                      # set up an iterator to use a
                                                                                    # loop variable to move down the xml
        for node1 in find_long:
            print "This is the original Longitude: " + find_long[i].text
            reLong = float(find_long[i].text)                                       # changing value from string to float
            #print format(reLong,'.12f')

            # the longitude is from 0 up to 279; we need a neg value ie. from 180 to -180 or Easting/Westing number
            newLong = reLong - 360
            print "This is the calculated new longitude: " + format(newLong, '.12f')
            addNewLong = format(newLong, '.12f')
            find_long[i].text = addNewLong
            print "This is the updated new longitude in the xml: " + find_long[i].text
            find_long[i].set('updated', 'yes')                                      # sets the new value in the xml
            i += 1
            print "Longitude Iteration number: " + str(i)

        print "Wrote new longitude positions to file " + xml + "\n"
        doc.write(xml)

if __name__ == "__main__":
    #-------- Select the XML file: --------#
    #Current file name and directory:
    curpath = os.path.dirname( os.path.realpath(__file__) )                         # gets current path
    filename = os.path.join(curpath, "FlightData.xml")                              # joins the current path with hc file
    #print "Filename: %s" % (filename)
    editFlightXML(filename)                                                         # puts file into function


