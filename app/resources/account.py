from flask import Blueprint, request
from app.schemas.account_schema import account_schema, accounts_schema
from app.services.account_services import AccountService

#OJO Aparece "AccountService" (en SINGULAR)

account = Blueprint('account',__name__, url_prefix='api/accounts')
account_services = AccountServices()


"""si en el 'services dice que lo que espera como argumento es un diccionario ... xej ..  def(.... algo:dict) 
entonces en el 'save ()   sin argumentos
pero va adentro '"""



@account.route('/save',method=['POST'])
def save():
    pass

@account.route('/update',method=['PUT'])
def update():
    pass

@account.route('/delete',method=['DELETE'])
def delete():
    pass

@account.route('/find_by_id',method=['GET'])
def find_by_id():
    pass

@account.route('/find_by_username', method = ['GET'])
def find_by_username(self, username: str):
    pass

@account.route('/find_by_dni', method = '[GET]')    
def find_by_dni():
    pass

@account.route('/check_auth', method = ['GET'])
def check_auth(): 
    pass
    
@account.get_other_account_info('/find_other_account_info', method=['GET'])
def get_other_account_info ():
    pass