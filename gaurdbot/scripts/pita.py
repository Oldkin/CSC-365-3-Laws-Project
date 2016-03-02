#!/usr/bin/env python
'''Base code provided by I Heart Robotics, modified by Peter Tran, and additional modifications  by Sam Caldwell and
Shannon Ehrnstein. It now includes a face detector using ROS_people, and object tracking through Rollin Tschirgi's code. The code 
also attempts to speak using pyttsx and warn any intruders of their intrusion.
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import math
from kobuki_msgs.msg import BumperEvent, CliffEvent
import pyttsx
# Every Python Controller needs these lines
# import roslib; roslib.load_manifest('project1')

talker = pyttsx.init()
message = "I am patrolling"

class Scan_msg:



	talker.say(message)
	#talker.say(self.speech)
	#talker.say(self.call_msg)
	

	def __init__(self):
	#'''Initializes an object of this class.
	#The constructor creates a publisher, a twist message.
	#3 integer variables are created to keep track of where obstacles exist.
	#3 dictionaries are to keep track of the movement and log messages.'''

		self.pub = rospy.Publisher('mobile_base/commands/velocity',Twist, queue_size=2)
		self.msg = Twist()
		self.sect_1 = 0
		self.sect_2 = 0
		self.sect_3 = 0
		self.ang = {0:0,001:-1.2,10:-1.2,11:-1.2,100:1.5,101:1.0,110:1.0,111:1.2}
		self.fwd = {0:.05,1:0,10:0,11:0,100:0.1,101:0,110:0,111:0}
		self.dbgmsg = {0:'Move forward',1:'Veer right',10:'Veer right',11:'Veer right',100:'Veer left',101:'Veer 	left',110:'Veer left',111:'Veer right'}
		self.msgs = message
		talker.say(self.msgs)
		#talker.say(self.pub)
		
	def reset_sect(self):

		'''Resets the below variables before each new scan message is read'''
		self.sect_1 = 0
		self.sect_2 = 0
		self.sect_3 = 0
		self.call_msg = "patrolling"
		talker.say(self.msgs)
		

	def sort(self, laserscan):
		'''Goes through 'ranges' array in laserscan message and determines
		where obstacles are located. The class variables sect_1, sect_2,
		and sect_3 are updated as either '0' (no obstacles within 0.7 m)
		or '1' (obstacles within 0.7 m)
		Parameter laserscan is a laserscan message.'''

		#no_nans = [n for n in data.ranges if not math.isnan(n)]
		entries = len(laserscan.ranges)
		talker.say(self.msgs)
		for entry in range(0,entries):
			if 0.4 < laserscan.ranges[entry] < 0.75:
				
				self.sect_1 = 1 if (0 < entry < entries/3) else 0
				self.sect_2 = 1 if (entries/3 < entry < entries/2) else 0
				self.sect_3 = 1 if (entries/2 < entry < entries) else 0
		rospy.loginfo("sort complete,sect_1: " + str(self.sect_1) + " sect_2: " + str(self.sect_2) + " sect_3: " 	+ str(self.sect_3))
		
	
			

	def movement(self, sect1, sect2, sect3):

		'''Uses the information known about the obstacles to move robot.
		Parameters are class variables and are used to assign a value to
		variable sect and then set the appropriate angular and linear
		velocities, and log messages.
		These are published and the sect variables are reset.'''
		sect = int(str(self.sect_1) + str(self.sect_2) + str(self.sect_3))
		rospy.loginfo("Sect = " + str(sect))
		talker.say(self.msgs)
		self.msg.angular.z = self.ang[sect]
		self.msg.linear.x = self.fwd[sect]
		rospy.loginfo(self.dbgmsg[sect])
		self.pub.publish(self.msg)
		self.reset_sect()
		talker.say("pat")

	def bumper_event_callback(self, msg):
		"""Checks to see if the bumper has been pressed, if so the robot will then
		back up and turn in a random direction."""

		k = 0
		if msg.state == BumperEvent.PRESSED:	
			for k in range(0, 4999):
				self.msg.angular.z = 0
				self.msg.linear.x = -0.1
				self.pub.publish(self.msg)
				k = k + 1
				k = 0
				crosscounter = randint(5000,50000)
				orientation = randint(-1,1)
			for orientation in range (0, 0):
				orientation = randint(-1,1)

			for k in range(0, crosscounter):
				self.msg.angular.z = orientation
				self.msg.linear.x = 0
				self.pub.publish(self.msg)
				self.pub.publish(self.msgs)
				k = k + 1
		
		talker.say(self.msgs)

	def for_callback(self,laserscan):
		'''Passes laserscan onto function sort which gives the sect
		variables the proper values. Then the movement function is run
		with the class sect variables as parameters.
		Parameter laserscan is received from callback function.'''

		self.sort(laserscan)
		self.movement(self.sect_1, self.sect_2, self.sect_3)
		talker.say(self.msgs)
		

def call_back(scanmsg):
	'''Passes laser scan message to for_callback function of sub_obj.
	Parameter scanmsg is laserscan message.'''
	sub_obj.for_callback(scanmsg)
	#talker.say(self.msgs)

def call_msg(scanmsg):
	'''Passes laser scan message to for_callback function of sub_obj.
	Parameter scanmsg is laserscan message.'''
	new_obj.for_callback(scanmsg)
	#talker.say(self.msgs)

def listener():
	'''Initializes node, creates subscriber, and states callback
	function.'''
	rospy.init_node('navigation_sensors')
	rospy.loginfo("Subscriber Starting")
	sub = rospy.Subscriber('/scan', LaserScan, call_back)
	#talker.say(self.msgs)
	rospy.spin()

def listener2():
	'''Initializes node, creates subscriber, and states callback
	function.'''
	rospy.init_node('people_tracker_measurements')
	rospy.loginfo("Subscriber Starting")
	sub2 = rospy.Subscriber('/people_tracker_measurements', face_detector/people_tracker_measurements, call_msg)
	message = "person detected"
	#talker.say(self.msgs)
	rospy.spin()

if __name__ == "__main__":
	'''A Scan_msg class object called sub_obj is created and listener
	function is run'''

	sub_obj = Scan_msg()
	talker.runAndWait()
	listener()	
	listener2()
	message = "person detected"
	talker.say(message)
	#rospy.spin()
