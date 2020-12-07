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
	global integral, move_flag
	if(move_flag == True):
		velocity = Twist()
		proportional = 0.004*error.data
		integral = 0.000005*error.data
		up = proportional + integral
		velocity.angular.z = up
		velocity.linear.x = 0.15 - 0.1*abs(up)
		pub_vel.publish(velocity)

def visError(msg):
	global move_flag
	id = msg.id
	rospy.loginfo(msg)
	if id == 0 and not move_flag:
		move_flag = True
	elif id == 1 and move_flag:
		move_flag = False
		velocity = Twist()
		velocity.angular.z = 0
		velocity.linear.x = 0
		pub_vel.publish(velocity)

if __name__ == '__main__':
	rospy.loginfo('Test')
	rospy.init_node('line_control')
	rospy.Subscriber('/error_lane', Float64, cbError, queue_size=1)
	rospy.Subscriber('/vel', BlobArray, visError, queue_size=1)
	while not rospy.is_shutdown():
		try:
			rospy.sleep(0.1)
		except KeyboardInterrupt:
			break
