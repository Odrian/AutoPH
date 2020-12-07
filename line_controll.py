#!/usr/bin/env python3

import rospy
from time import sleep
from std_msgs.msg import Float64, Bool
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

if __name__ == '__main__':
	rospy.init_node('line_control')
	sub_image = rospy.Subscriber('/error_lane', Float64, cbError, queue_size=1)
	while not rospy.is_shutdown():
		try:
			rospy.sleep(0.1)
		except KeyboardInterrupt:
			break
