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
from ariac_flexbe_behaviors.notify_shipment_ready_sm import notify_shipment_readySM
from ariac_flexbe_states.message_state import MessageState
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
		self.add_behavior(notify_shipment_readySM, 'notify_shipment_ready')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:867 y:12, x:483 y:355
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.order_id = ''
		_state_machine.userdata.shipments = []
		_state_machine.userdata.number_of_shipments = 0
		_state_machine.userdata.shipment_type = ''
		_state_machine.userdata.shipment_index = 0
		_state_machine.userdata.agv_id = ''
		_state_machine.userdata.number_of_products = 0
		_state_machine.userdata.products = []
		_state_machine.userdata.product_index = 0
		_state_machine.userdata.part_type = ''
		_state_machine.userdata.part_pose = []
		_state_machine.userdata.increment = 1
		_state_machine.userdata.Null = 0
		_state_machine.userdata.pose_on_agv = []
		_state_machine.userdata.old_order_id = ''

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
										transitions={'continue': 'TestLastOrder'},
										autonomy={'continue': Autonomy.Off},
										remapping={'order_id': 'order_id', 'shipments': 'shipments', 'number_of_shipments': 'number_of_shipments'})

			# x:410 y:121
			OperatableStateMachine.add('getProductsfromshipment',
										GetProductsFromShipmentState(),
										transitions={'continue': 'ShipmentID', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'shipments': 'shipments', 'index': 'shipment_index', 'shipment_type': 'shipment_type', 'agv_id': 'agv_id', 'products': 'products', 'number_of_products': 'number_of_products'})

			# x:848 y:122
			OperatableStateMachine.add('transport_part_form_bin_to_agv_state',
										self.use_behavior(transport_part_form_bin_to_agv_stateSM, 'transport_part_form_bin_to_agv_state'),
										transitions={'finished': 'IncreaseProductIndex', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit},
										remapping={'part_type': 'part_type', 'agv_id': 'agv_id', 'part_pose': 'part_pose', 'pose': 'pose'})

			# x:649 y:120
			OperatableStateMachine.add('GetPartinfo',
										GetPartFromProductsState(),
										transitions={'continue': 'transport_part_form_bin_to_agv_state', 'invalid_index': 'failed'},
										autonomy={'continue': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'products': 'products', 'index': 'product_index', 'type': 'part_type', 'pose': 'part_pose'})

			# x:928 y:241
			OperatableStateMachine.add('IncreaseProductIndex',
										AddNumericState(),
										transitions={'done': 'CheckProduct_index'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'increment', 'result': 'product_index'})

			# x:934 y:323
			OperatableStateMachine.add('CheckProduct_index',
										EqualState(),
										transitions={'true': 'SETnull', 'false': 'GetPartinfo'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'product_index', 'value_b': 'number_of_products'})

			# x:770 y:514
			OperatableStateMachine.add('IncreaseShipmentIndex',
										AddNumericState(),
										transitions={'done': 'Checkshipmentindex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value_a': 'shipment_index', 'value_b': 'increment', 'result': 'shipment_index'})

			# x:396 y:499
			OperatableStateMachine.add('Checkshipmentindex',
										EqualState(),
										transitions={'true': 'get_order', 'false': 'notify_shipment_ready'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'number_of_shipments', 'value_b': 'shipment_index'})

			# x:990 y:530
			OperatableStateMachine.add('SETnull',
										ReplaceState(),
										transitions={'done': 'IncreaseShipmentIndex'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'Null', 'result': 'product_index'})

			# x:721 y:355
			OperatableStateMachine.add('notify_shipment_ready',
										self.use_behavior(notify_shipment_readySM, 'notify_shipment_ready'),
										transitions={'finished': 'getProductsfromshipment', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:388 y:13
			OperatableStateMachine.add('TestLastOrder',
										EqualState(),
										transitions={'true': 'finished', 'false': 'RememberOldOrder'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'value_a': 'order_id', 'value_b': 'old_order_id'})

			# x:632 y:44
			OperatableStateMachine.add('RememberOldOrder',
										ReplaceState(),
										transitions={'done': 'getProductsfromshipment'},
										autonomy={'done': Autonomy.Off},
										remapping={'value': 'order_id', 'result': 'old_order_id'})

			# x:40 y:265
			OperatableStateMachine.add('ShipmentID',
										MessageState(),
										transitions={'continue': 'GetPartinfo'},
										autonomy={'continue': Autonomy.Off},
										remapping={'message': 'shipment_type'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
