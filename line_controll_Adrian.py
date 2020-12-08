#!/usr/bin/env python3
import rospy
from time import sleep
from std_msgs.msg import Float64, Bool
from blobs_msgs.msg import BlobArray
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)

move_flag = True
rotate_flag = True
alr_park = False
vis_park = False
parking = False
integral = 0
x = 0
time = 0.0
dist = 0
def cbError(error):
	global integral, move_flag, rotate_flag, parking
	if move_flag and not parking:
		velocity = Twist()
		proportional = 0.0032*error.data
		integral = 0.000005*error.data
		up = proportional + integral
		velocity.angular.z = up
		if rotate_flag:
			velocity.linear.x = 0.15 - 0.1*abs(up)
		pub_vel.publish(velocity)

def visError(msg):
	global move_flag, rotate_flag, alr_park, vis_park, parking, x, y, time
	idd = msg.blobs[0].id
	if not parking:
		if idd == 0 and not move_flag:
			move_flag = True
		elif idd == 1:
			move_flag = False
			vstop = Twist()
			vstop.angular.z = 0.0
			vstop.linear.x = 0.0
			pub_vel.publish(vstop)
		elif idd == 2:
			time = rospy.get_time()
			if y > -0.6 and x > 1.0 and not alr_park and not vis_park:
				vis_park = True
				alr_park = True
		elif idd == 3:
			rospy.loginfo('labirint')

def Addons(msg):
	global x, y
	y = msg.pose.pose.position.y
	x = msg.pose.pose.position.x

def Distance(msg):
	global dist
	dist = msg.ranges[89]

def loop():
	global time, vis_park, rotate_flag, move_flag, parking, dist
	rospy.loginfo(dist)
	if not parking and vis_park:
		if rospy.get_time() - time > 2:
			vis_park = False
			move_flag = False
			v1 = Twist()
			v1.angular.z = 0.0
			v1.linear.x = 0.0
			pub_vel.publish(v1)
			v1.angular.z = 0.4
			pub_vel.publish(v1)
			sleep(3)
			move_flag, rotate_flag = True, False
			sleep(1)
			parking = True
			Parking()

def Parking():
	pass

if __name__ == '__main__':
	rospy.init_node('line_control')
	rospy.Subscriber('/error_lane', Float64, cbError, queue_size=1)
	rospy.Subscriber('/new_blobs', BlobArray, visError, queue_size=1)
	rospy.Subscriber('/odom', Odometry, Addons, queue_size=1)
	rospy.Subscriber('/scan', LaserScan, Distance, queue_size=1)
	while not rospy.is_shutdown():
		try:
			rospy.sleep(0.05)
			loop()
		except KeyboardInterrupt:
			break
