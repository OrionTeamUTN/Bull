from flask import Blueprint, request
from app.schemas.swap_schema import swap_schema, swaps_schema
from app.services.swap_services import SwapServices
from datetime import datetime

swap = Blueprint('swap',__name__, url_prefix='api/swaps')
swap_services = SwapServices()


@swap.route('/save',methods=['POST'])
def save():
    swap = swap_schema.load(request.json)
    return swap_schema.dump(swap_services.update(swap))
    
@swap.route('/update/<int:id>',methods=['PUT'])
def update(id: int):
    pass

@swap.route('/delete',methods=['DELETE'])
def delete():
    pass


@swap.route('/get_all',methods=['GET'])
def get_all():
    return swap_schema.dump(swap_services.get_all())


@swap.route('/find_by_id/<int:id>',methods=['GET'])
def find_by_id(id: int):
    return swap_schema.dump(swap_services.find_by_id(id))


@swap.route('/filter_by_wallet_send/<int:idwallet>',methods = ['GET'])
def filter_by_wallet_send(idwallet: int):
    return swap_schema.dump(swap_services.filter_by_wallet_send(idwallet))

@swap.route('/filter_by_wallet_recv/<int:idwallet>', methods = ['GET'])
def filter_by_wallet_recv(idwallet: int):
    return swap_schema.dump(swap_services.filter_by_wallet_recv(idwallet))


@swap.route('/filter_by_wallet/<int:idwallet>', methods = ['GET'])
def filter_by_wallet(idwallwt: int):
    return swap_schema.dump(swap_services.filter_by_wallet(idwallet))

# PREGUNTAR
@swap.route('filter_by_op_date/<datetime:op_date>', methods=['GET'])
def filter_by_op_date(l_swaps,op_date: datetime):
    return swap_schema.dump(swap_services.filter_by_op_date(l_swaps, op_date))

# PREGUNTAR
@swap.route('/filter_by_wallet_at_op_date/<datetime:date>/<id:int>', methods = ['GET'])
def filter_by_wallet_at_op_date(op_date: datetime, id: int):
    return swap_schema.dump(swap_services.filter_by_wallet_at_op_date(op_date, id))

