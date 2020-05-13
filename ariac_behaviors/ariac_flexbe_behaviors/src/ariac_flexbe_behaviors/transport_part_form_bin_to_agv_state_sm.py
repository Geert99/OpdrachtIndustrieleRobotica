#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_logistics_flexbe_states.get_material_locations import GetMaterialLocationsState
from ariac_flexbe_states.message_state import MessageState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.use_gripper import UseGripper
from ariac_flexbe_states.detect_part_camera_ariac_state import DetectPartCameraAriacState
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from flexbe_states.wait_state import WaitState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
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
		# x:50 y:436, x:669 y:461
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['part_type', 'agv_id', 'pose_on_agv'], output_keys=['pose'])
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.pose_on_agv = []
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
		_state_machine.userdata.ref_frame = 'arm1_linear_arm_actuator'
		_state_machine.userdata.camera_frame = 'Camera_Bin_1_frame'
		_state_machine.userdata.camera_topic = '/ariac/Camera_Bin_1'
		_state_machine.userdata.pose = ''
		_state_machine.userdata.part = 'gasket_part'
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.part_offset = 0.035
		_state_machine.userdata.part_rotation = 0
		_state_machine.userdata.config_name_R1PreAGV1 = 'R1PreAGV1'
		_state_machine.userdata.agv_pose = []
		_state_machine.userdata.place_offset = 0.05
		_state_machine.userdata.material_locations = []
		_state_machine.userdata.bin_location = ''
		_state_machine.userdata.zero_value = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:71 y:40
			OperatableStateMachine.add('GetPartLocation',
										GetMaterialLocationsState(),
										transitions={'continue': 'GetBinLocation'},
										autonomy={'continue': Autonomy.Off},
										remapping={'part': 'part_type', 'material_locations': 'material_locations'})

			# x:834 y:33
			OperatableStateMachine.add('MoseMessage',
										MessageState(),
										transitions={'continue': 'CheckPosePartsinBIn'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'pose_on_agv'})

			# x:648 y:35
			OperatableStateMachine.add('PartTypeMessage',
										MessageState(),
										transitions={'continue': 'MoseMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'part_type'})

			# x:438 y:162
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

			# x:54 y:161
			OperatableStateMachine.add('CheckPosePartsinBIn',
										DetectPartCameraAriacState(time_out=2),
										transitions={'continue': 'R1PreGrasp1', 'failed': 'failed', 'not_found': 'failed'},
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
										transitions={'reached': 'ComputePlace', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name_R1PreAGV1', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1352 y:259
			OperatableStateMachine.add('Wacht1',
										WaitState(wait_time=1),
										transitions={'done': 'R1PreGrasp1Back'},
										autonomy={'done': Autonomy.Off})

			# x:1254 y:718
			OperatableStateMachine.add('ComputePlace',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'R1ToPlace', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'agv_pose', 'offset': 'place_offset', 'rotation': 'part_rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

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

			# x:1019 y:593
			OperatableStateMachine.add('Retry',
										WaitState(wait_time=0.1),
										transitions={'done': 'R1ToPlace'},
										autonomy={'done': Autonomy.Off})

			# x:277 y:27
			OperatableStateMachine.add('GetBinLocation',
										GetItemFromListState(),
										transitions={'done': 'AgvIdMessage', 'invalid_index': 'failed'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'material_locations', 'index': 'zero_value', 'item': 'bin_location'})

			# x:468 y:36
			OperatableStateMachine.add('AgvIdMessage',
										MessageState(),
										transitions={'continue': 'PartTypeMessage'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'agv_id'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
