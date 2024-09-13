from flask import Blueprint, request
from app.schemas.swap_schema import swap_schema, swaps_schema
from app.services.swap_services import SwapServices

swap = Blueprint('swap',__name__, url_prefix='api/swaps')
swap_services = SwapServices()


@swap.route('/save',method=['POST'])
def save():
    pass

@swap.route('/update',method=['PUT'])
def update():
    pass

@swap.route('/delete',method=['DELETE'])
def delete():
    pass

@swap.route('/get_all',method=['GET'])
def get_all():
    pass


@swap.route('/find_by_id',method=['GET'])
def find_by_id():
    pass

@swap.route('/filter_by_wallet_send',method = ['GET'])
def filter_by_wallet_send():
    pass

@swap.route('/filter_by_wallet_recv', method = ['GET'])
def filter_by_wallet_recv():
    pass


@swap.route('/filter_by_wallet', method = ['GET'])
def filter_by_wallet():
    pass

@swap.route('filter_by_op_date', method=['GET'])
def filter_by_op_date():
    pass

@swap.route('/filter_by_wallet_at_op_date', method = ['GET'])
def filter_by_wallet_at_op_date():
    pass

