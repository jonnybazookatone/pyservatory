
import string
import math
# import numarray
import _skysub
from types import *  # names of types for input handling ... 

# from Tkinter import *

def todeci(instuff) :
	# This code converts string input into decimal
	try: z = float(instuff)
	except ValueError:
		# allow for space- or colon-separated triplets
		instuff = string.replace(instuff,":"," ")
		x = string.split(instuff)
#		print x, len(x)
#		if len(x) == 2 :
		#	print "ERROR: %s not a valid coord, need three fields. " % instuff
		if(string.find(x[0],"-") < 0) :
			sign = 1
		else : sign = -1
		try :
			z = abs(float(x[0]))
			fac = 60. 
			for y in x[1:3] :
				z = z + float(y) / fac
				fac = fac * 60
			z = sign * z
		except ValueError :
			print "Illegal format for time or angle input."
			z = None
	
	return z

class coord :
	"""Stores, converts, prints a coordinate as decimal or triplet."""
	def __init__(self,instuff) :
		if type(instuff) == StringType :
			self.val = todeci(instuff)
		elif type(instuff) == FloatType :
			self.val = instuff
	def printit(self) :
		print self.val
	def set(self,instuff) :
		self.val = todeci(instuff)
	def tripletstring(self, delin = " ", places = 2, showsign = 1) :

	# returns a triplet string representation of a time or angle,
	# OR if places < 0 rounds to the nearest tenth of a minute or
	# nearest minute.  
		
		if(self.val < 0.) :
			sign = -1
			tempval = self.val * -1.
			c = '-'
		else : 
			sign = 1
			tempval = self.val
			if(showsign == 1) : c = '+'
			else : c = ' '
		h = int(tempval)
		frac = tempval - h
		mm = 60. * frac
		if places >= 0 :
			m = int(mm)
			ss = 60. * (mm - m)
	
			stry = round(ss,places)
			if(stry > 59.9999999999) :
				stry = 0.
				m = m + 1
				if(m == 60) :
					m = 0
					h = h + 1
	
			ss = stry
	
			if(places > 0) :
				formatstr = "%c%d%c%02d%c%0" + \
				  str(places+3) + "." + str(places) + "f"
			if(places == 0) :  # nearest second
				formatstr = "%c%d%c%02d%c%02.0f"
			return formatstr % (c,h,delin,m,delin,ss)
		elif places == -1 :  # tenths of a minute
			if mm >= 59.95 :
				h = h + 1
				mm = 0.
			formatstr = "%c%d%c%04.1f" 
			return formatstr % (c,h,delin,mm)
		else :  # nearest minute
			if mm >= 59.5 :
				h = h + 1
				mm = 0.
			formatstr = "%c%d%c%02.0f"
			return formatstr % (c,h,delin,mm)

	
	def tripletprint(self, delin = " ", places = 2, showsign = 1) :
		if(self.val < 0.) :
			sign = -1
			tempval = self.val * -1.
		else : 
			sign = 1
			tempval = self.val
		h = int(tempval)
		frac = tempval - h
		mm = 60. * frac
		m = int(mm)
		ss = 60. * (mm - m)

		stry = round(ss,places)
		if(stry > 59.9999999999) :
			stry = 0.
			m = m + 1
			if(m == 60) :
				m = 0
				h = h + 1

		ss = stry

		if(places > 0) :
			formatstr = "%c%d%c%02d%c%0" + str(places+3) + "." + \
				str(places) + "f"
		if(places == 0) :
			formatstr = "%c%d%c%02d%c%02.0f"

		if sign == -1 :
			c = '-'
		else:
		    if(showsign == 1) : c = '+'
		    else : c = ' '
		print formatstr % (c,h,delin,m,delin,ss),

	def round(x, places) :
		
		tempval = self.val
		base = 10 ** places
		tempval = tempval * base
		if(tempval > 0) :
			tempval = tempval + 0.5
		else : 
			tempval = tempval - 0.5
		ip = int(tempval)
		return float(ip) / base
	
class ra(coord) :

	def __init__(self, instuff) :
		coord.__init__(self, instuff)
		while(self.val < 0.) :
			self.val = self.val + 24.
		while(self.val >= 24.) :
			self.val = self.val - 24.
	def putra(self, raplaces=3, radelin = " ") :
		return coord.tripletprint(self,delin=radelin,places = raplaces,showsign=0)
		return s
	def radian(self) :
		return(self.val /  3.819718634205)
	def degree(self) :
		return(self.val * 15.)

class ha(coord) :

	def __init__(self, instuff) :
		coord.__init__(self, instuff)
		while(self.val < -12.) :
			self.val = self.val + 24.
		while(self.val >= 12.) :
			self.val = self.val - 24.
	def putha(self, haplaces=0,hadelin = " ") :
		return coord.tripletprint(self,delin=hadelin,places=haplaces,showsign=1)
	def radian(self) :
		return(self.val /  3.819718634205)


class dec(coord) :

	def __init__(self, instuff) :
		coord.__init__(self, instuff)
	def putdec(self, decplaces=2, decdelin=" ") :
		return coord.tripletprint(self,delin=decdelin,places=decplaces,showsign=1)
	def radian(self) :
		return(self.val /  57.2957795130823)

class celest :
	
	def __init__(self,instuff) :
		if type(instuff) == ListType : 
			self.ra = ra(instuff[0])  # need these
			self.dec = dec(instuff[1])
			try :
				self.equinox = float(instuff[2])
			except :
				self.equinox = 2000. # this can default.
		elif type(instuff) == StringType :
			x = string.split(instuff) 
			if len(x) > 5 :   # hr min sec deg min sec
				inra =  x[0] + " " + x[1] + " " + x[2]
				indec = x[3] + " " + x[4] + " " + x[5]
				try :
					self.equinox = float(x[6])
				except :
					self.equinox = 2000.
			else :
				inra = x[0]
				indec = x[1]
				try :
					self.equinox = float(x[2])
				except :
					self.equinox = 2000.
			self.ra = ra(inra)
			self.dec = dec(indec)
		else :
			print "Couldn't parse celest input."
			

	def quickpr(self) :

		self.ra.putra()
		print "  ",
		self.dec.putdec()
		print "  ",
		print "%7.2f" % self.equinox

	def summarystring(self,radigits = 2, delin = ":",include_eq = 1) :
		outstr = self.ra.tripletstring(places = radigits, 
			showsign = 0, delin = delin)
		outstr = outstr + "  " + \
			self.dec.tripletstring(places = radigits - 1,
			   showsign = 1, delin = delin)
		if include_eq == 1 :
			outstr = outstr + "  %6.1f" % self.equinox
		return outstr
	
	def longpr(self,prec = 2, delin=" ") :
		
		print "RA =",
		self.ra.putra(prec+1,delin)
		print ", dec =",
		self.dec.putdec(prec,delin)
		print ", equinox ",
		print "%7.2f" % self.equinox

	def aslist(self) :
		return [self.ra.val,self.dec.val,self.equinox]
	
	def xyz(self) :
	
		x = math.cos(self.ra.radian()) * math.cos(self.dec.radian())
		y = math.sin(self.ra.radian()) * math.cos(self.dec.radian())
		z = math.sin(self.dec.radian())
		return x,y,z

	def precess(self,newequinox) :
		# returns a new position ....
		x = _skysub.cooxform(self.ra.val,self.dec.val, 
			self.equinox,float(newequinox),1,0,1)	
		return celest([x[0],x[1],newequinox])

	def selfprecess(self,newequinox) :
		# precesses in place ....
		# print "Doin stuff ... "
		x = _skysub.cooxform(self.ra.val,self.dec.val, 
			self.equinox,float(newequinox),1,0,1)	
		# print x
		self.ra.val = x[0]
		self.dec.val = x[1]
		self.equinox = float(newequinox)

	def galact(self) :
		return _skysub.galact(self.ra.val,self.dec.val,self.equinox)

	def eclipt(self) :
		return _skysub.eclipt(self.ra.val,self.dec.val,self.equinox,
			self.jd)
	
	def constel(self) :
		con = "   "  # empty 3-char string
		_skysub.radec_to_constel(self.ra.val,self.dec.val,self.equinox,
			con)
		return con

class Longit(coord) :  # I believe this class is unused, so I provide a 
			# standalone longitude converter below.
	
	def __init__(self,longitin) :
		if type(longitin) == FloatType :
			self.val = longitin      # In this case it must be decimal hours.
		elif type(longitin) == StringType :
			if string.find(longitin,'d') >= 0 :
				longitnew = string.replace(longitin,"d","")
				input_deg = 1
		 	elif string.find(longitin,'D') >= 0  :
				longitnew = string.replace(longitin,"D","")
				input_deg = 1		
			else :
				longitnew = longitin
				input_deg = 0
			self.val = todeci(longitnew)
			if input_deg == 1 :
				self.val = self.val / 15.
			

def getradec(instuff,input_units = "h") :
	
	if type(instuff) == FloatType :   # floating point must be decimal hrs
		return instuff
	elif type(instuff) == StringType :  # parse this ...
		instuff = string.upper(instuff)
		instuff = string.replace(instuff,":"," ")  # de-colonize ... 
		x = string.split(instuff)
		if len(x) == 1 :
			try :
				return float(x[0])
			except :
				print "Unconvertible input in getra."
				return None
		units = input_units 
		if string.find(x[-1],"D") == 0:
			units = "d"
			x = x[:-1]
		elif string.find(x[-1],"H") == 0:
			units = "h"
			x = x[:-1]
		if string.find(x[0],"-") > -1 :
			sign = -1
		else :
			sign = 1
		
		try :
			value = float(x[0]) * sign   # make positive explicitly
			fac = 60.
			for xx in x[1:3] :
				value = value + float(xx) / fac
				fac = fac * 60.
			value = value * sign
			if units == input_units :
			       return value
			elif units == "d" and input_units == "h" :
			 	return value / 15.
			else :
				return value * 15.
	
		except :
			print "Can't parse RA or dec input!"
			return None
	
def getlongit(instuff) :
	
	if type(instuff) == FloatType :   # floating point must be decimal hrs, W.
		return instuff
	elif type(instuff) == StringType :  # parse this ...
		instuff = string.upper(instuff)
		instuff = string.replace(instuff,":"," ")  # de-colonize ... 
		x = string.split(instuff)
		if len(x) == 1 :
			try :
				return float(x[0])
			except :
				print "Unconvertible input in getlongit."
				return None
		dir = 'w'
		if string.find(x[-1],"E") == 0 :
			dir = 'e' 
			x = x[:-1]  # throw away last part after parsing 
		elif string.find(x[-1],"W") == 0 :
			dir = 'w'
			x = x[:-1]
		units = "h"
		if string.find(x[-1],"D") == 0:
			units = "d"
			x = x[:-1]
		elif string.find(x[-1],"H") == 0:
			units = "h"
			x = x[:-1]
		if string.find(x[0],"-") > -1 :
			sign = -1
		else :
			sign = 1
		
		try :
			value = float(x[0]) * sign   # make positive explicitly
			fac = 60.
			for xx in x[1:3] :
				value = value + float(xx) / fac
				fac = fac * 60.
			value = value * sign
			if units == "d" : value = value / 15.   # in hours
			if dir == "e" : value = value * -1.     # positive west 
			return value
	
		except :
			print "Can't parse longitude input!"
			return None
		
		
class site :

	# A variety of initiators are allowed.
	# - a list passing in the parameters 
	# - a name of an observatory
	
	def __init__(self, instuff) :

		# dictionary of observatories.  The site params are
		# (0) longitude, decimal hours west; (2) latitude, 
 		# decimal degrees north; (3) standard time zone, 
		# offset, hours west; (4) daylight savings time option 
		# (integer); (5) elevation in meters; (6) elevation
		# above the local horizon; (7) site name; (8) local
		# time zone name; (9) 1-character abbrev. for local
		# time (not yet used).

		# If you ADD to this dictionary, be sure to choose a new
		# key letter which does not conflict with one already used.
		# (Either that or erase the conflcting choice from the list).
		# Also, DO NOT USE the letter 'x', it is a special code
		# used elsewhere.  The letters are hidden from the user
		# in the GUI, so your choice need not be mnemonic. 
	
		self.obsdir = {'k':[7.44111,31.9533,7.,0,1925,700,\
		"Kitt Peak [MDM Obs.]","Mountain",'M'],\
	         'd':[4.81907,43.705,5.,1,183,0,"Shattuck Observatory", \
	        "Eastern",'E'], \
		 's':[-1.38744,-32.3783,-2.,0,1771.,0.,"SAAO, Sutherland", \
		"SAST",'S'], \
		 'g':[7.32611,32.7017,7.,0,3181,1500,"Mount Graham, Arizona",
		"Mountain","M"],
	         'e':[4.7153,-29.257,4.,-1,2347.,2347., \
	  	 "ESO, Cerro La Silla", "Chilean", 'C'], \
	         'v':[4.69356,-24.625,4.,-1,2635.,2635., \
	         "VLT, Cerro Paranal","Chilean",'C'], \
	  	 'p':[7.79089,33.35667,8.,1.,1706.,1706., \
	  	 "Palomar Observatory","Pacific",'P'], \
	  	't':[4.721,-30.165,4.,-1,2215.,2215., \
	  	"Cerro Tololo","Chilean",'C'], \
	  	'c':[4.71333,-29.00833,4.,-1,2282.,2282., \
	  	 "Las Campanas Obs.","Chilean","C"],\
	  	'h':[7.39233,31.6883,7.,0,2608.,500.,\
	  	"Mount Hopkins, Arizona","Mountain",'M'],\
	          'o':[6.93478,30.6717,6.,1,2075,1000,\
	  	"McDonald Observatory","Central","C"],\
	  	'a':[-9.937739,-31.277039,-10.,-2,1149.,670.,\
	           "Anglo-Australian Tel.","Australian",'A'],\
	  	'b':[8.22778,48.52,8.,1,74.,74., \
	  	 "DAO, Victoria, BC","Pacific","P"], \
	        'm': [10.36478, 19.8267, 10., 0, 4215., 4215., \
	        "Mauna Kea, Hawaii","Hawaiian",'H'], \
	  	'l':[8.10911,37.3433,8.,1,1290.,1290.,\
	  	"Lick Observatory","Pacific",'P'],\
	  	'r':[1.192,28.75833,0.,2,2326.,2326.,\
	           "Roque de los Muchachos","pseudo-Greenwich",'G']}
	
		# set up a default 
		self.longit = 7.4411
		self.lat = 31.9533
		self.stdz = 7
		self.use_dst = 0
		self.obs_name = "Kitt Peak"
		self.zone_name = "Mountain"
		self.zone_abbrev = "M"
		self.elevsea = 1925
		self.elevhoriz = 700.
		if type(instuff) == ListType :
		   try :
		   	# put this in a try so you don't have to 
			# quote every parameter ... 
			self.longit = instuff[0]
			self.lat = instuff[1]
			self.stdz = instuff[2]
			self.use_dst = instuff[3]
			self.elevsea = instuff[4]
			self.elevhoriz = instuff[5]
			self.obs_name = instuff[6]
			self.zone_name = instuff[7]
			self.zone_abbrev = instuff[8]
		   except :
			pass
		elif type(instuff) == StringType :
		   try :
			# if it's on the list ...
			[self.longit,self.lat,self.stdz,self.use_dst,self.elevsea,
			  self.elevhoriz,self.obs_name,self.zone_name,self.zone_abbrev] = \
				self.obsdir[instuff]
		   except :
			try :
				x = string.split(instuff)
				self.longit = instuff[0]
				self.lat = instuff[1]
				self.stdz = instuff[2]
				self.use_dst = instuff[3]
				self.elevsea = instuff[4]
				self.elevhoriz = instuff[5]
				self.obs_name = instuff[6]
				self.zone_name = instuff[7]
				self.zone_abbrev = instuff[8]
			except :
				# I give up!
				pass
	

def getmonth(monthstring) :
   
    months = ['xxx','jan','feb','mar','apr','may','jun','jul','aug', \
	             'sep','oct','nov','dec']
    monthstring = string.lower(monthstring)
    mo = 0
    for m in months :
       if string.find(monthstring,m) > -1 :
          mo = months.index(m)
    return mo

def monthstring(number, abbrev = 1) :
    month_abbrev = ['xxx','Jan','Feb','Mar','Apr','May','Jun','Jul', \
	'Aug','Sep','Oct','Nov','Dec']
    month_full = ['xxx','January','February','March','April','May', \
	'June','July','August','September','October','November','December']
    if abbrev == 1 :
	try : 
	   mstr = month_abbrev[number]
	   return(mstr)
        except :
	   return "Illegal month number = %d" % number
    else :
	try :
	   mstr = month_full[number]
	   retrun(mstr)
	except :
	   return "Illegal month number = %d" % number

def daystring(dow, abbrev = 1) :
   days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
   days_abbrev = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
   if abbrev == 1 :
	try :
	   daystr = days_abbrev[dow]
	except :
	   daystr = "Illegal day of week = %d" % dow
   else :
	try :
	   daystr = days[dow]
	except :
	   daystr = "Illegal day of week = %d" % dow
   return daystr
 
def time_to_jd(instuff = "NOW",stdz = 0.,use_dst = 0) :
	
	v = _skysub.new_date_time()

	if type(instuff) == ListType or type(instuff) == TupleType :
		yr = float(instuff[0])
		if yr < 1901 or yr > 2099 :
			print "Outside calendrical range, no action."
			_skysub.delete_date_time(v)
			return -1.
		try :
		   mo = float(instuff[1])
		except ValueError :
		   mo = getmonth(instuff[1])
                   if mo == 0 :
                              printx('Illegal month name!!')
		dd = float(instuff[2])

		hh = 0.  # in case they aren't passed in 
		mm = 0.
		ss = 0.
			
		if len(instuff) > 3 :
		   try :
		      if string.find(instuff[3],":") > -1 : # colon-ized
		         temptup = string.split(instuff[3],":")
                         instuff[3] = temptup[0]
		         instuff = instuff + [temptup[1]]
		      if len(temptup) > 2 :
                                    instuff = instuff + [temptup[2]]
		      hh = float(instuff[3])
		   except :
		      hh= float(instuff[3])
		if len(instuff) > 4 :	
		   mm = float(instuff[4])
		if len(instuff) > 5 :
		   ss = float(instuff[5])

		_skysub.date_time_y_set(v,int(yr))
		_skysub.date_time_mo_set(v,int(mo))
		_skysub.date_time_d_set(v,int(dd))
		_skysub.date_time_h_set(v,int(hh))
		_skysub.date_time_mn_set(v,int(mm))
		_skysub.date_time_s_set(v,ss)

	elif type(instuff) == StringType :  # it's a string ...
        #        print "instuff ",instuff,"type and StrTy",type(instuff),StringType
		if string.find(instuff,"NOW") > -1 :
			_skysub.get_sys_date(v,0,0,0,0,0)
		else :	
			# de-colonize
			instuff = string.replace(instuff,":"," ")
			instuff = string.replace(instuff,","," ")
			# time given as y m d h m s
			x = string.split(instuff)
			# allow low-order fields to be omitted .. 
				# fill in here
			while len(x) < 6 :
				x = x + [0.]
			# wacky interface to struct date_time in 
					# skysub

			try :
				mo = float(x[1])
			except ValueError :
				mo = getmonth(x[1])

			y = float(x[0])
			if y < 1901 or y > 2099 :
				print "Outside calendrical limits."
				_skysub.delete_date_time(v)
				return -1.
			_skysub.date_time_y_set(v,int(y))
			_skysub.date_time_mo_set(v,int(mo))
			_skysub.date_time_d_set(v,int(x[2]))
			_skysub.date_time_h_set(v,int(x[3]))
			_skysub.date_time_mn_set(v,int(x[4]))
			_skysub.date_time_s_set(v,float(x[5]))

	elif type(instuff) == FloatType :	
	# it better be just a JD by itself ... 
		z = float(instuff)
		if z > 1.0e6 :  # it's a JD
			if z > 2415388. and z < 2488069 :
				jdin = z
			else :
				print "JD out of valid range."
				_skysub.delete_date_time(v)
				return -1.
		elif z < 5000. :  # it's a year
			jdin = _skysub.J2000 + \
				365.25 * (z - 2000.) 
		dow = _skysub.caldat(jdin,v)

	else :
		print "ERROR: Can't initialize 'instant' from given info."

	# v is now loaded with the date derived from input jd ... 
	# Now that input info is parsed, let's set the REAL jd:
	
	jd = _skysub.true_jd(v,use_dst,0,0,stdz)
	_skysub.delete_date_time(v)
	
	return(jd)
	
def jd2cal(jdin, stdz = 0.,use_dst = 0,jd_override = 0.) :

	# jd_override is basically a switch not to use jdin for 
 	# the calculation -- if it's > 100000, it overrides jdin

	if jd_override > 1000000. :
		jdin = jd_override

	# need to find year to get jd's of beginning and end of dst
	v = _skysub.new_date_time()
	jdwork = jdin - stdz / 24.  # local jd, without dst
	dow = _skysub.caldat(jdwork,v)
	y = _skysub.date_time_y_get(v)   # again without dst

	# There's a possible problem about daylight savings time around
	# the turn of the year ... 

	if use_dst != 0 :
		#print "jdwork ",jdwork,"year y", y
		#sys.exit()  # needed to catch a runaway in true_jd.
		
		[jdb,jde] = _skysub.find_dst_bounds(y,stdz,use_dst)
		# print "year",y,"jdb",jdb,"jde",jde
		# print "jdin, jdwork  = ",jdin,jdwork
		# jdb, jde are real jds, so compare to real input jd.	
		offset = _skysub.zone(use_dst,stdz,jdin,jdb,jde) / 24.
		# print "offset ",offset
	else :
		offset = stdz / 24.

	jdwork = jdin - offset
	dow = _skysub.caldat(jdwork,v)
	y = _skysub.date_time_y_get(v)
	mo = _skysub.date_time_mo_get(v)
	d = _skysub.date_time_d_get(v)
	h = _skysub.date_time_h_get(v)
	mn = _skysub.date_time_mn_get(v)
	s = _skysub.date_time_s_get(v)
	_skysub.delete_date_time(v)
	return [y,mo,d,h,mn,s,dow,stdz,use_dst,offset]

def julian_ep(jdin) : 
	ep = 2000. + (jdin - _skysub.J2000) / 365.25
	return ep

class instant :

	# One instant of time, stored internally as a JD.
	# Includes knowledge of standard time zone and 
	# daylight savings, which default to zero in initialization
	# (i.e., UT input). 

	# There's a wide variety of input formats:
	#    - jd by itself
	#    - decimal year  (distinguished from JD by reasonableness)
	#    - a string of "yyyy mo dd hh mm ss" in which 'mo' can 
	#       optionally be a string including a 3-letter abbreviation
	#    - a list or tuple of [yyyy,mo,dd,hh,mm,ss]  or
	#                         [yyyy,mo,dd,"hh:mm:ss"] -- in either 
	#                          of these the month can be an abbrev.
	#    - one special string, "NOW".

	def __init__(self,instuff = "NOW",stdz = 0.,use_dst = 0) :
		test = time_to_jd(instuff, stdz, use_dst)
		if test > 0. : self.jd = test
		else :self.jd = _skysub.J2000

	def print_all(self, stdz = 0., use_dst = 0) :
		print "UT date and time: ",
		_skysub.print_all(self.jd)

	def incrtime(self, increment = 1.) :
		# increments time by increment (in minutes)
		self.jd = self.jd + increment / 1440.
	
	def caldat(self,stdz = 0.,use_dst = 0,jd_override = 0.) :
		return jd2cal(self.jd, stdz, use_dst, jd_override)

	def calstring(self, stdz = 0., use_dst = 0, style = 0, secdigits = 0, 
	   timedelim = " ", print_day = 0, daycomma = 1, dayabbrev = 0, jd_override = 0.) :

		outstring = ""

		[y,mo,d,h,mn,s,dow,stdz,use_dst,offset] = self.caldat(stdz = stdz,use_dst=use_dst,jd_override=jd_override)
#		print "caldat output in calstring",\
#		   y,mo,d,h,mn,s,dow,stdz,use_dst,offset

		if secdigits > 3 : secdigits = 3  # further digits insignificant (JD)	
		if secdigits <= 0 : totalsecdigits = 2
		else : totalsecdigits = secdigits + 3
		secformat = "%" + "0%d.%df" % (totalsecdigits,secdigits)
		# print "secformat = ", secformat

		# The following code corrects the problem of seconds rounding to 60,
		# in such a manner that the date follows along if second is rounded
		# up to midnight.

		secteststring = secformat % s
		sectestfloat = float(secteststring)
		# print "sectest string and float:",secteststring,sectestfloat
		if sectestfloat > 59.9999 :  # we have a 60 in the seconds place ...
			addamount = 0.49 * 10 ** (-1. * secdigits)
			# print "adding ",addamount," seconds .. "
			if jd_override < 0.01 :
				jdtemp = self.jd + addamount / 86400.
			else : jdtemp = jd_override + addamount / 86400.
			[y,mo,d,h,mn,s,dow,stdz,use_dst,offset] = self.caldat(stdz=stdz,
				use_dst = use_dst,jd_override = jdtemp)

		if style == 0 :
		   outstring = outstring +  "%4.0f %02.0f %02.0f  %2.0f%s%02.0f%s" % \
			(y,mo,d,h,timedelim,mn,timedelim) + secformat % s
		if style == 1 :
		   outstring = outstring + "%4.0f %s %02.0f  %2.0f%s%02.0f%s" % \
			(y,monthstring(mo),d,h,timedelim,mn,timedelim) + secformat % s
		if print_day != 0 and style != 2 :
		   if daycomma == 1 :
		      outstring = outstring + ", " + daystring(dow,abbrev = dayabbrev)
		   else :
		      outstring = outstring + "  " + daystring(dow,abbrev = dayabbrev)

		if style == 2 :   # "Fri Jan. 07 13:43"
			if(s > 30.) :  # round up
				mn = mn + 1.
				if mn > 59 :  # uh-oh
					h = h + 1		
					mn = 0
					if h > 23 :  # double uh-oh
						# add 1/2 minute + a bit
						if jd_override < 0.01 :
							jdtemp = self.jd + 0.00034723
						else :
							jdtemp = jd_override + 0.00034723
						[y,mo,d,h,mn,s,dow,stdz,use_dst,offset] = \
						  self.caldat(stdz,use_dst,jd_override = jdtemp)
		
			outstring = daystring(dow, abbrev = 1) + " %s %02.0f %2.0f:%02.0f" % \
					(monthstring(mo),d,h,mn)
		if style == 3 :   #  "2005 Apr 12"
			if(s > 30.) :  # round up
				mn = mn + 1.
				if mn > 59 :  # uh-oh
					h = h + 1		
					if h > 23 :  # double uh-oh
						# add 1/2 minute + a bit
						if jd_override < 0.01 :
							jdtemp = self.jd + 0.00034723
						else :
							jdtemp = jd_override + 0.00034723
						[y,mo,d,h,mn,s,dow,stdz,use_dst,offset] = \
						  self.caldat(stdz,use_dst,jd_override = jdtemp)
		
			outstring = "%04d %s %02.0f" % \
					(y,monthstring(mo),d)


		return outstring

	def day_of_year(self,stdz = 0.,use_dst = 0) :

		# returns floating-point time since "Jan 0" at 0h.
		# JD should be a true UT jd given how it's initialized,
		# providing stdz and use_dst adjusts day_of_year to local.

		x = self.caldat(stdz,use_dst)
		v = _skysub.new_date_time()
		_skysub.date_time_y_set(v,float(x[0]))
		_skysub.date_time_mo_set(v,1)
		_skysub.date_time_d_set(v,1)
		_skysub.date_time_h_set(v,0)
		_skysub.date_time_mn_set(v,0)
		_skysub.date_time_s_set(v,0)
		jdjan1 = _skysub.date_to_jd(v)
		_skysub.delete_date_time(v)

		return self.jd - jdjan1 + 1.   # anything on Jan 1 is 1.xxx 

	def julian_epoch(self) : 
		ep = 2000. + (self.jd - _skysub.J2000) / 365.25
		return ep

	def moonphasedescr(self) :
		nlast = int((self.jd - 2415020.5)/ 29.5307 - 1)
		lastnewjd = _skysub.flmoon(nlast,0)
		nlast = nlast + 1
		newjd = _skysub.flmoon(nlast,0)
		kount = 0
		while newjd < self.jd and kount < 40 :
			lastnewjd = newjd
			nlast = nlast + 1
			newjd = _skysub.flmoon(nlast,0)
		if kount > 35 :
			print "Didn't find phase in moonphasedescr!"
			return "error"
		else :
			x = self.jd - lastnewjd
			nlast = nlast - 1
			noctiles = int(x / 3.69134)  # octile of the month
			if noctiles == 0 :
				return "%3.1f d since new moon" % x
			elif noctiles <= 2 :
				fqjd = _skysub.flmoon(nlast,1)
				x = self.jd - fqjd
				if x < 0. :
					return "%3.1f d before 1st quarter" % (-1 * x)
				else :
					return "%3.1f d after 1st quarter" % x
			elif noctiles <= 4 :
				fljd = _skysub.flmoon(nlast,2)
				x = self.jd - fljd 
				if x < 0. :
					return "%3.1f d before full moon" % (-1 * x)
				else :
					return "%3.1f d after full moon" % x
			elif noctiles <= 6 :
				lqjd = _skysub.flmoon(nlast,3)
				x = self.jd - lqjd
				if x < 0. :
					return "%3.1f d before last quarter" % (-1 * x)
				else :
					return "%3.1f d after last quarter" % x
			else : return "%3.1f d before new moon" % (newjd - self.jd)
	
# Dropping planetmags, it calls numarray -- want to keep this simpler
#
#def planetmags(jd) :
#
## **** NOTE NOTE NOTE **** comp_el(jd) must be called before this
## routine.
#
## returns the magnitudes of the planets in a list;
## [merc,venus,earth,mars,jupiter,saturn]
## Does position calculations in ecliptic, since only
## relative positions matter.  Somewhat approximate.
#
#   earthxyz = numarray.array(_skysub.planetxyz(3,jd))
##   print "earthxyz:",earthxyz
#
##   V0 = [None,-0.42,-4.40,-3.86,-1.52,-9.40,-9.22,-7.19,-6.87,-1.0]
#  # From Astronomical Almanac, 2003, p. E88.  V mag of planet when
#   # full face on at unit distance from both sun and earth.  Saturn
#   # has been goosed up a bit b/c Almanac quantity didn't have rings
#   # in it ... 
#
#   mags = [None]  # leave a blank at zeroth index
#
#   for i in range(1,7) :
#      if i != 3 :   # skip the earth
#         xyz = numarray.array(_skysub.planetxyz(i,jd))
#         xyzmodulus = math.sqrt(dot(xyz,xyz))
#         pl2earth = earthxyz - xyz
#         pl2earthmodulus = math.sqrt(dot(pl2earth,pl2earth))
#         xyznegnorm = -1. * xyz / xyzmodulus
#         pl2earthnorm = pl2earth / pl2earthmodulus
#         phasefac =  0.5 * (dot(xyznegnorm,pl2earthnorm) + 1.)
#         # we want the cosine of the phase ultimately, and the dot gives it...
#         # actually, 1/2 of cosine phase plus one.  This is simply the
#         # illuminated fraction, nothing more elaborate.
#         mag = V0[i] + 2.5*math.log10(phasefac) + 5*math.log10(xyzmodulus*pl2earthmodulus)
#         mags = mags + [mag]
#      else :
#         mags = mags + [None]   # not doing earth.    
#     
#   return mags 

def py_get_planets(jd,longit,lat,doprint) :
   # hides the ugliness needed to run pposns from python.

   raptr = _skysub.new_doubleArray(10)
   decptr = _skysub.new_doubleArray(10)
   sidt = _skysub.lst(jd,longit)
   _skysub.pposns(jd,lat,sidt,doprint,raptr,decptr)
   planetpos = [[None]]
   for i in range(1,10) :  
      if i != 3 :
         pos = [_skysub.doubleArray_getitem(raptr,i), \
		_skysub.doubleArray_getitem(decptr,i)]
         planetpos = planetpos + [pos]
      else :
         planetpos = planetpos + [None]
   _skysub.delete_doubleArray(raptr)
   _skysub.delete_doubleArray(decptr)
   return planetpos

def computeplanets(jd,longit,lat,doprint) :

   label = [None,'Mercury','Venus',None,'Mars','Jupiter','Saturn',
	'Uranus','Neptune','Pluto']
   _skysub.comp_el(jd)
   if doprint == 1 :
      print "Planets for ",
      _skysub.print_all(jd)
      print "UT.",
#   mags = planetmags(jd) 
   planetpos = py_get_planets(jd,longit,lat,doprint) 
   planets = [None]  # blank for position zero
   for i in range(1,10) :
      if i != 3 :
         planets = planets + [[label[i],planetpos[i][0],planetpos[i][1]]]
			# ,mags[i]]]  # dropping the magnitudes.
      else :
         planets = planets + [None]
   return planets

def opposite_angle(inangle) :
	
	o = inangle + 180.
	while o > 180. :
		o = o - 360.
	while o < -180. :
		o = o + 360.
	return o

def subtendang(ra1, dec1, ra2, dec2) :
 # simple wrapper for _skysub.subtend.  To hide dependence on skysub
 # from pyskycal.

	return _skysub.subtend(ra1,dec1,ra2,dec2)
 
class observation(site,instant,celest) :

	def __init__(self,siteinput = 'k',celestinput = "ZENITH",
		instantinput = "NOW") :
		
		site.__init__(self,siteinput)
		instant.__init__(self,instantinput,self.stdz,self.use_dst)
		if celestinput == "ZENITH" :
			sidt = _skysub.lst(self.jd,self.longit)
			self.ra = ra(sidt)
			self.dec = dec(self.lat)
			self.equinox = instant.julian_epoch(self)
		else :
			celest.__init__(self,celestinput)

	def setcelest(self,celestinput = [0.,0.,2000]) :
		if celestinput == "ZENITH" :
			sidt = _skysub.lst(self.jd,self.longit)
			self.ra = ra(sidt)
			self.dec = dec(self.lat)
			self.equinox = instant.julian_epoch(self)
		else :
			celest.__init__(self,celestinput)

	def setut(self,instantinput = "NOW",stdz = 0., use_dst = 0) :
		# sets the JD using UT input
		test = time_to_jd(instantinput, stdz = 0, use_dst = 0)
		if test > 0. : self.jd = test
	def setlocal(self,instantinput = "NOW") :
		# sets the JD using local input, accounting for 
		# time zone and DST
		test = time_to_jd(instantinput,stdz=self.stdz,
				use_dst = self.use_dst)
		if test > 0. : self.jd = test

	def setsite(self,siteinput = 'k') :
		site.__init__(self,siteinput)

	def computesky(self) :
		# computes many quantities so they're self-consistent
		sidtemp = _skysub.lst(self.jd,self.longit)
		self.sidereal = ra(sidtemp) # it behaves like an RA
		self.decimalyr = self.julian_epoch()
		self.CoordsOfDate = self.precess(self.julian_epoch())
		self.hanow = ha(self.sidereal.val - self.CoordsOfDate.ra.val)
		[self.altit,self.az,self.parang] = \
		   _skysub.altit(self.CoordsOfDate.dec.val,self.hanow.val, \
			self.lat)
		self.secz = _skysub.secant_z(self.altit)
		self.airmass = _skysub.true_airmass(self.secz)

	def computesunmoon(self) :
		[ras,decs,dists,toporas,topodecs,xs,ys,zs] = \
			_skysub.accusun(self.jd, self.sidereal.val,self.lat) 
		self.SunCoords = celest([ras,decs,self.julian_epoch()])
		self.hasun = ha(self.sidereal.val - self.SunCoords.ra.val)
		[self.altsun,self.azsun,parangsun] = \
			_skysub.altit(self.SunCoords.dec.val,self.hasun.val,\
				self.lat)
		self.ztwilight = _skysub.ztwilight(self.altsun)

		[georam,geodm,geodism,toporam,topodecm,topodistm] = \
			_skysub.accumoon(self.jd,self.lat,self.sidereal.val,
			   self.elevsea)
		self.MoonCoords = celest([toporam,topodecm,self.julian_epoch()])
		self.hamoon = ha(self.sidereal.val - self.MoonCoords.ra.val)
		[self.altmoon,self.azmoon,parangmoon] = \
			_skysub.altit(self.MoonCoords.dec.val,self.hamoon.val,\
				self.lat)
		self.sun_moon = _skysub.subtend(self.MoonCoords.ra.val,  
			self.MoonCoords.dec.val,self.SunCoords.ra.val,
			self.SunCoords.dec.val) # radians
		self.moonillfrac = 0.5 * (1. - math.cos(self.sun_moon))
		self.sun_moon = self.sun_moon * _skysub.DEG_IN_RADIAN
		self.obj_moon = _skysub.subtend(self.MoonCoords.ra.val,
			self.MoonCoords.dec.val,self.CoordsOfDate.ra.val,
			self.CoordsOfDate.dec.val) * _skysub.DEG_IN_RADIAN
		self.lunsky = _skysub.lunskybright(self.sun_moon,
			self.obj_moon,0.17,self.altmoon,self.altit,topodistm)
		[self.barytcor, self.baryvcor] = _skysub.helcor(self.jd,self.CoordsOfDate.ra.val,
		   self.CoordsOfDate.dec.val,self.hanow.val,self.lat,self.elevsea)
		self.baryjd = self.jd + self.barytcor / _skysub.SEC_IN_DAY

		# find the jd at the nearest clock-time midnight ... 
		localtimestr = self.calstring(stdz = self.stdz, use_dst = self.use_dst)
		x = string.split(localtimestr)
		ymd = x[0] + " " + x[1] + " " + x[2]
		if float(x[3]) >= 12. :
			midnstring = ymd + " 23 59 59.99"
		else :
			midnstring = ymd + " 0 0 0 "
		self.jdmid = time_to_jd(midnstring, stdz = self.stdz, \
			use_dst = self.use_dst)
		self.stmid = ra( _skysub.lst(self.jdmid,self.longit))

		# elevation correction (in degrees) for horizon depression
		horiz = math.sqrt(2. * self.elevhoriz / _skysub.EQUAT_RAD) \
			 * _skysub.DEG_IN_RADIAN
		setelev = -1. * (0.83 + horiz)

		hasunset = _skysub.ha_alt(self.SunCoords.dec.val,self.lat,setelev)
	
		if hasunset > 900.  : 
			self.jdsunset = 1000.  # never sets
			self.jdsunrise = 1000.
			self.jdcent = 1000.
		elif hasunset < -900.  : 
			self.jdsunset = -1000.  # never rises
			self.jdsunrise = -1000.
			self.jdcent = -1000.
		else :
		    self.jdsunset = self.jdmid + _skysub.adj_time(self.SunCoords.ra.val \
			+ hasunset - self.stmid.val)/24.  # initial guess
		    # print "entering jdsunset - self.jdsunset = ",self.jdsunset,
		    self.jdsunset = _skysub.jd_sun_alt(setelev,self.jdsunset,self.lat, \
			self.longit)
		    self.jdsunrise = self.jdmid + _skysub.adj_time(self.SunCoords.ra.val \
			- hasunset - self.stmid.val)/24.  # initial guess
		    self.jdsunrise = _skysub.jd_sun_alt(setelev,self.jdsunrise,self.lat, \
			self.longit)

		    self.jdcent = (self.jdsunset + self.jdsunrise) / 2.

		hatwilight = _skysub.ha_alt(self.SunCoords.dec.val, self.lat, -18.)

		if hatwilight > 900. : 
			self.jdevetwi = 1000.   # never gets dark
			self.jdmorntwi = 1000. 
		elif hatwilight < -900. :  
			self.jdevetwi = -1000.  # never gets light
			self.jdmorntwi = -1000.  
		
		else :
		    self.jdevetwi = self.jdmid + _skysub.adj_time(self.SunCoords.ra.val \
			+ hatwilight - self.stmid.val)/24.  # initial guess
		    self.jdevetwi = _skysub.jd_sun_alt(-18.,self.jdevetwi,self.lat, \
			self.longit)
		    self.jdmorntwi = self.jdmid + _skysub.adj_time(self.SunCoords.ra.val \
			- hatwilight - self.stmid.val)/24.  # initial guess
		    self.jdmorntwi = _skysub.jd_sun_alt(-18.,self.jdmorntwi,self.lat, \
			self.longit)

		[ramoonmid,decmoonmid,distmoonmid] = \
		   _skysub.lpmoon(self.jdmid,self.lat,self.sidereal.val)
		[minmoonalt,maxmoonalt] = _skysub.min_max_alt(self.lat,decmoonmid)
		# rough (close enough) check to see if moonrise or moonset occur ... 
		if maxmoonalt < setelev :
			self.jdmoonrise = -100.  # never rises
			# -1000. is used later to signal non-convergence
			self.jdmoonset = -100.
		if minmoonalt > setelev :
			self.jdmoonrise = 100. # never sets
			self.jdmoonset = 100.
		else :
		    hamoonset = _skysub.ha_alt(decmoonmid,self.lat,setelev)
		    tmoonrise = _skysub.adj_time(ramoonmid - hamoonset - self.stmid.val)
		    tmoonset = _skysub.adj_time(ramoonmid + hamoonset - self.stmid.val)
		    self.jdmoonrise = self.jdmid + tmoonrise / 24.
		    self.jdmoonrise = _skysub.jd_moon_alt(setelev,self.jdmoonrise, \
			self.lat,self.longit,self.elevsea)
		    self.jdmoonset = self.jdmid + tmoonset / 24.
		    self.jdmoonset = _skysub.jd_moon_alt(setelev,self.jdmoonset,self.lat, \
			self.longit,self.elevsea)

		[self.par_dra,self.par_ddec,self.aber_dra,self.aber_ddec] = \
			_skysub.parellipse(self.jd,self.ra.val,self.dec.val,self.equinox,
					self.lat,self.longit)
	

	def printstuff(self) :

		self.computesky()
		self.computesunmoon()
	
		print "UT date and time   :",
		print self.calstring(style = 1)
		print "Local date and time:",
		print self.calstring(style = 1, stdz = self.stdz, use_dst = self.use_dst)
		print ""
		print " Input coords : ",
		self.quickpr()
		print "Coords of date: ",
		self.CoordsOfDate.quickpr()
		print " "
		print "sidereal time :",
		self.sidereal.putra(raplaces = 0)
		print " HA: ",
		self.hanow.putha()
		print ""
		print "altitude %5.2f azimuth %6.2f, parallactic %5.1f" % \
			(self.altit,self.az,self.parang)
		print "airmass %6.3f" % self.airmass
		print " "
		print "Sun  : ",
		self.SunCoords.quickpr()
		print "Sun alititude and az : %5.2f %5.2f  " % (self.altsun,
			self.azsun)
		if self.altsun >= -18. and self.altsun < 0. :
			print "Zenith twilight %4.1f mag" % \
				(self.ztwilight)
		else :
			print " "
		print "Moon : ",
		self.MoonCoords.quickpr()
		print "Moon alititude and az: %5.2f %5.2f  " % (self.altmoon,
			self.azmoon)
		_skysub.print_phase(self.jd)
		print "; illuminated frac %4.3f " % self.moonillfrac
		if(self.altmoon > -2.) :
			print "Object is %5.1f degr from moon." % self.obj_moon,
			print "; Lunar sky brightness %5.1f mag." % self.lunsky
		print " "
		print "Barycentric corrections:  %5.1f sec, %5.2f km/s." % (self.barytcor,
			self.baryvcor)
		print "Barycentric Julian Date:  %13.5f" % self.baryjd

	def printplanets(self) :
		self.planets = computeplanets(self.jd,self.longit,self.lat,1) 

