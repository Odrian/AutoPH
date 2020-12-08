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
flag6 = False
park = 0
integral = 0
x = 0
time = 0.0
dist = 0
rot = 0
err = 0.0
def cbError(error):
	global integral, move_flag, rotate_flag, parking, err
	if move_flag:
		velocity = Twist()
		err = error.data
		proportional = 0.0032*err
		integral = 0.000005*err
		up = proportional + integral
		velocity.angular.z = up
		if rotate_flag:
			velocity.linear.x = 0.15 - 0.1*abs(up)
		else:
			velocity.linear.x = 0.0
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
			if y > -0.6 and x > 1.0 or not alr_park and not vis_park:
				vis_park = True
				alr_park = True
		elif idd == 3:
			if x < -1:
				rospy.loginfo('labirint')

def Addons(msg):
	global x, y
	y = msg.pose.pose.position.y
	x = msg.pose.pose.position.x

def Distance(msg):
	global dist
	dist = msg.ranges
#	rospy.loginfo(dist)

def loop():
	global time, vis_park, move_flag, parking, flag6, dist, park
	if not parking and vis_park:
		if rospy.get_time() - time > 0.1 and not flag6:
			flag6 = True
			rospy.loginfo(dist[0])
			rospy.loginfo(type(dist[0]))
			if str(dist[0]) == 'inf':
				park = 2
			else:
				park = 1
		if rospy.get_time() - time > 2:
			vis_park = False
			move_flag = False
			v1 = Twist()
			v1.linear.x = 0.0
			v1.angular.z = 0.5
			pub_vel.publish(v1)
			sleep(3)
			parking = True
			move_flag = True
			Parking()
	if parking:
		if dist[270] < 0.5:
			rospy.loginfo('FACK')
			move_flag = False
			v2 = Twist()
			v2.linear.x = 0.0
			v2.angular.z = 0.0
			pub_vel.publish(v2)

def Parking():
	global parking, dist, err
	v_stop, v_right, v_left, v_go = Twist(), Twist(), Twist(), Twist()
	v_stop.angular.z = 0.0
	v_stop.linear.x = 0.0
	v_go.angular.z = 0.0
	v_go.linear.x = 0.15
	v_right.angular.z = -0.4
	v_right.linear.x = 0.0
	v_left.angular.z = 0.4
	v_left.linear.x = 0.0
	pub_vel.publish(v_right)
	sleep(abs(err)*0.13)
	pub_vel.publish(v_stop)
#	sleep(1)
#	rospy.loginfo('vse')
#	parking = False

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
