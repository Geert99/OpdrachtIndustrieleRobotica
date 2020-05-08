#!/usr/bin/env python

# Software License Agreement (BSD License)
#
# Copyright (c) 2020, Avans Hogeschool
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Avans Hogeschool nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Gerard Harkema


import rospy
import rostopic
import inspect

import tf2_ros
import tf2_geometry_msgs

from flexbe_core import EventState, Logger
from geometry_msgs.msg import Pose, PoseStamped
from osrf_gear.msg import LogicalCameraImage, Model
from flexbe_core.proxy import ProxySubscriberCached

'''

Created on Sep 5 2018

@author: HRWROS mooc instructors

'''

class GetObjectPoseState(EventState):
	'''
	State to detect the pose of a object

  	-- object_frame		string		the objectd frame
	-- ref_frame		string		reference frame for the part pose output key
	-- time_out		float		Time with the camera to have detected the part
	#> pose			PoseStamped	Pose of the detected part

	<= continue 				if the pose of the object has been succesfully obtained
	<= time_out 				a timeout

	<= failed 				otherwise
	'''

	def __init__(self, object_frame, ref_frame, time_out = 5.0):
		# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(GetObjectPoseState, self).__init__(outcomes = ['continue', 'time_out', 'failed'], output_keys = ['pose'])
		self.ref_frame = ref_frame
		self._object_frame = object_frame
		self._failed = False

		# Store state parameter for later use.
		self._wait = time_out


		# tf to transfor the object pose
		self._tf_buffer = tf2_ros.Buffer(rospy.Duration(10.0)) #tf buffer length
		self._tf_listener = tf2_ros.TransformListener(self._tf_buffer)

	def execute(self, userdata):
		# This method is called periodically while the state is active.
		# Main purpose is to check state conditions and trigger a corresponding outcome.
		# If no outcome is returned, the state will stay active.

		if self._failed:
			userdata.pose = None
			return 'failed'

		elapsed = rospy.get_rostime() - self._start_time;
		if (elapsed.to_sec() > self._wait):
			return 'time_out'

		pose_stamped = PoseStamped()
		pose = Pose()

		pose.position = self._transform.transform.translation
		pose.orientation = self._transform.transform.rotation 

		rospy.loginfo(pose)
		rospy.loginfo(pose_stamped)

		pose_stamped.pose = pose
		pose_stamped.header.frame_id = self._object_frame
		pose_stamped.header.stamp = rospy.Time.now()
		# Transform the pose to desired output frame
		pose_stamped = tf2_geometry_msgs.do_transform_pose(pose_stamped, self._transform)
		rospy.loginfo(pose_stamped)
		userdata.pose = pose_stamped
		return 'continue'


	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

		self._start_time = rospy.get_rostime()


		# Get transform between world and robot_base
		try:
			self._transform = self._tf_buffer.lookup_transform(self._object_frame, self.ref_frame, rospy.Time(0), rospy.Duration(1.0))
			rospy.loginfo(self._transform)
		except Exception as e:
			Logger.logwarn('Could not transform pose: ' + str(e))
		 	self._failed = True


	def on_exit(self, userdata):
		# This method is called when an outcome is returned and another state gets active.
		# It can be used to stop possibly running processes started by on_enter.

		pass # Nothing to do


	def on_start(self):
		# This method is called when the behavior is started.
		# If possible, it is generally better to initialize used resources in the constructor
		# because if anything failed, the behavior would not even be started.
		self._start_time = rospy.Time.now()

	def on_stop(self):
		# This method is called whenever the behavior stops execution, also if it is cancelled.
		# Use this event to clean up things like claimed resources.

		pass # Nothing to do



