#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.use_gripper import UseGripper
from flexbe_states.wait_state import WaitState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.get_object_pose import GetObjectPoseState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Fri May 15 2020
@author: Stijn en Geert
'''
class op_overzetbin_plaatsen_en_frame_kiezenSM(Behavior):
	'''
	Ervoor zorgen dat de part in de overzetbin geplaatst en een nieuwe camera gekozen wordt.
	'''


	def __init__(self):
		super(op_overzetbin_plaatsen_en_frame_kiezenSM, self).__init__()
		self.name = 'op_overzetbin_plaatsen_en_frame_kiezen'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1723 y:19, x:585 y:171
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['ref_frame', 'config_name', 'move_group_prefix', 'arm_id', 'agv_id', 'part_type'], output_keys=['move_group_prefix', 'config_name', 'arm_id', 'ref_frame', 'camera_topic', 'camera_frame', 'part_offset', 'overzet'])
		_state_machine.userdata.ref_frame = ''
		_state_machine.userdata.bin3_pose = ''
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.move_group_prefix = ''
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.arm_id = ''
		_state_machine.userdata.offset = 0.5
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.agv1_id = 'agv1'
		_state_machine.userdata.agv2_id = 'agv2'
		_state_machine.userdata.part_offset = 0
		_state_machine.userdata.partoffset1 = 0.035
		_state_machine.userdata.partoffset2 = 0.081
		_state_machine.userdata.partoffset3 = 0.02
		_state_machine.userdata.partoffset4 = 0.025
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.part1 = 'gasket_part'
		_state_machine.userdata.part2 = 'pulley_part'
		_state_machine.userdata.part3 = 'piston_rod_part'
		_state_machine.userdata.part4 = 'gear_part'
		_state_machine.userdata.move_group_prefix1 = '/ariac/arm1'
		_state_machine.userdata.move_group_prefix2 = '/ariac/arm2'
		_state_machine.userdata.config_namer1 = 'R1PreBin4'
		_state_machine.userdata.config_namer2 = 'R2PreBin4'
		_state_machine.userdata.arm1_id = 'arm1'
		_state_machine.userdata.arm2_id = 'arm2'
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.camera_topic4 = '/ariac/Camera_Bin_4'
		_state_machine.userdata.camera_frame4 = 'Camera_Bin_4_frame'
		_state_machine.userdata.overzet = ''
		_state_machine.userdata.overzetnee = 'nee'
		_state_machine.userdata.ref_frame1 = 'arm1_linear_arm_actuator'
		_state_machine.userdata.ref_frame2 = 'arm2_linear_arm_actuator'
		_state_machine.userdata.config_name1 = 'R1PreBin1'
		_state_machine.userdata.config_name4 = 'R2PreBin6'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:91 y:23
			OperatableStateMachine.add('Arm?',
										EqualState(),
										transitions={'true': 'R1', 'false': 'R2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'arm_id', 'value_b': 'arm1_id'})

			# x:630 y:12
			OperatableStateMachine.add('PreBin3',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'ComputeDrop3', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:907 y:30
			OperatableStateMachine.add('ComputeDrop3',
										ComputeGraspAriacState(joint_names=['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']),
										transitions={'continue': 'DropBin3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'tool_link': 'tool_link', 'pose': 'bin3_pose', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1122 y:79
			OperatableStateMachine.add('DropBin3',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'OpengripperBin3', 'planning_failed': 'failed', 'control_failed': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'move_group_prefix': 'move_group_prefix', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1142 y:173
			OperatableStateMachine.add('OpengripperBin3',
										UseGripper(enable=False),
										transitions={'continue': 'WachtenGripper', 'failed': 'failed', 'invalid_arm': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'invalid_arm': Autonomy.Off},
										remapping={'arm_id': 'arm_id'})

			# x:984 y:236
			OperatableStateMachine.add('WachtenGripper',
										WaitState(wait_time=1),
										transitions={'done': 'PreBin3Back'},
										autonomy={'done': Autonomy.Off})

			# x:799 y:244
			OperatableStateMachine.add('PreBin3Back',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'AGV?', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:16 y:99
			OperatableStateMachine.add('AGV?',
										EqualState(),
										transitions={'true': 'PreBin4', 'false': 'PreBin1'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv1_id'})

			# x:186 y:106
			OperatableStateMachine.add('R1',
										ReplaceState(),
										transitions={'done': 'Getbin3Pose'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_namer1', 'result': 'config_name'})

			# x:254 y:189
			OperatableStateMachine.add('R2',
										ReplaceState(),
										transitions={'done': 'Getbin3Pose_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_namer2', 'result': 'config_name'})

			# x:331 y:21
			OperatableStateMachine.add('Getbin3Pose',
										GetObjectPoseState(object_frame='bin3_frame', ref_frame='arm1_linear_arm_actuator'),
										transitions={'continue': 'PreBin3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'bin3_pose'})

			# x:1615 y:384
			OperatableStateMachine.add('CameraTopic',
										ReplaceState(),
										transitions={'done': 'CameraFrame'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic4', 'result': 'camera_topic'})

			# x:1644 y:217
			OperatableStateMachine.add('CameraFrame',
										ReplaceState(),
										transitions={'done': 'Overzetnee'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame4', 'result': 'camera_frame'})

			# x:1651 y:97
			OperatableStateMachine.add('Overzetnee',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetnee', 'result': 'overzet'})

			# x:170 y:444
			OperatableStateMachine.add('rod',
										EqualState(),
										transitions={'true': 'RepaceOffset_3', 'false': 'RepaceOffset_4'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part3'})

			# x:73 y:289
			OperatableStateMachine.add('gasket',
										EqualState(),
										transitions={'true': 'RepaceOffset', 'false': 'pulley'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part1'})

			# x:171 y:357
			OperatableStateMachine.add('pulley',
										EqualState(),
										transitions={'true': 'RepaceOffset_2', 'false': 'rod'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part2'})

			# x:86 y:713
			OperatableStateMachine.add('rod_2',
										EqualState(),
										transitions={'true': 'RepaceOffset_7', 'false': 'RepaceOffset_8'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part3'})

			# x:43 y:523
			OperatableStateMachine.add('gasket_2',
										EqualState(),
										transitions={'true': 'RepaceOffset_5', 'false': 'pulley_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part1'})

			# x:110 y:608
			OperatableStateMachine.add('pulley_2',
										EqualState(),
										transitions={'true': 'RepaceOffset_6', 'false': 'rod_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part2'})

			# x:451 y:287
			OperatableStateMachine.add('RepaceOffset',
										ReplaceState(),
										transitions={'done': 'R1PreBin3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset1', 'result': 'part_offset'})

			# x:451 y:344
			OperatableStateMachine.add('RepaceOffset_2',
										ReplaceState(),
										transitions={'done': 'R1PreBin3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset2', 'result': 'part_offset'})

			# x:450 y:402
			OperatableStateMachine.add('RepaceOffset_3',
										ReplaceState(),
										transitions={'done': 'R1PreBin3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset3', 'result': 'part_offset'})

			# x:450 y:463
			OperatableStateMachine.add('RepaceOffset_4',
										ReplaceState(),
										transitions={'done': 'R1PreBin3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset4', 'result': 'part_offset'})

			# x:452 y:557
			OperatableStateMachine.add('RepaceOffset_5',
										ReplaceState(),
										transitions={'done': 'R1PreBin3_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset1', 'result': 'part_offset'})

			# x:453 y:614
			OperatableStateMachine.add('RepaceOffset_6',
										ReplaceState(),
										transitions={'done': 'R1PreBin3_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset2', 'result': 'part_offset'})

			# x:453 y:674
			OperatableStateMachine.add('RepaceOffset_7',
										ReplaceState(),
										transitions={'done': 'R1PreBin3_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset3', 'result': 'part_offset'})

			# x:454 y:733
			OperatableStateMachine.add('RepaceOffset_8',
										ReplaceState(),
										transitions={'done': 'R1PreBin3_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'partoffset4', 'result': 'part_offset'})

			# x:802 y:342
			OperatableStateMachine.add('R1PreBin3',
										ReplaceState(),
										transitions={'done': 'RefFrame'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_namer1', 'result': 'config_name'})

			# x:958 y:342
			OperatableStateMachine.add('RefFrame',
										ReplaceState(),
										transitions={'done': 'MoveGroupPrefix'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ref_frame1', 'result': 'ref_frame'})

			# x:1115 y:342
			OperatableStateMachine.add('MoveGroupPrefix',
										ReplaceState(),
										transitions={'done': 'ArmID'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'move_group_prefix1', 'result': 'move_group_prefix'})

			# x:1273 y:342
			OperatableStateMachine.add('ArmID',
										ReplaceState(),
										transitions={'done': 'CameraTopic'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm1_id', 'result': 'arm_id'})

			# x:802 y:419
			OperatableStateMachine.add('R1PreBin3_2',
										ReplaceState(),
										transitions={'done': 'RefFrame_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_namer2', 'result': 'config_name'})

			# x:958 y:419
			OperatableStateMachine.add('RefFrame_2',
										ReplaceState(),
										transitions={'done': 'MoveGroupPrefix_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ref_frame2', 'result': 'ref_frame'})

			# x:1115 y:419
			OperatableStateMachine.add('MoveGroupPrefix_2',
										ReplaceState(),
										transitions={'done': 'ArmID_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'move_group_prefix2', 'result': 'move_group_prefix'})

			# x:1273 y:419
			OperatableStateMachine.add('ArmID_2',
										ReplaceState(),
										transitions={'done': 'CameraTopic'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm2_id', 'result': 'arm_id'})

			# x:397 y:93
			OperatableStateMachine.add('Getbin3Pose_2',
										GetObjectPoseState(object_frame='bin3_frame', ref_frame='arm2_linear_arm_actuator'),
										transitions={'continue': 'PreBin3', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'pose': 'bin3_pose'})

			# x:73 y:182
			OperatableStateMachine.add('PreBin4',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'gasket', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name4', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:17 y:343
			OperatableStateMachine.add('PreBin1',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'gasket_2', 'planning_failed': 'failed', 'control_failed': 'failed', 'param_error': 'failed'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name1', 'move_group': 'move_group', 'move_group_prefix': 'move_group_prefix', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
