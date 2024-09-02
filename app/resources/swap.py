from flask import Blueprint, request
from app.schemas.coin_schema import swap_schema, swaps_schema
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