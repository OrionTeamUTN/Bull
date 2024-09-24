from flask import Blueprint, request
from app.schemas.coin_schema import coin_schema, coins_schema
from app.services.coin_services import CoinServices

# instanciar el objeto Blueprint

coin = Blueprint('coin',__name__, url_prefix='api/coins')
coin_services = CoinServices()


"""si en el 'services dice que lo que espera como argumento es un diccionario ... xej ..  def(.... algo:dict) 
entonces en el 'save ()   sin argumentos
pero va adentro '"""


# tantos archivos como los que se ven en Schemas

# y en cada archivo una ruta para cada funcion .. que las encuentro en 

@coin.route('/save',methods=['POST'])
def save():
    coin = coin_schema.load(request.json)
    return coin_schema.dump(coin_services.save(coin))

""" ESTAMOS HACIENDO BASICAMENTE:
    dato = account_services.save(acc)
    dato2 = account_schema.dump(dato)
    dato3 = {"account" : dato2 }
    return dato3 """



@coin.route('/delete/<int:id>',methods=['DELETE'])
def delete(id: int):
    return{"coin": coin_schema.delete(id)}


# ACA PIDE ADMIN ID
@coin.route('/update/<id:int>/<int:id_admin>', methods =['PUT'])
def update(id:int, id_admin: int):
    coin = coin_schema.load(request.json)
    return coin_schema.dump(coin_services.update(id, id_admin))


@coin.route('/find_by_id/<int:id>',methods=['GET'])
def find_by_id(id: int):
    return coin_schema.dump(coin_services.find_by_id(id)) 


@coin.route('/get_all', methods=['GET'])
def get_all():
    return coin_schema.dump(coin_services.get_all())


@coin.route('/find_by_name/<str:name>', methods = ['GET'])
def find_by_name(name: str):
    return coin_schema.dump(coin_services.find_by_name(name))



@coin.route('/find_by_symbol/<str:symbol>', methods = ['GET'])
def find_by_symbol(symbol: str):
    return coin_schema.dump(coin_services.find_by_symbol(symbol))


@coin.route('/get_active_coins',methods = ['GET'])
def get_active_coins():
    return coin_schema.dump(coin_services.get_active_coins())


@coin.route('/get_inactive_coins',methods = ['GET'])
def get_inactive_coins():
    return coin_schema.dump(coin_services.get_inactive_coins())
