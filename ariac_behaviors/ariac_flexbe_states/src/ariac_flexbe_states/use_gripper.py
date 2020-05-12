#!/usr/bin/env python
import rospy

from flexbe_core import EventState, Logger
from osrf_gear.srv import VacuumGripperControl, VacuumGripperControlRequest, VacuumGripperControlResponse


class UseGripper(EventState):
	'''	Opening or closing the gripper of robot1 or robot2
	-- enable		bool		If 'true' the gripper is opened		
	#> arm_id		string		Which robot is used
	<= continue				The gripper is in its desired state
	<= failed				The gripper did not get to its desired state after a certain amount of time
	<= invalid_arm				Invalid arm id
	'''
	def __init__(self, enable):
	# Declare outcomes, input_keys, and output_keys by calling the super constructor with the corresponding arguments.
		super(UseGripper, self).__init__(input_keys = ['arm_id'], outcomes = ['continue', 'failed', 'invalid_arm'])

		self._enable = enable

		pass # Nothing to do

 
	def execute(self, userdata):
        # This method is called periodically while the state is active.
        # Main purpose is to check state conditions and trigger a corresponding outcome.
        # If no outcome is returned, the state will stay active.

 		if userdata.arm_id == 'arm1':
			gripper_service = '/ariac/arm1/gripper/control'
		else:
			if userdata.arm_id == 'arm2':
				gripper_service = '/ariac/arm1/gripper/control'
			else:
				return 'invalid_arm'

       		rospy.loginfo("Waiting for service...")
		rospy.wait_for_service(gripper_service)
		try:
		
			vacuum_gripper_control = rospy.ServiceProxy(gripper_service, VacuumGripperControl)

			request = VacuumGripperControlRequest()
			request.enable = self._enable

			service_response = vacuum_gripper_control(request)
			
			rospy.loginfo("I only got here AFTER the service call was completed!")

			if service_response.succes == True:
				return 'continue'
			else:
				return 'failed'
		
		except rospy.ServiceException, e:
			rospy.loginfo("Service call failed: %s"%e)
			return 'failed'


 
	def on_enter(self, userdata):
		# This method is called when the state becomes active, i.e. a transition from another state to this one is taken.
		# It is primarily used to start actions which are associated with this state.

	 
		pass # Nothing to do

 
	def on_exit(self, userdata):
        	# This method is called when an outcome is returned and another state gets active.
        	# It can be used to stop possibly running processes started by on_enter.

 

        	pass # Nothing to do

 
	def on_start(self):
        	# This method is called when the behavior is started.
        	# If possible, it is generally better to initialize used resources in the constructor
        	# because if anything failed, the behavior would not even be started.
        	pass

 
	def on_stop(self):
        	# This method is called whenever the behavior stops execution, also if it is cancelled.
        	# Use this event to clean up things like claimed resources.

 

        	pass # Nothing to do
		
