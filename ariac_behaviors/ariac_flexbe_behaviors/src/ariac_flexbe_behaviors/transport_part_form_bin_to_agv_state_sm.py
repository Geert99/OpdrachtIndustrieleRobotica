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
from ariac_flexbe_states.compute_grasp_part_offset_ariac_state import ComputeGraspPartOffsetAriacState
from ariac_flexbe_behaviors.camerarobotselector_sm import CameraRobotSelectorSM
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_behaviors.op_overzetbin_plaatsen_en_frame_kiezen_sm import op_overzetbin_plaatsen_en_frame_kiezenSM
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
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
		self.add_behavior(CameraRobotSelectorSM, 'CameraRobotSelector')
		self.add_behavior(op_overzetbin_plaatsen_en_frame_kiezenSM, 'op_overzetbin_plaatsen_en_frame_kiezen')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:21 y:601, x:938 y:468
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_type', 'agv_id', 'part_pose'], output_keys=['pose'])
		_state_machine.userdata.arm_id = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.joint_values = []
		_state_machine.userdata.joint_names = []
		_state_machine.userdata.offset = 0.2
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.move_group_prefix = ''
		_state_machine.userdata.action_topic = '/move_group'
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
		_state_machine.userdata.material_locations = []
		_state_machine.userdata.bin_location = ''
		_state_machine.userdata.zero_value = ''
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.ref_frame2 = 'arm2_linear_arm_actuator'
		_state_machine.userdata.agv2 = 'agv2'
		_state_machine.userdata.ref_frame = ''
		_state_machine.userdata.part1 = 'gasket_part'
		_state_machine.userdata.part2 = 'pulley_part'
		_state_machine.userdata.part3 = 'piston_rod_part'
		_state_machine.userdata.part4 = 'gear_part'
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.overzet = ''
		_state_machine.userdata.overzetja = 'ja'
		_state_machine.userdata.overzetnee = 'nee'
		_state_machine.userdata.agv1_id = 'agv1'
		_state_machine.userdata.agv2_id = 'agv2'

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
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

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
										remapping={'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part_type', 'pose': 'pose'})

			# x:1325 y:349
			OperatableStateMachine.add('R1PreGrasp1Back',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Overzetten?', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

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
										transitions={'reached': 'ComputePlace', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_preagv', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

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
										remapping={'config_name': 'config_name_preagv', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

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

			# x:951 y:616
			OperatableStateMachine.add('Retry',
										WaitState(wait_time=0.1),
										transitions={'done': 'R1ToPlace'},
										autonomy={'done': Autonomy.Off})

			# x:834 y:33
			OperatableStateMachine.add('MoseMessage',
										MessageState(),
										transitions={'continue': 'CameraRobotSelector'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_pose'})

			# x:1238 y:628
			OperatableStateMachine.add('ComputePlacePose',
										ComputeGraspPartOffsetAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'R1ToPlace', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'part_pose': 'part_pose', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:266 y:9
			OperatableStateMachine.add('retry',
										WaitState(wait_time=0.5),
										transitions={'done': 'CheckPosePartsinBIn'},
										autonomy={'done': Autonomy.Off})

			# x:42 y:416
			OperatableStateMachine.add('RefMSG',
										MessageState(),
										transitions={'continue': 'TopicMSG'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'ref_frame'})

			# x:190 y:412
			OperatableStateMachine.add('TopicMSG',
										MessageState(),
										transitions={'continue': 'FrameMSG'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'camera_topic'})

			# x:330 y:414
			OperatableStateMachine.add('FrameMSG',
										MessageState(),
										transitions={'continue': 'CheckPosePartsinBIn'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'camera_frame'})

			# x:133 y:217
			OperatableStateMachine.add('CameraRobotSelector',
										self.use_behavior(CameraRobotSelectorSM, 'CameraRobotSelector'),
										transitions={'finished': 'RefMSG', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'agv_id': 'agv_id', 'part_type': 'part_type', 'part_pose': 'part_pose', 'move_group_prefix': 'move_group_prefix', 'config_name': 'config_name', 'arm_id': 'arm_id', 'ref_frame': 'ref_frame', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part': 'part', 'part_offset': 'part_offset', 'overzet': 'overzet', 'config_name_preagv': 'config_name_preagv'})

			# x:1551 y:346
			OperatableStateMachine.add('Overzetten?',
										EqualState(),
										transitions={'true': 'AGV?', 'false': 'op_overzetbin_plaatsen_en_frame_kiezen'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'overzet', 'value_b': 'overzetnee'})

			# x:1469 y:662
			OperatableStateMachine.add('ComputePlace',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'R1ToPlace', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'agv_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1179 y:60
			OperatableStateMachine.add('op_overzetbin_plaatsen_en_frame_kiezen',
										self.use_behavior(op_overzetbin_plaatsen_en_frame_kiezenSM, 'op_overzetbin_plaatsen_en_frame_kiezen'),
										transitions={'finished': 'CheckPosePartsinBIn', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'ref_frame': 'ref_frame', 'config_name': 'config_name', 'move_group_prefix': 'move_group_prefix', 'arm_id': 'arm_id', 'agv_id': 'agv_id', 'part_type': 'part_type', 'camera_topic': 'camera_topic', 'camera_frame': 'camera_frame', 'part_offset': 'part_offset', 'overzet': 'overzet'})

			# x:1324 y:446
			OperatableStateMachine.add('GetAGV1Pose',
										GetObjectPoseState(object_frame='kit_tray_1', ref_frame='arm1_linear_arm_actuator'),
										transitions={'continue': 'R1PreAGV1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'agv_pose'})

			# x:1531 y:492
			OperatableStateMachine.add('GetAGV1Pose_2',
										GetObjectPoseState(object_frame='kit_tray_2', ref_frame='arm2_linear_arm_actuator'),
										transitions={'continue': 'R1PreAGV1', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'agv_id'})

			# x:1670 y:414
			OperatableStateMachine.add('AGV?',
										EqualState(),
										transitions={'true': 'GetAGV1Pose', 'false': 'GetAGV1Pose_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv1_id'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
