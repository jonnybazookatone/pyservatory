#!/usr/bin/python
"""
PYSERVATORY v0.0
----------------
Plot object visibility
Usage:
	python visibility -r RA -d DEC -e EQUINOX"""

import sys
import getopt
import matplotlib.pyplot as plt

from pyservatory.cooReWrapperClass import CelestialObject

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  ""
__license__ = "GPL"
__version__ = "0.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"

def main(RA, DEC, EQUINOX, siteabbrev='e'):

	CO = CelestialObject()
	CO.setObservatory(siteabbrev=siteabbrev)
	CO.setRADEC(RA=RA, DEC=DEC, EQUINOX=EQUINOX)
	CO.computeTwilights()
	CO.computeNightLength()
	CO.plotNightAltitude()
	CO.printInfo()
	plt.show()

if __name__ == "__main__":

        # Key list for input & other constants, stupid final colon
        key_list = 'r:d:e:'

	# check flags
	RA, DEC, EQUINOX = False, False, False

        # Take the input & sort it out
        option, remainder = getopt.getopt(sys.argv[1:], key_list)
        for opt, arg in option:
                flag = opt.replace('-','')
                
                if flag == "r":
                        RA = arg
		elif flag == "d":
			DEC = arg
		elif flag == "e":
			EQUINOX = arg
                else:
                        print __doc__
                        sys.exit(0)

	if RA and DEC and EQUINOX:
		main(RA, DEC, EQUINOX)
	else:
		print __doc__
		sys.exit(0)
# Tue Dec 20 11:18:54 CET 2011
