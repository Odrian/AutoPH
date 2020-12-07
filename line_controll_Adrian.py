#!/usr/bin/env python3
import rospy
from time import sleep
from std_msgs.msg import Float64, Bool
from blobs_msgs.msg import BlobArray
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)

move_flag = True
rotate_flag = True
alr_park = False
integral = 0
x = 0
def cbError(error):
	global integral, move_flag, rotate_flag
	if(move_flag == True):
		velocity = Twist()
		proportional = 0.0032*error.data
		integral = 0.000005*error.data
		up = proportional + integral
		velocity.angular.z = up
		if rotate_flag:
			velocity.linear.x = 0.15 - 0.1*abs(up)
		pub_vel.publish(velocity)

def visError(msg):
	global move_flag, rotate_flag, alr_park , x, y
	idd = msg.blobs[0].id
	if idd == 0 and not move_flag:
		move_flag = True
	elif idd == 1:
		move_flag = False
		velocity = Twist()
		velocity.angular.z = 0
		velocity.linear.x = 0
		pub_vel.publish(velocity)
	elif idd == 2:
		if y > -0.6 and x > 1.0 or not alr_park:
			alr_park = True
			rospy.loginfo(['Fuck'])
			v_stop, v1 = Twist(), Twist()
			v_stop.angular.z = 0.0
			v_stop.linear.x = 0.0
			v1.angular.z = 0.3
			v1.linear.x = 0.0
			sleep(17)
			rospy.loginfo(['stoi debil'])
			move_flag = False
			pub_vel.publish(v1)
			sleep(3)
			pub_vel.publish(v_stop)
			rotate_flag = True
			move_flag = False
			sleep(3)
			rospy.loginfo(['vse'])
	elif idd == 3:
		pass

def Addons(msg):
	global x, y
	y = msg.pose.pose.position.y
	x = msg.pose.pose.position.x

if __name__ == '__main__':
	rospy.init_node('line_control')
	rospy.Subscriber('/error_lane', Float64, cbError, queue_size=1)
	rospy.Subscriber('/new_blobs', BlobArray, visError, queue_size=1)
	rospy.Subscriber('/odom', Odometry, Addons, queue_size=1)
	while not rospy.is_shutdown():
		try:
			rospy.sleep(0.1)
		except KeyboardInterrupt:
			break
