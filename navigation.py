#!/usr/bin/env python

"""

    RoboCup@Home Education | oc@robocupathomeedu.org
    navi.py - enable turtlebot to navigate to predefined waypoint location

"""

import rospy
import time
import sys
import os
import actionlib
from std_msgs.msg import String
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, PoseWithCovarianceStamped, Point, Quaternion, Twist
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient

original = 0
start = 1

class NavToPoint:
    def __init__(self):
        rospy.on_shutdown(self.cleanup)
        
	# Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        rospy.loginfo("Waiting for move_base action server...")
        pub.publish("Waiting for move_base action server...")

        # Wait for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(120))
        rospy.loginfo("Connected to move base server")
        pub.publish("Connected to move base server")

        # A variable to hold the initial pose of the robot to be set by the user in RViz
        initial_pose = PoseWithCovarianceStamped()
        rospy.Subscriber('initialpose', PoseWithCovarianceStamped, self.update_initial_pose)

	# Get the initial pose from the user
        rospy.loginfo("Click the 2D Pose Estimate button in RViz to set the robot's initial pose")
        pub.publish("Click the 2D Pose Estimate button in RViz to set the robot's initial pose")
        rospy.wait_for_message('initialpose', PoseWithCovarianceStamped)
        
        # Make sure we have the initial pose
        while initial_pose.header.stamp == "":
        	rospy.sleep(1)

        goal_pose = String()
        rospy.Subscriber('lm_data', String, self.update_goal_pose)
        while True:
            rospy.loginfo("Waiting for your order...")
            pub.publish("Waiting for your order...")
            rospy.sleep(3)
            rospy.wait_for_message('lm_data', String)

            rospy.loginfo(self.goal_pose.data)
            A_x = 3.02
	    A_y = -1.62
	    A_theta = 1.5708
            A_name = "0"
            if(self.goal_pose.data == "PLEASE NAVIGATE TO POINT ONE" or self.goal_pose.data == "NAVIGATE TO POINT ONE"):
                A_x = 1.8
	        A_y = -5.51
	        A_theta = 1.5708
                A_name = "1"
            elif(self.goal_pose.data == "PLEASE NAVIGATE TO POINT TWO" or self.goal_pose.data == "NAVIGATE TO POINT TWO"):
                A_x = -2.2
	        A_y = -2.53
	        A_theta = 1.5708
                A_name = "2"
            elif(self.goal_pose.data == "PLEASE NAVIGATE TO POINT THREE" or self.goal_pose.data == "NAVIGATE TO POINT THREE"):
                A_x = -7.44
	        A_y = -2.08
	        A_theta = 1.5708
                A_name = "3"
            elif(self.goal_pose.data == "PLEASE NAVIGATE TO POINT FOUR" or self.goal_pose.data == "NAVIGATE TO POINT FOUR"):
                A_x = -2
	        A_y = 3.61
	        A_theta = 1.5708
                A_name = "4"
            elif(self.goal_pose.data == "PLEASE NAVIGATE TO POINT FIVE" or self.goal_pose.data == "NAVIGATE TO POINT FIVE"):
                A_x = 1.9
	        A_y = 1.18
	        A_theta = 1.5708
                A_name = "5"
            
            rospy.loginfo("Ready to go")
            pub.publish("Ready to go")
	    rospy.sleep(1)

	    locations = dict()

	    quaternion = quaternion_from_euler(0.0, 0.0, A_theta)
	    locations['A'] = Pose(Point(A_x, A_y, 0.000), Quaternion(quaternion[0], quaternion[1], quaternion[2], quaternion[3]))

	    self.goal = MoveBaseGoal()
            rospy.loginfo("Starting navigation test")


	    
	    self.goal.target_pose.header.frame_id = 'map'
	    self.goal.target_pose.header.stamp = rospy.Time.now()
	    rospy.loginfo("Going to point "+A_name)
            pub.publish("Going to point "+A_name)
            rospy.sleep(2)
	    self.goal.target_pose.pose = locations['A']
	    self.move_base.send_goal(self.goal)
	    waiting = self.move_base.wait_for_result(rospy.Duration(300))
	    if waiting == 1:
	        rospy.loginfo("Reached point "+A_name)
                pub.publish("Reached point "+A_name)
		rospy.sleep(2)


    def update_initial_pose(self, initial_pose):
        self.initial_pose = initial_pose
	if original == 0:
		self.origin = self.initial_pose.pose.pose
		global original
		original = 1
    
    def update_goal_pose(self, goal_pose):
        self.goal_pose = goal_pose

    def cleanup(self):
        rospy.loginfo("Shutting down navigation	....")
	self.move_base.cancel_goal()

if __name__=="__main__":
    pub = rospy.Publisher('answer', String, queue_size=10)
    rospy.init_node('navi_point')
    try:
        NavToPoint()
        rospy.spin()
    except:
        pass

