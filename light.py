#!/usr/bin/env python3
import rospy
from time import sleep
from std_msgs.msg import Float64, Bool
from blobs_msgs.msg import BlobArray
from geometry_msgs.msg import Twist
pub_vel = rospy.Publisher('vel', Twist, queue_size=1)

def Error(msg):
	


if __name__ == '__main__':
	rospy.loginfo('Test')
	rospy.init_node('line_control')
	rospy.Subscriber('/new_blobs', BlobArray, Error, queue_size=1)
	while not rospy.is_shutdown():
		try:
			rospy.sleep(0.1)
		except KeyboardInterrupt:
			break
