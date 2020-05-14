#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.use_gripper import UseGripper
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.Compute_belt_drop import ComputeBeltDrop
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu Apr 23 2020
@author: Geert en Stijn
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
		# x:1630 y:562, x:1479 y:95
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['arm'])
		_state_machine.userdata.arm_id = 'arm1'
		_state_machine.userdata.power = 100
		_state_machine.userdata.NoPower = 0
		_state_machine.userdata.part = ''
		_state_machine.userdata.ref_frame1 = 'arm1_linear_arm_actuator'
		_state_machine.userdata.Camera1_topic = '/ariac/Camera_Converyor_Links'
		_state_machine.userdata.camera_frame1 = 'Camera_Converyor_Links_frame'
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.move_group_prefix = '/ariac/arm1'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.arm = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.Disk_rotation = 0
		_state_machine.userdata.Disk_offset = 0.035
		_state_machine.userdata.config_name_R1PreBin3 = 'R1PreBin3'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.config_name_R1PreConveyor = 'R1PreConveyor'
		_state_machine.userdata.Round_Nr = 0
		_state_machine.userdata.Round_target = 6
		_state_machine.userdata.Zero = 0
		_state_machine.userdata.ONE = 1
		_state_machine.userdata.SideYoffset = 0
		_state_machine.userdata.SideXoffset = 0
		_state_machine.userdata.PlusOffset = 0.07
		_state_machine.userdata.config_name_R1HOME = 'R1Home'
		_state_machine.userdata.Row_count = 3
		_state_machine.userdata.offset = 0.040
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.BIN3_pose = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:49 y:25
			OperatableStateMachine.add('MoveToHOME',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GripperUIT_2', 'planning_failed': 'RetryHOME', 'control_failed': 'RetryHOME', 'param_error': 'WAIT_failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1HOME', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1262 y:559
			OperatableStateMachine.add('WAIT_completed',
										WaitState(wait_time=2),
										transitions={'done': 'SluitConveyorAF_2'},
										autonomy={'done': Autonomy.Off})

			# x:202 y:91
			OperatableStateMachine.add('Stopconveyor_2',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'MoveToPreConveyor', 'fail': 'WAIT_failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'NoPower'})

			# x:1106 y:35
			OperatableStateMachine.add('WAIT_failed',
										WaitState(wait_time=5),
										transitions={'done': 'SluitConveyorAF'},
										autonomy={'done': Autonomy.Off})

			# x:563 y:30
			OperatableStateMachine.add('WAIT_check',
										WaitState(wait_time=1),
										transitions={'done': 'CheckforDisk'},
										autonomy={'done': Autonomy.Off})

			# x:372 y:91
			OperatableStateMachine.add('CheckforDisk',
										DetectFirstPartCameraAriacState(part_list=['disk_part'], time_out=2),
										transitions={'continue': 'WaitConveyorStop', 'failed': 'WAIT_failed', 'not_found': 'WAIT_check'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame1', 'camera_topic': 'Camera1_topic', 'camera_frame': 'camera_frame1', 'part': 'part', 'pose': 'pose'})

			# x:200 y:162
			OperatableStateMachine.add('Computebeltpick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveToConveyorPart', 'failed': 'WAIT_failed_pick'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'Disk_offset', 'rotation': 'Disk_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:371 y:166
			OperatableStateMachine.add('MoveToConveyorPart',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'WAIT_gripperoke', 'planning_failed': 'WAIT_failed_pick', 'control_failed': 'RetryDropBin'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1106 y:97
			OperatableStateMachine.add('WAIT_failed_pick',
										WaitState(wait_time=5),
										transitions={'done': 'SluitConveyorAF'},
										autonomy={'done': Autonomy.Off})

			# x:201 y:299
			OperatableStateMachine.add('MoveToBin3',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetBin3Pose', 'planning_failed': 'RetryBin3', 'control_failed': 'RetryBin3', 'param_error': 'WAIT_failed_pick'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreBin3', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:51 y:163
			OperatableStateMachine.add('Gripperaan',
										UseGripper(enable=True),
										transitions={'continue': 'Computebeltpick', 'failed': 'WAIT_failed_pick', 'invalid_arm': 'WAIT_failed_pick'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:370 y:243
			OperatableStateMachine.add('WAIT_gripperoke',
										WaitState(wait_time=0.5),
										transitions={'done': 'MoveToPreConveyor_2'},
										autonomy={'done': Autonomy.Off})

			# x:51 y:96
			OperatableStateMachine.add('MoveToPreConveyor',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Gripperaan', 'planning_failed': 'RetryPreConveyor', 'control_failed': 'RetryPreConveyor', 'param_error': 'WAIT_failed_pick'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreConveyor', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:22 y:707
			OperatableStateMachine.add('RetryPreConveyor',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToPreConveyor'},
										autonomy={'done': Autonomy.Off})

			# x:261 y:768
			OperatableStateMachine.add('RetryBin3',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToBin3'},
										autonomy={'done': Autonomy.Off})

			# x:200 y:231
			OperatableStateMachine.add('MoveToPreConveyor_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'MoveToBin3', 'planning_failed': 'RetryPreConveyor_2', 'control_failed': 'RetryPreConveyor_2', 'param_error': 'WAIT_failed_pick'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreConveyor', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:20 y:769
			OperatableStateMachine.add('RetryPreConveyor_2',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToPreConveyor_2'},
										autonomy={'done': Autonomy.Off})

			# x:358 y:514
			OperatableStateMachine.add('GripperUIT',
										UseGripper(enable=False),
										transitions={'continue': 'AddYOffset', 'failed': 'WAIT_failed_pick', 'invalid_arm': 'WAIT_failed_pick'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:1033 y:518
			OperatableStateMachine.add('AddRound',
										AddNumericState(),
										transitions={'done': 'CheckRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'Round_Nr', 'value_b': 'ONE', 'result': 'Round_Nr'})

			# x:1032 y:584
			OperatableStateMachine.add('CheckRound',
										EqualState(),
										transitions={'true': 'ResetRound', 'false': 'StartConveryor'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'Round_Nr', 'value_b': 'Round_target'})

			# x:1031 y:654
			OperatableStateMachine.add('ResetRound',
										ReplaceState(),
										transitions={'done': 'WAIT_completed'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Round_Nr', 'result': 'Zero'})

			# x:360 y:382
			OperatableStateMachine.add('ComputeDrop',
										ComputeBeltDrop(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'MoveToDROP', 'failed': 'WAIT_failed_drop'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'BIN3_pose', 'offset': 'offset', 'SideYoffset': 'SideYoffset', 'SideXoffset': 'SideXoffset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:359 y:442
			OperatableStateMachine.add('MoveToDROP',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'GripperUIT', 'planning_failed': 'RetryDROP', 'control_failed': 'RetryDROP'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1106 y:159
			OperatableStateMachine.add('WAIT_failed_drop',
										WaitState(wait_time=5),
										transitions={'done': 'SluitConveyorAF'},
										autonomy={'done': Autonomy.Off})

			# x:360 y:768
			OperatableStateMachine.add('RetryDROP',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToDROP'},
										autonomy={'done': Autonomy.Off})

			# x:743 y:522
			OperatableStateMachine.add('AddYOffset',
										AddNumericState(),
										transitions={'done': 'CheckRow'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'SideYoffset', 'value_b': 'PlusOffset', 'result': 'SideYoffset'})

			# x:742 y:579
			OperatableStateMachine.add('CheckRow',
										EqualState(),
										transitions={'true': 'AddXOffset', 'false': 'AddRound'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'Row_count', 'value_b': 'Round_Nr'})

			# x:739 y:700
			OperatableStateMachine.add('ResetRow',
										ReplaceState(),
										transitions={'done': 'AddRound'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'SideYoffset', 'result': 'Zero'})

			# x:739 y:641
			OperatableStateMachine.add('AddXOffset',
										AddNumericState(),
										transitions={'done': 'ResetRow'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'SideXoffset', 'value_b': 'PlusOffset', 'result': 'SideXoffset'})

			# x:156 y:768
			OperatableStateMachine.add('RetryDropBin',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToConveyorPart'},
										autonomy={'done': Autonomy.Off})

			# x:22 y:645
			OperatableStateMachine.add('RetryHOME',
										WaitState(wait_time=1),
										transitions={'done': 'MoveToHOME'},
										autonomy={'done': Autonomy.Off})

			# x:371 y:28
			OperatableStateMachine.add('StartConveryor',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'WAIT_check', 'fail': 'WAIT_failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'power'})

			# x:203 y:26
			OperatableStateMachine.add('GripperUIT_2',
										UseGripper(enable=False),
										transitions={'continue': 'StartConveryor', 'failed': 'WAIT_failed', 'invalid_arm': 'WAIT_failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:1300 y:89
			OperatableStateMachine.add('SluitConveyorAF',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'failed', 'fail': 'WAIT_failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'power'})

			# x:1396 y:560
			OperatableStateMachine.add('SluitConveyorAF_2',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'finished', 'fail': 'WAIT_completed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'power'})

			# x:368 y:311
			OperatableStateMachine.add('GetBin3Pose',
										GetObjectPoseState(object_frame='kit_tray_1', ref_frame='arm1_linear_arm_actuator'),
										transitions={'continue': 'ComputeDrop', 'failed': 'WAIT_failed_drop'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'BIN3_pose'})

			# x:30 y:225
			OperatableStateMachine.add('WaitConveyorStop',
										WaitState(wait_time=1),
										transitions={'done': 'Stopconveyor_2'},
										autonomy={'done': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
