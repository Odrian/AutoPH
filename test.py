#!/usr/bin/env python3
import rospy
from time import sleep
from std_msgs.msg import Float64, Bool
from blobs_msgs.msg import BlobArray
from geometry_msgs.msg import Twist
pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)

move_flag = True
integral = 0
def cbError(error):
	rospy.loginfo(error)

def visError(msg):
	rospy.loginfo(msg.blobs)

if __name__ == '__main__':
	rospy.init_node('line_control')
#	rospy.Subscriber('/error_lane', Float64, cbError, queue_size=1)
	rospy.Subscriber('/new_blobs', BlobArray, visError, queue_size=1)
	while not rospy.is_shutdown():
		try:
			rospy.sleep(0.1)
		except KeyboardInterrupt:
			break
