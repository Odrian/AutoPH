#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64, Bool
from geometry_msgs.msg import Twist
pub_vel = rospy.Publisher('cmd_vel', Twist, queue_size=1)
velocity = Twist()
velocity.angular.z = 0
velocity.linear.x = 0
pub_vel.publish(velocity)
