from flask import Blueprint, request

from app.schemas.wallet_schema import wallet_schema, wallets_schema
from app.services.wallet_services import WalletServices

wallet = Blueprint('wallet',__name__, url_prefix='api/wallet')
wallet_services = WalletServices()



@wallet.route('/save',method=['POST'])
def save():
    pass

@wallet.route('/update',method=['PUT'])
def update():
    pass

@wallet.route('/delete',method=['DELETE'])
def delete():
    pass

@wallet.route('/get_all',method=['GET'])
def get_all():
    pass


@wallet.route('/find_by_id',method=['GET'])
def find_by_id():
    pass

@wallet.route('/find_by_coin_name',method=['GET'])
def find_by_coin_name():
    pass

@wallet.route('/find_by_coin_symbol',method=['GET'])
def find_by_coin_symbol():
    pass

@wallet.route('/check_balance',method=['PUT'])
def check_balance():
    pass


# withdraw
# find_by_positive_balance
# find_by_zero_balance