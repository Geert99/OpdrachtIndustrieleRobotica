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
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.message_state import MessageState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Thu May 14 2020
@author: Stijn en Geert
'''
class CameraRobotSelectorSM(Behavior):
	'''
	Selects the right camera and robot
	'''


	def __init__(self):
		super(CameraRobotSelectorSM, self).__init__()
		self.name = 'CameraRobotSelector'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1313 y:295, x:1054 y:659
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['agv_id', 'part_type', 'part_pose'], output_keys=['move_group_prefix', 'config_name', 'arm_id', 'ref_frame', 'camera_topic', 'camera_frame', 'part', 'part_offset', 'overzet', 'config_name_preagv'])
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.move_group_prefix = ''
		_state_machine.userdata.config_name = ''
		_state_machine.userdata.arm_id = ''
		_state_machine.userdata.ref_frame = ''
		_state_machine.userdata.camera_topic = ''
		_state_machine.userdata.camera_frame = ''
		_state_machine.userdata.part = ''
		_state_machine.userdata.part_offset = 0
		_state_machine.userdata.move_group_prefix1 = '/ariac/arm1'
		_state_machine.userdata.move_group_prefix2 = '/ariac/arm2'
		_state_machine.userdata.config_name_r1b2 = 'R1PreBin2'
		_state_machine.userdata.config_name_r1b3 = 'R1PreBin3'
		_state_machine.userdata.config_name_r1b4 = 'R1PreBin4'
		_state_machine.userdata.config_name_r2b3 = 'R2PreBin3'
		_state_machine.userdata.config_name_r2b4 = 'R2PreBin4'
		_state_machine.userdata.config_name_r2b6 = 'R2PreBin6'
		_state_machine.userdata.config_name_r2b5 = 'R2PreBin5'
		_state_machine.userdata.config_name_r1b1 = 'R1PreBin1'
		_state_machine.userdata.arm1_id = 'arm1'
		_state_machine.userdata.arm2_id = 'arm2'
		_state_machine.userdata.ref_frame1 = 'arm1_linear_arm_actuator'
		_state_machine.userdata.ref_frame2 = 'arm2_linear_arm_actuator'
		_state_machine.userdata.camera_topic2 = '/ariac/Camera_Bin_2'
		_state_machine.userdata.camera_topic3 = '/ariac/Camera_Bin_3'
		_state_machine.userdata.camera_topic4 = '/ariac/Camera_Bin_4'
		_state_machine.userdata.camera_topic5 = '/ariac/Camera_Bin_5'
		_state_machine.userdata.camera_topic6 = '/ariac/Camera_Bin_6'
		_state_machine.userdata.camera_topic1 = '/ariac/Camera_Bin_1'
		_state_machine.userdata.camera_frame2 = 'Camera_Bin_2_frame'
		_state_machine.userdata.camera_frame3 = 'Camera_Bin_3_frame'
		_state_machine.userdata.camera_frame4 = 'Camera_Bin_4_frame'
		_state_machine.userdata.camera_frame5 = 'Camera_Bin_5_frame'
		_state_machine.userdata.camera_frame6 = 'Camera_Bin_6_frame'
		_state_machine.userdata.camera_frame1 = 'Camera_Bin_1_frame'
		_state_machine.userdata.part1 = 'gasket_part'
		_state_machine.userdata.part2 = 'pulley_part'
		_state_machine.userdata.part3 = 'piston_rod_part'
		_state_machine.userdata.part4 = 'gear_part'
		_state_machine.userdata.part_offset2 = 0.05
		_state_machine.userdata.part_offset3 = 0.03
		_state_machine.userdata.part_offset4 = 0.03
		_state_machine.userdata.part_offset1 = 0.035
		_state_machine.userdata.agv1_id = 'agv1'
		_state_machine.userdata.agv2_id = 'agv2'
		_state_machine.userdata.overzetja = 'ja'
		_state_machine.userdata.overzetnee = 'nee'
		_state_machine.userdata.overzet = ''
		_state_machine.userdata.config_name_preagv = ''
		_state_machine.userdata.config_name_agv1 = 'R1PreAGV1'
		_state_machine.userdata.config_name_agv2 = 'R2PreAGV2'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:28 y:28
			OperatableStateMachine.add('AGV1?',
										EqualState(),
										transitions={'true': 'Agv1pregrasp', 'false': 'Agv2pregrasp'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'agv_id', 'value_b': 'agv1_id'})

			# x:191 y:345
			OperatableStateMachine.add('Rod?',
										EqualState(),
										transitions={'true': 'Overzetten1', 'false': 'Overzetten1_2'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part3'})

			# x:235 y:234
			OperatableStateMachine.add('Pulley?',
										EqualState(),
										transitions={'true': 'Overzettennee2', 'false': 'Rod?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part2'})

			# x:604 y:60
			OperatableStateMachine.add('r1b1',
										ReplaceState(),
										transitions={'done': 'Offset1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_name_r1b1', 'result': 'config_name'})

			# x:606 y:141
			OperatableStateMachine.add('r1b2',
										ReplaceState(),
										transitions={'done': 'Offset2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_name_r1b2', 'result': 'config_name'})

			# x:646 y:444
			OperatableStateMachine.add('r2b5',
										ReplaceState(),
										transitions={'done': 'Offset3'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_name_r2b5', 'result': 'config_name'})

			# x:632 y:536
			OperatableStateMachine.add('r2b6',
										ReplaceState(),
										transitions={'done': 'Offset4'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_name_r2b6', 'result': 'config_name'})

			# x:796 y:50
			OperatableStateMachine.add('Offset1',
										ReplaceState(),
										transitions={'done': 'CameraTopic1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part_offset1', 'result': 'part_offset'})

			# x:797 y:149
			OperatableStateMachine.add('Offset2',
										ReplaceState(),
										transitions={'done': 'CameraTopic2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part_offset2', 'result': 'part_offset'})

			# x:838 y:432
			OperatableStateMachine.add('Offset3',
										ReplaceState(),
										transitions={'done': 'CameraTopic5'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part_offset3', 'result': 'part_offset'})

			# x:832 y:525
			OperatableStateMachine.add('Offset4',
										ReplaceState(),
										transitions={'done': 'CameraTopic6'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'part_offset4', 'result': 'part_offset'})

			# x:158 y:506
			OperatableStateMachine.add('Gasket2?',
										EqualState(),
										transitions={'true': 'Overzetten1_3', 'false': 'Pulley2?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part1'})

			# x:161 y:698
			OperatableStateMachine.add('Rod2?',
										EqualState(),
										transitions={'true': 'Overzettennee3', 'false': 'Overzettennee4'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part3'})

			# x:158 y:597
			OperatableStateMachine.add('Pulley2?',
										EqualState(),
										transitions={'true': 'Overzetten1_4', 'false': 'Rod2?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part2'})

			# x:407 y:258
			OperatableStateMachine.add('Overzetten1',
										ReplaceState(),
										transitions={'done': 'r2b5'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetja', 'result': 'overzet'})

			# x:401 y:335
			OperatableStateMachine.add('Overzetten1_2',
										ReplaceState(),
										transitions={'done': 'r2b6'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetja', 'result': 'overzet'})

			# x:383 y:412
			OperatableStateMachine.add('Overzetten1_3',
										ReplaceState(),
										transitions={'done': 'r1b1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetja', 'result': 'overzet'})

			# x:374 y:496
			OperatableStateMachine.add('Overzetten1_4',
										ReplaceState(),
										transitions={'done': 'r1b2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetja', 'result': 'overzet'})

			# x:1046 y:61
			OperatableStateMachine.add('CameraTopic1',
										ReplaceState(),
										transitions={'done': 'CameraFrame1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic1', 'result': 'camera_topic'})

			# x:1046 y:138
			OperatableStateMachine.add('CameraTopic2',
										ReplaceState(),
										transitions={'done': 'CameraFrame_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic2', 'result': 'camera_topic'})

			# x:1032 y:429
			OperatableStateMachine.add('CameraTopic5',
										ReplaceState(),
										transitions={'done': 'CameraFrame_5'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic5', 'result': 'camera_topic'})

			# x:1037 y:525
			OperatableStateMachine.add('CameraTopic6',
										ReplaceState(),
										transitions={'done': 'CameraFrame_6'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_topic6', 'result': 'camera_topic'})

			# x:1229 y:66
			OperatableStateMachine.add('CameraFrame1',
										ReplaceState(),
										transitions={'done': 'Refframe'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame1', 'result': 'camera_frame'})

			# x:1229 y:143
			OperatableStateMachine.add('CameraFrame_2',
										ReplaceState(),
										transitions={'done': 'Refframe'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame2', 'result': 'camera_frame'})

			# x:1254 y:424
			OperatableStateMachine.add('CameraFrame_5',
										ReplaceState(),
										transitions={'done': 'Refframe_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame5', 'result': 'camera_frame'})

			# x:1258 y:520
			OperatableStateMachine.add('CameraFrame_6',
										ReplaceState(),
										transitions={'done': 'Refframe_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'camera_frame6', 'result': 'camera_frame'})

			# x:1399 y:121
			OperatableStateMachine.add('Refframe',
										ReplaceState(),
										transitions={'done': 'movegroupprefix1'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ref_frame1', 'result': 'ref_frame'})

			# x:1564 y:120
			OperatableStateMachine.add('movegroupprefix1',
										ReplaceState(),
										transitions={'done': 'armid'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'move_group_prefix1', 'result': 'move_group_prefix'})

			# x:1667 y:219
			OperatableStateMachine.add('armid',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm1_id', 'result': 'arm_id'})

			# x:1432 y:451
			OperatableStateMachine.add('Refframe_2',
										ReplaceState(),
										transitions={'done': 'movegroupprefix1_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'ref_frame2', 'result': 'ref_frame'})

			# x:1599 y:452
			OperatableStateMachine.add('movegroupprefix1_2',
										ReplaceState(),
										transitions={'done': 'armid_2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'move_group_prefix2', 'result': 'move_group_prefix'})

			# x:1667 y:296
			OperatableStateMachine.add('armid_2',
										ReplaceState(),
										transitions={'done': 'finished'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'arm2_id', 'result': 'arm_id'})

			# x:221 y:124
			OperatableStateMachine.add('Gasket?',
										EqualState(),
										transitions={'true': 'Overzettennee1', 'false': 'Pulley?'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'part_type', 'value_b': 'part1'})

			# x:403 y:71
			OperatableStateMachine.add('Overzettennee1',
										ReplaceState(),
										transitions={'done': 'oz'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetnee', 'result': 'overzet'})

			# x:386 y:167
			OperatableStateMachine.add('Overzettennee2',
										ReplaceState(),
										transitions={'done': 'r1b2'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetnee', 'result': 'overzet'})

			# x:409 y:588
			OperatableStateMachine.add('Overzettennee3',
										ReplaceState(),
										transitions={'done': 'r2b5'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetnee', 'result': 'overzet'})

			# x:460 y:705
			OperatableStateMachine.add('Overzettennee4',
										ReplaceState(),
										transitions={'done': 'r2b6'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'overzetnee', 'result': 'overzet'})

			# x:465 y:0
			OperatableStateMachine.add('oz',
										MessageState(),
										transitions={'continue': 'r1b1'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'overzet'})

			# x:30 y:90
			OperatableStateMachine.add('Agv1pregrasp',
										ReplaceState(),
										transitions={'done': 'Gasket?'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_name_agv1', 'result': 'config_name_preagv'})

			# x:5 y:360
			OperatableStateMachine.add('Agv2pregrasp',
										ReplaceState(),
										transitions={'done': 'Gasket2?'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'config_name_agv2', 'result': 'config_name_preagv'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
