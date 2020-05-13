#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.start_assignment_state import StartAssignment
from ariac_logistics_flexbe_states.get_order_state import GetOrderState
from ariac_logistics_flexbe_states.get_products_from_shipment_state import GetProductsFromShipmentState
from ariac_flexbe_behaviors.transport_part_form_bin_to_agv_state_sm import transport_part_form_bin_to_agv_stateSM
from ariac_logistics_flexbe_states.get_part_from_products_state import GetPartFromProductsState
from ariac_support_flexbe_states.add_numeric_state import AddNumericState
from ariac_support_flexbe_states.equal_state import EqualState
from ariac_support_flexbe_states.replace_state import ReplaceState
from ariac_flexbe_states.end_assignment_state import EndAssignment
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed May 13 2020
@author: Geert en Stijn
'''
class order_handelingSM(Behavior):
	'''
	dit is een behaivor voor het handelen van orders
	'''


	def __init__(self):
		super(order_handelingSM, self).__init__()
		self.name = 'order_handeling'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(transport_part_form_bin_to_agv_stateSM, 'transport_part_form_bin_to_agv_state')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1444 y:130, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.order_id = ''
		_state_machine.userdata.shipments = []
		_state_machine.userdata.number_of_shipments = 0
		_state_machine.userdata.shipment_type = 0
		_state_machine.userdata.shipment_index = ''
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.number_of_products = 0
		_state_machine.userdata.products = []
		_state_machine.userdata.product_index = 0
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.increment = 1
		_state_machine.userdata.Null = 0
		_state_machine.userdata.pose_on_agv = []

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:49 y:117
			OperatableStateMachine.add('startassignment',
										StartAssignment(),
										transitions={'continue': 'get_order'},
										autonomy={'continue': Autonomy.Off})

			# x:207 y:119
			OperatableStateMachine.add('get_order',
										GetOrderState(),
										transitions={'continue': 'getProductsfromshipment'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:410 y:121
			OperatableStateMachine.add('getProductsfromshipment',
										GetProductsFromShipmentState(),
										transitions={'continue': 'GetPartinfo', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'product_index', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:848 y:122
			OperatableStateMachine.add('transport_part_form_bin_to_agv_state',
										self.use_behavior(transport_part_form_bin_to_agv_stateSM, 'transport_part_form_bin_to_agv_state'),
										transitions={'finished': 'IncreaseProductIndex', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'agv_id': 'agv_id', 'pose_on_agv': 'pose_on_agv'})

			# x:649 y:120
			OperatableStateMachine.add('GetPartinfo',
										GetPartFromProductsState(),
										transitions={'continue': 'transport_part_form_bin_to_agv_state', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'product_index', 'type': 'part_type', 'pose': 'part_pose'})

			# x:930 y:194
			OperatableStateMachine.add('IncreaseProductIndex',
										AddNumericState(),
										transitions={'done': 'CheckProduct_index'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'increment', 'result': 'product_index'})

			# x:932 y:255
			OperatableStateMachine.add('CheckProduct_index',
										EqualState(),
										transitions={'true': 'SETnull', 'false': 'IncreaseProductIndex'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'number_of_products'})

			# x:932 y:382
			OperatableStateMachine.add('IncreaseShipmentIndex',
										AddNumericState(),
										transitions={'done': 'Checkshipmentindex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'increment', 'result': 'shipment_index'})

			# x:933 y:444
			OperatableStateMachine.add('Checkshipmentindex',
										EqualState(),
										transitions={'true': 'SETnull_2', 'false': 'getProductsfromshipment'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_shipments', 'value_b': 'shipment_index'})

			# x:931 y:314
			OperatableStateMachine.add('SETnull',
										ReplaceState(),
										transitions={'done': 'IncreaseShipmentIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Null', 'result': 'product_index'})

			# x:934 y:503
			OperatableStateMachine.add('SETnull_2',
										ReplaceState(),
										transitions={'done': 'EndAssignment'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Null', 'result': 'shipment_index'})

			# x:1194 y:160
			OperatableStateMachine.add('EndAssignment',
										EndAssignment(),
										transitions={'continue': 'finished'},
										autonomy={'continue': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
