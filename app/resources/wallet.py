from flask import Blueprint, request

from app.schemas.wallet_schema import wallet_schema, wallets_schema
from app.services.wallet_services import WalletServices

wallet = Blueprint('wallet',__name__, url_prefix='api/wallets')
wallet_services = WalletServices()


## A diferencia de todos NO GUARDO UN DICT ?
@wallet.route('/save/<int:accid>/<int:coinid>',methods=['POST'])
def save(accid: int, coinid: int):
    return wallet_schema.dump(wallet_services.save(accid, coinid))

@wallet.route('/update/<int:idwallet/<int:balance>>',methods=['PUT'])
def update(idwallet: int, balance: int):
    return wallet_schema.dump(wallet_services.update(idwallet,balance))    

@wallet.route('/delete/<int:idwallet>',methods=['DELETE'])
def delete(idwallet: int):
    return wallet_schema.dump(wallet_services.delete(idwallet))


@wallet.route('/get_all',methods=['GET'])
def get_all():
    return wallet_schema.dump(wallet_services.get_all())


@wallet.route('/find_by_id/<int:idwallet>',methods=['GET'])
def find_by_id(idwallet: int):
    return wallet_schema.dump(wallet_services.find_by_id(idwallet))

@wallet.route('/find_by_coin_name/',methods=['GET'])
def find_by_coin_name():
    wallet = wallet_schema
    pass

@wallet.route('/find_by_coin_symbol',methods=['GET'])
def find_by_coin_symbol():
    wallet = wallet_schema.load(request.json)
    return wallet_schema.dump(wallet_services.find_by_coin_symbol(wallet['coin_symbol']))

@wallet.route('/check_balance',methods=['PUT'])
def check_balance():
    return


@wallet.route('/withdraw', methods = ['PUT'])
def withdraw():
    pass


@wallet.route('/find_by_positive_balance', methods = ['GET'])
def find_by_positive_balance():
    return wallet_schema.dump(wallet_services.find_by_positive_balance())


@wallet.route('/find_by_zero_balance', methods = ['GET'])
def find_by_zero_balance():
    return wallet_schema.dump(wallet_services.find_by_zero_balance())
