#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.use_gripper import UseGripper
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.compute_grasp_part_offset_ariac_state import ComputeGraspPartOffsetAriacState
from ariac_support_flexbe_states.replace_state import ReplaceState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Apr 22 2020
@author: Gerard Harkema
'''
class transport_part_form_bin_to_agv_stateSM(Behavior):
	'''
	transports part from it's bin to the selected agv
	'''


	def __init__(self):
		super(transport_part_form_bin_to_agv_stateSM, self).__init__()
		self.name = 'transport_part_form_bin_to_agv_state'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:21 y:584, x:938 y:468
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_type', 'agv_id', 'part_pose'], output_keys=['pose'])
		_state_machine.userdata.arm_id = 'arm1'
		_state_machine.userdata.agv_id = 'agv1'
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.offset = 0.1
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.move_group_prefix = '/ariac/arm1'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.config_name_R1PreBin1 = 'R1PreBin1'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.srdf_param = 'ur10.srdf'
		_state_machine.userdata.ref_frame1 = 'arm1_linear_arm_actuator'
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.pose = []
		_state_machine.userdata.part = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.part_offset = 0.035
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.config_name_R1PreAGV1 = 'R1PreAGV1'
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.place_offset = 0.05
		_state_machine.userdata.material_locations = []
		_state_machine.userdata.bin_location = ''
		_state_machine.userdata.zero_value = ''
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.ref_frame2 = 'arm2_linear_arm_actuator'
		_state_machine.userdata.agv1 = 'agv1'
		_state_machine.userdata.agv2 = 'agv2'
		_state_machine.userdata.camera_topic2 = '/ariac/Camera_Bin_2'
		_state_machine.userdata.camera_topic3 = '/ariac/Camera_Bin_3'
		_state_machine.userdata.camera_topic5 = '/ariac/Camera_Bin_5'
		_state_machine.userdata.camera_topic4 = '/ariac/Camera_Bin_4'
		_state_machine.userdata.camera_topic6 = '/ariac/Camera_Bin_6'
		_state_machine.userdata.camera_topic1 = '/ariac/Camera_Bin_1'
		_state_machine.userdata.ref_frame = ''
		_state_machine.userdata.camera_frame5 = 'Camera_Bin_5_frame'
		_state_machine.userdata.camera_frame4 = 'Camera_Bin_4_frame'
		_state_machine.userdata.camera_frame3 = 'Camera_Bin_3_frame'
		_state_machine.userdata.camera_frame2 = 'Camera_Bin_2_frame'
		_state_machine.userdata.camera_frame1 = 'Camera_Bin_1_frame'
		_state_machine.userdata.camera_frame6 = 'Camera_Bin_6_frame'
		_state_machine.userdata.part1 = 'gasket_part'
		_state_machine.userdata.part2 = 'pulley_part'
		_state_machine.userdata.part3 = 'piston_rod_part'
		_state_machine.userdata.part4 = 'gear_part'
		_state_machine.userdata.rotation = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:468 y:36
			OperatableStateMachine.add('AgvIdMessage',
										MessageState(),
										transitions={'continue': 'PartTypeMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'agv_id'})

			# x:648 y:35
			OperatableStateMachine.add('PartTypeMessage',
										MessageState(),
										transitions={'continue': 'MoseMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_type'})

			# x:460 y:161
			OperatableStateMachine.add('R1PreGrasp1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'OpenGripper', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreBin1', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:688 y:174
			OperatableStateMachine.add('OpenGripper',
										UseGripper(enable=False),
										transitions={'continue': 'ComputePick', 'failed': 'failed', 'invalid_arm': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:235 y:96
			OperatableStateMachine.add('CheckPosePartsinBIn',
										DetectPartCameraAriacState(time_out=2),
										transitions={'continue': 'R1PreGrasp1', 'failed': 'retry', 'not_found': 'retry'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'pose': 'pose'})

			# x:1325 y:349
			OperatableStateMachine.add('R1PreGrasp1Back',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'GetAGVPose', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreBin1', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:884 y:176
			OperatableStateMachine.add('ComputePick',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'R1ToPick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'pose', 'offset': 'part_offset', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1106 y:178
			OperatableStateMachine.add('R1ToPick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'CloseGripper', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1336 y:188
			OperatableStateMachine.add('CloseGripper',
										UseGripper(enable=True),
										transitions={'continue': 'Wacht1', 'failed': 'failed', 'invalid_arm': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:1329 y:548
			OperatableStateMachine.add('R1PreAGV1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputePlacePose', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreAGV1', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1352 y:259
			OperatableStateMachine.add('Wacht1',
										WaitState(wait_time=1),
										transitions={'done': 'R1PreGrasp1Back'},
										autonomy={'done': Autonomy.Off})

			# x:986 y:718
			OperatableStateMachine.add('R1ToPlace',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'OpenGripper2', 'planning_failed': 'Retry', 'control_failed': 'Retry'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:37 y:655
			OperatableStateMachine.add('R1PreAGV1Back',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreAGV1', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:626 y:689
			OperatableStateMachine.add('OpenGripper2',
										UseGripper(enable=False),
										transitions={'continue': 'Wacht2', 'failed': 'failed', 'invalid_arm': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:349 y:702
			OperatableStateMachine.add('Wacht2',
										WaitState(wait_time=1),
										transitions={'done': 'R1PreAGV1Back'},
										autonomy={'done': Autonomy.Off})

			# x:1341 y:436
			OperatableStateMachine.add('GetAGVPose',
										GetObjectPoseState(object_frame='kit_tray_1', ref_frame='arm1_linear_arm_actuator'),
										transitions={'continue': 'R1PreAGV1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'agv_pose'})

			# x:951 y:616
			OperatableStateMachine.add('Retry',
										WaitState(wait_time=0.1),
										transitions={'done': 'R1ToPlace'},
										autonomy={'done': Autonomy.Off})

			# x:834 y:33
			OperatableStateMachine.add('MoseMessage',
										MessageState(),
										transitions={'continue': 'WelkeAGV?'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_pose'})

			# x:36 y:256
			OperatableStateMachine.add('Gasket?',
										EqualState(),
										transitions={'true': 'ReplaceRef1', 'false': 'Pulley?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part1'})

			# x:30 y:444
			OperatableStateMachine.add('Pulley?',
										EqualState(),
										transitions={'true': 'ReplaceRef_2', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part2'})

			# x:1252 y:694
			OperatableStateMachine.add('ComputePlacePose',
										ComputeGraspPartOffsetAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'R1ToPlace', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'part_pose': 'part_pose', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:14 y:90
			OperatableStateMachine.add('WelkeAGV?',
										EqualState(),
										transitions={'true': 'Gasket?', 'false': 'failed'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv1'})

			# x:138 y:370
			OperatableStateMachine.add('ReplaceRef1',
										ReplaceState(),
										transitions={'done': 'ReplaceTopic1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ref_frame1', 'result': 'ref_frame'})

			# x:28 y:524
			OperatableStateMachine.add('ReplaceRef_2',
										ReplaceState(),
										transitions={'done': 'ReplaceTopic2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ref_frame2', 'result': 'ref_frame'})

			# x:198 y:591
			OperatableStateMachine.add('ReplaceTopic2',
										ReplaceState(),
										transitions={'done': 'ReplaceFrame2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic2', 'result': 'camera_topic'})

			# x:399 y:379
			OperatableStateMachine.add('ReplaceTopic1',
										ReplaceState(),
										transitions={'done': 'ReplaceFrame1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic1', 'result': 'camera_topic'})

			# x:212 y:497
			OperatableStateMachine.add('ReplaceFrame2',
										ReplaceState(),
										transitions={'done': 'ReplacePart2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame2', 'result': 'camera_frame'})

			# x:357 y:312
			OperatableStateMachine.add('ReplaceFrame1',
										ReplaceState(),
										transitions={'done': 'ReplacePart1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame1', 'result': 'camera_frame'})

			# x:224 y:202
			OperatableStateMachine.add('ReplacePart1',
										ReplaceState(),
										transitions={'done': 'RefMSG'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part1', 'result': 'part'})

			# x:435 y:499
			OperatableStateMachine.add('ReplacePart2',
										ReplaceState(),
										transitions={'done': 'CheckPosePartsinBIn'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part2', 'result': 'part'})

			# x:266 y:9
			OperatableStateMachine.add('retry',
										WaitState(wait_time=0.5),
										transitions={'done': 'CheckPosePartsinBIn'},
										autonomy={'done': Autonomy.Off})

			# x:468 y:98
			OperatableStateMachine.add('RefMSG',
										MessageState(),
										transitions={'continue': 'TopicMSG'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ref_frame'})

			# x:648 y:97
			OperatableStateMachine.add('TopicMSG',
										MessageState(),
										transitions={'continue': 'FrameMSG'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'camera_topic'})

			# x:834 y:95
			OperatableStateMachine.add('FrameMSG',
										MessageState(),
										transitions={'continue': 'FrameMSG_2'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'camera_frame'})

			# x:974 y:92
			OperatableStateMachine.add('FrameMSG_2',
										MessageState(),
										transitions={'continue': 'CheckPosePartsinBIn'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
