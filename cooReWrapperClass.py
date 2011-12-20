#!/usr/bin/python
"""
COOCLASS RE-WRAPPER
-------------------

This is another class for using JT's skycalc program for calculating ephemeries and other useful information. It follows Abdullah's rewrite of the same class which can be found in the library ~/gp/....(libs).../grond/server/visibility.py. Unfortunately I did not find it so readable and so have re-written it in a more object oriented-easy-to-read (hopefully) approach.

Classes:

	CelestialObject
		Properties:
		Functions:
"""

import calendar
import time
import sys
import numpy
import datetime
import matplotlib.pyplot as plt

import cooclasses as coo

__author__ = "Jonny Elliott"
__copyright__ = "Copyright 2011"
__credits__ =  ""
__license__ = "GPL"
__version__ = "0.0"
__maintainer__ = "Jonny Elliott"
__email__ = "jonnyelliott@mpe.mpg.de"
__status__ = "Prototype"




class CelestialObject(coo.observation):
  
	# Initialisation
	def __init__(self):
	  
		self._RA = None
		self._DEC = None
		self._EQUINOX = None
		self._siteabbrev = 'v'
		self._OBJECTWRAPPER = coo.observation()
		self._SunRiseStart = None
		self._SunSetEnd = None
		self._EveningTwilightEnd = None
		self._MorningTwilightStart = None
		self._Name = None
		self._NightLength = None
		self._Figures = 0
		self._TriggerTime = None
 
	# Properties of the class in a C++ manor to try to keep tidy
	#
	# Print
	#
	def printInfo(self):
		print "Celestial Object"
		print "----------------"
		print "Name: %s" % self.getName()
		print "RA: %s" % self.getRADEC()[0]
		print "DEC: %s" % self.getRADEC()[1]
		print "EQUINOX: %s" % self.getRADEC()[2]
		print "TRIGGERTIME: %s JD" % self.getTriggerTime()
		print "\t\t", (self.jd2skycalcstruct(self.getTriggerTime()))
		print ""
		print "Location Information"
		print "--------------------"
		
		temp = self.getSunSetEnd()
		print "Sunset:\t\t\t %s-%s-%s\t%s:%s:%d UT" % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
		
		temp = self.getEveningTwilightEnd()
		print "EveningTwilight:\t %s-%s-%s\t%s:%s:%d UT" % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]) 
		
		temp = self.getMorningTwilightStart()
		print "MorningTwilight:\t %s-%s-%s\t%s:%s:%d UT" % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
		
		temp = self.getSunRiseStart()
		print "Sunrise:\t\t %s-%s-%s\t%s:%s:%d UT" % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])
		
		temp = str(datetime.timedelta(seconds=self.getNightLength())).split(":")
		print "NightLength (Nautical): %s hours %s minutes %s seconds" % (temp[0], temp[1], temp[2])
		
		temp = str(datetime.timedelta(seconds=self.getANightLength())).split(":")
		print "NightLength (Astronomical): %s hours %s minutes %s seconds" % (temp[0], temp[1], temp[2])

	#
	# Set
	#
	def setTRIGGER(self, TriggerTime):
		self._TriggerTime = TriggerTime
	
	def setNightLength(self, NightLength):
		self._NightLength = NightLength

	def setANightLength(self, ANightLength):
		self._ANightLength = ANightLength

	def setSunRiseStart(self, SunRiseStart):
		self._SunRiseStart = SunRiseStart
		
	def setSunSetEnd(self, SunSetEnd):
		self._SunSetEnd = SunSetEnd
		
	def setEveningTwilightEnd(self, EveningTwilightEnd):
		self._EveningTwilightEnd = EveningTwilightEnd

	def setMorningTwilightStart(self, MorningTwilightStart):
		self._MorningTwilightStart = MorningTwilightStart
	
	def setRADEC(self, RA, DEC, EQUINOX="J2000"):
		# This object
		self._RA = RA
		self._DEC = DEC
		self._EQUINOX = EQUINOX
		
		# Wrapper for coo.observation
		self._OBJECTWRAPPER.setcelest([RA, DEC, EQUINOX])
	  
	def setSITEABBREV(self, siteabbrev):
		self._siteabbrev = siteabbrev
		
	def setName(self, Name):
		self._Name = Name
	# 
	# Get
	#
	def getTriggerTime(self):
		return self._TriggerTime
	
	def getFigure(self):
		tmp = self._Figures
		self._Figures += 1
		return tmp

	def getANightLength(self):
		return self._ANightLength
		
	def getNightLength(self):
		return self._NightLength

	def getName(self):
		return self._Name
	
	def getRADEC(self):
		return self._RA, self._DEC, self._EQUINOX

	def getMorningTwilightStart(self):
		return self._MorningTwilightStart
	
	def getEveningTwilightEnd(self):
		return self._EveningTwilightEnd
	
	def getSunRiseStart(self):
		return self._SunRiseStart
	
	def getSunSetEnd(self):
		return self._SunSetEnd
	  
	def getSITEABBREV(self):
		return self._siteabbrev

	#
	# General Functions
	#
	def jd2skycalcstruct(self, jd):
		calendardate = coo.observation().caldat(jd_override=jd)
		timestruct = time.struct_time(calendardate[0:9])
		skycalcstruct = timestruct[0:6]
		
		return skycalcstruct
	#
	# Object Functions
	#
	def setObservatory(self, siteabbrev='v', celestialinput='ZENITH', instantinput='NOW'):
	  
		# set values
		self.setSITEABBREV(siteabbrev)
	  
		# Call the coo function, for now I do not implement celestial input etc as it is default
		self._OBJECTWRAPPER.setsite(self.getSITEABBREV())
	
	
	def computeTwilights(self, intime="NOW"):
	
		# Set the times
		if intime == "NOW":
			ut = time.gmtime(time.time())[:6]
			self._OBJECTWRAPPER.setut(ut)
		else:
			# IMPORTANT - PLEASE CHECK THE FORMAT OF THE TIME INPUT FOR THIS CALL
			ut = time.gmtime(intime)[:6]
			self._OBJECTWRAPPER.setut(ut)
		
		# Calculates twilight tims etc (.jdsunset, .jdevetwi, ....)
		self._OBJECTWRAPPER.computesky()
		self._OBJECTWRAPPER.computesunmoon()
		
		# Collate the important times
		self.setSunSetEnd(self._OBJECTWRAPPER.caldat(jd_override=self._OBJECTWRAPPER.jdsunset))
		self.setEveningTwilightEnd(self._OBJECTWRAPPER.caldat(jd_override=self._OBJECTWRAPPER.jdevetwi))
		self.setMorningTwilightStart(self._OBJECTWRAPPER.caldat(jd_override=self._OBJECTWRAPPER.jdmorntwi))
		self.setSunRiseStart(self._OBJECTWRAPPER.caldat(jd_override=self._OBJECTWRAPPER.jdsunrise))
		
		#sunri = datetime.datetime(int(sunrise[0]),int(sunrise[1]),int(sunrise[2]),int(sunrise[3]),int(sunrise[4]),int(sunrise[5]))
		#sunse = datetime.datetime(int(sunset[0]),int(sunset[1]),int(sunset[2]),int(sunset[3]),int(sunset[4]),int(sunset[5]))
		
	def computeNightLength(self, intime="NOW"):
	  		# Set the times
		if intime == "NOW":
			ut = time.gmtime(time.time())[:6]
			self._OBJECTWRAPPER.setut(ut)
		else:
			# IMPORTANT - PLEASE CHECK THE FORMAT OF THE TIME INPUT FOR THIS CALL
			ut = time.gmtime(intime)[:6]
			self._OBJECTWRAPPER.setut(ut)
			
		# Too many formats!!!!!
		sunrise = self.getSunRiseStart()
		sunset = self.getSunSetEnd()
		
		evetwi = self.getEveningTwilightEnd()
		morntw = self.getMorningTwilightStart()
		
		sunri = datetime.datetime(int(sunrise[0]),int(sunrise[1]),int(sunrise[2]),int(sunrise[3]),int(sunrise[4]),int(sunrise[5]))
		sunse = datetime.datetime(int(sunset[0]),int(sunset[1]),int(sunset[2]),int(sunset[3]),int(sunset[4]),int(sunset[5]))
		
		evetwi = datetime.datetime(int(evetwi[0]),int(evetwi[1]),int(evetwi[2]),int(evetwi[3]),int(evetwi[4]),int(evetwi[5]))
		morntw = datetime.datetime(int(morntw[0]),int(morntw[1]),int(morntw[2]),int(morntw[3]),int(morntw[4]),int(morntw[5]))
		
		# Nautical Night Length
		nightdt = (sunri-sunse)
		nightlen = nightdt.seconds + nightdt.days*60*60*24
		
		# Astronomical Night Length
		anightdt = (morntw-evetwi)
		anightlen = anightdt.seconds + anightdt.days*60*60*24
		
		# Haven't decided on how to do object oriented functions, to embed or return
		self.setNightLength(nightlen)
		self.setANightLength(anightlen)
		return nightlen, anightlen
		
	def computeNightAltitude(self, intime="NOW"):
	  
		if intime != "NOW":
			ut = time.gmtime(intime)[:6]
			self._OBJECTWRAPPER.setut(ut)
		
		# Loop over the entire night length
		#	i.e. SunRise -> SunSet with resolution of minutes
		#
		resolution_s = 1. #seconds
		resolution_m = 60. # minutes
		resolution_h = 3600. # hours
		resolution_d = 24*resolution_h # days
		
		timeIntervalArray = numpy.arange(0, self.getANightLength(), resolution_m)
		
		observableArray = numpy.array([])
		observableTimeArray = numpy.array([])
		
		notObservableArray = numpy.array([])
		notObservableTimeArray = numpy.array([])
		
		fullAltitude = numpy.array([])
		
		time0 = self._OBJECTWRAPPER.jdsunset
		
		# Loop through
		for i in range(len(timeIntervalArray)):
			
			TimeInterval = time0 + timeIntervalArray[i]/resolution_d
			formatTimeInterval = self.jd2skycalcstruct(jd=TimeInterval)
			
			self._OBJECTWRAPPER.setut(formatTimeInterval)
			self._OBJECTWRAPPER.computesky()
			
			# Telescope pointing limit
			ALT = self._OBJECTWRAPPER.altit

			# Full array list for later analysis
			fullAltitude = numpy.append(fullAltitude, ALT)
			
			if ALT >= 20:
				observableArray = numpy.append(observableArray, ALT)
				observableTimeArray = numpy.append(observableTimeArray, TimeInterval)
			else:
				notObservableArray = numpy.append(notObservableArray, ALT)
				notObservableTimeArray = numpy.append(notObservableTimeArray, TimeInterval)
				
				
				
		timeIntervalArray = numpy.array([(i/resolution_d + time0) for i in timeIntervalArray])
	
		return observableArray, observableTimeArray, notObservableArray, notObservableTimeArray, fullAltitude, timeIntervalArray

	def plotNightAltitude(self, intime="NOW"):

		obs1, time1, obs2, time2, trash1, trash2 = self.computeNightAltitude(intime=intime)
		fig = plt.figure(self.getFigure())
		ax = fig.add_subplot(111)
		ax.plot(time1, obs1, color='blue')
		ax.plot(time2, obs2, color='red')
		ax.set_ylabel("Altitude")
		ax.set_xlabel("Time")
		plt.draw()
		#plt.savefig("obs.png", format="png")

	def computeNightVisibility(self, intime="NOW", telescopelimit=20, triggerdelay=(4/24.), triggertime=23400):
	  
		# Sort the altitude arrays into visibility periods
		#
		observableArray, observableTimeArray, \
		notObservableArray, notObservableTimeArray, \
		fullAltitude, timeIntervalArray \
		                                                = self.computeNightAltitude(intime=intime)
		# Flag list
		#
		# observableFlag - TRUE if it is observable start, FALSE if it goes below
		# afterTrigger - TRUE if it is < 4 hours after the burst, FALSE for > 4 hours
		
		arrLen = len(fullAltitude)
		observableFlag, afterTrigger, appendFlag = False, False, False
		# Temp arrays
		fullVisibilityArray = []
		altitudeArray = numpy.array([])
		hourtimeArray = numpy.array([])

		for i in range(arrLen):
 
			Altitude = fullAltitude[i]
			Hourtime = timeIntervalArray[i]
			
			# Telescope pointing, i.e. alt > 20 deg
			if Altitude >= telescopelimit:
				observableFlag = True
			else:
				observableFlag = False
			
		
			if observableFlag:
				# This means the time is consequential and observable
				altitudeArray = numpy.append(altitudeArray, Altitude)
				hourtimeArray = numpy.append(hourtimeArray, Hourtime)
			else:
				# This means we need a new array
				fullVisibilityArray.append( [ altitudeArray, hourtimeArray ] )
				altitudeArray = numpy.array([])
				hourtimeArray = numpy.array([])
				
		# Incase the observable flag is never hit
		fullVisibilityArray.append( [ altitudeArray, hourtimeArray ] )


		return fullVisibilityArray
		
	def plotNightVisibility(self, intime="NOW", telescopelimit=20, triggerdelay=(4/24.), triggertime=23400):
	  
		"""Plots the output of computeNightVisibility onto matplotlib"""
		
		# Load the arrays from the function
		fullVisibilityArray = self.computeNightVisibility(intime=intime, telescopelimit=telescopelimit, \
								  triggerdelay=triggerdelay, triggertime=triggertime \
								 )
           
		fig = plt.figure(self.getFigure())
		ax = fig.add_subplot(111)
		# Plot to output using matplotlib
		for i in range(len(fullVisibilityArray)):
			
			tmp = fullVisibilityArray[i]
			
			alt = fullVisibilityArray[i][0]
			tim = fullVisibilityArray[i][1]
			
			ax.plot(tim, alt)
			ax.set_xlabel("time")
			ax.set_ylabel("altitude")
		
		plt.draw()

def main():


	RA = "23:18:11.57"
	DEC = "32:28:31.8"
	EQUINOX = "J2000"
	# Format for my script = ?!? skycat!!!
	#TRIGGER = 

	# Example usage
	# Set the observatory information and calc twilights
	GRB = CelestialObject()
	GRB.setObservatory(siteabbrev='e')
	GRB.computeTwilights()
	GRB.computeNightLength()
	GRB.setRADEC(RA=RA, DEC=DEC, EQUINOX=EQUINOX)
	#GRB.setTRIGGER(TRIGGER)
	#GRB.plotNightAltitude()
	#GRB._Figures = GRB._Figures - 1
	#GRB.plotNightVisibility()
	
	
	# Check if the GRB is observable
	fullVisibilityArray = GRB.computeNightVisibility(telescopelimit=20, triggerdelay=(4/24.), triggertime=GRB._OBJECTWRAPPER.jdsunset+10)
	
	if len(fullVisibilityArray) == 0:
		print "####################"
		print "INFO: NOT OBSERVABLE"
		print "####################"
	#plt.show()
	#GRB.printInfo()

if __name__ == "__main__":
	main()
# Mon Dec 19 11:46:31 CET 2011
