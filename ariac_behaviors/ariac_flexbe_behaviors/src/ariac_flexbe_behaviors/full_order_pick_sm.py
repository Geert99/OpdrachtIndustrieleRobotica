#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from flexbe_states.wait_state import WaitState
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_flexbe_behaviors.transport_part_form_bin_to_agv_state_sm import transport_part_form_bin_to_agv_stateSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Tue May 12 2020
@author: Geert en Stijn
'''
class Full_order_pickSM(Behavior):
	'''
	Deze behaivor pick de volledige order door middel van de behaivor bin_to_agv_state
	'''


	def __init__(self):
		super(Full_order_pickSM, self).__init__()
		self.name = 'Full_order_pick'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(transport_part_form_bin_to_agv_stateSM, 'transport_part_form_bin_to_agv_state')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:472 y:615, x:38 y:355
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.part_type = part_type
		_state_machine.userdata.agv_id = agv_id
		_state_machine.userdata.pose_on_agv = pose_on_agv

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:427 y:22
			OperatableStateMachine.add('standby',
										WaitState(wait_time=3),
										transitions={'done': 'Get_order'},
										autonomy={'done': Autonomy.Off})

			# x:399 y:103
			OperatableStateMachine.add('Get_order',
										GetOrderState(),
										transitions={'continue': 'transport_part_form_bin_to_agv_state'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:368 y:302
			OperatableStateMachine.add('transport_part_form_bin_to_agv_state',
										self.use_behavior(transport_part_form_bin_to_agv_stateSM, 'transport_part_form_bin_to_agv_state'),
										transitions={'finished': 'finished', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'agv_id': 'agv_id', 'pose_on_agv': 'pose_on_agv'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
