from flask import Blueprint, request
from app.schemas.account_schema import account_schema, accounts_schema
from app.services.account_services import AccountService

#OJO Aparece "AccountService" (en SINGULAR)

account = Blueprint('account',__name__, url_prefix='/api/accounts')
account_services = AccountService()


# Argumentos en el def ¿¿
@account.route('/save',methods=['POST'])
def save():
    account = account_schema.load(request.json)
    return account_schema.dump(account_services.save(account))
    

# argumentos en el def van ¿¿
# en los argumentos .. creo que va al reves <id : int>?
@account.route('/update/<int:id>',methods=['PUT'])
def update(id:int):
    account = account_schema.load(request.json)
    return account_schema.dump(account_services.update(account,id))
    

## Acá delete no pide un dict .... solo un id
## Argumentos del def van ¿¿
@account.route('/delete/<int:id>',methods=['DELETE'])
def delete(id: int):
   return account_services.delete(id)
    

## va el self¿¿
# pongo "lo que devuelve ¿¿"
@account.route('/find_by_id/<int:id>',methods=['GET'])
def find_by_id(id: int):
    return account_schema.dump(account_services.find_by_id(id))
    

# no me queda claro que devuelven los "find by"... account¿¿ dict¿¿
# en Services creo que habría que poner lo que devuelve el find_by_username 
# es decir agrear  -> Account.. idem para find_by_dni
@account.route('/find_by_username', methods=['GET'])
def find_by_username():
    account = account_schema.load(request.json)
    return account_schema.dump(account_services.find_by_username(account['username']))


# en estos no convendría agregar -> dict  para especificar que devuelve un dict¿¿
@account.route('/find_by_dni/<int:dni>', methods=['GET'])    
def find_by_dni(dni: int):
    return account_schema.dump(account_services.find_by_dni(dni))
    

## ni idea como pedir dos aparametros 
@account.route('/check_auth/<int:dni>', methods=['GET'])
def check_auth(dni : int):  
    account = account_schema.load(request.json)
    return account_schema.dump(account_services.check_auth(account['dni'], account['password']))
    

# acá devuelvo un json o un dict
@account.get_other_account_info('/find_other_account_info', methods=['GET'])
def get_other_account_info (): 
    account = account_schema.load(request.json)
    return account_schema.dump(account_services.get_other_account_info(account['target_acc_dni'], account['admin_dni']))