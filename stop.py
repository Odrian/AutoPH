#!/usr/bin/env python3
import rospy
from time import sleep
from std_msgs.msg import Float64, Bool
from geometry_msgs.msg import Twist
pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)
def cbError(error):
	velocity = Twist()
	velocity.angular.z = 0.0
	velocity.linear.x = 0.0
	pub_vel.publish(velocity)

if __name__ == '__main__':
	rospy.init_node('line_control')
	sub_image = rospy.Subscriber('/error_lane', Float64, cbError, queue_size=1)
	while not rospy.is_shutdown():
		try:
			rospy.sleep(0.1)
		except KeyboardInterrupt:
			break
