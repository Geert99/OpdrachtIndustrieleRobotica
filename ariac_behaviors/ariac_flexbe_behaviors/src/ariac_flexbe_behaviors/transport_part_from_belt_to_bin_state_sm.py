#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Apr 23 2020
@author: Gerard Harkema
'''
class transport_part_from_belt_to_bin_stateSM(Behavior):
	'''
	Transports a part from pelt to a its own bin.
	'''


	def __init__(self):
		super(transport_part_from_belt_to_bin_stateSM, self).__init__()
		self.name = 'transport_part_from_belt_to_bin_state'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1189 y:652, x:1235 y:42
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['arm'])
		_state_machine.userdata.arm = ''
		_state_machine.userdata.power = 100
		_state_machine.userdata.NoPower = 0
		_state_machine.userdata.part1 = 'disk_part'
		_state_machine.userdata.ref_frame1 = 'arm1_linear_arm_actuator'
		_state_machine.userdata.Camera1_topic = '/ariac/Camera_Converyor_Links'
		_state_machine.userdata.camera_frame1 = 'Camera_Converyor_Links_frame'
		_state_machine.userdata.part3 = 'piston_rod_part'
		_state_machine.userdata.Camera2_topic = '/ariac/Camera_Converyor_Rechts'
		_state_machine.userdata.ref_frame2 = 'arm2_linear_arm_actuator'
		_state_machine.userdata.camera_frame2 = 'Camera_Converyor_Rechts_frame'
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.part2 = 'gasket_part'
		_state_machine.userdata.part4 = 'disk_part'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:131 y:27
			OperatableStateMachine.add('StartConveryor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'WAIT_check', 'fail': 'WAIT_failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'power'})

			# x:1053 y:645
			OperatableStateMachine.add('WAIT_completed',
										WaitState(wait_time=5),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off})

			# x:663 y:31
			OperatableStateMachine.add('Stopconveyor_2',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'WAIT_completed', 'fail': 'WAIT_failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'NoPower'})

			# x:1106 y:35
			OperatableStateMachine.add('WAIT_failed',
										WaitState(wait_time=5),
										transitions={'done': 'failed'},
										autonomy={'done': Autonomy.Off})

			# x:298 y:163
			OperatableStateMachine.add('WAIT_check',
										WaitState(wait_time=2),
										transitions={'done': 'CheckforDisk'},
										autonomy={'done': Autonomy.Off})

			# x:441 y:35
			OperatableStateMachine.add('CheckforDisk',
										DetectFirstPartCameraAriacState(part_list=['disk_part'], time_out=2),
										transitions={'continue': 'Stopconveyor_2', 'failed': 'WAIT_failed', 'not_found': 'WAIT_check'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame1', 'camera_topic': 'Camera1_topic', 'camera_frame': 'camera_frame1', 'part': 'part', 'pose': 'pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
