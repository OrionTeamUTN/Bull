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

@coin.route('/save',method=['POST'])
def save():
    pass
    coin = coin_schema.load(request.json)
    return{"coin": coin_schema.dump(coin_services.save(coin))}

""" ESTAMOS HACIENDO BASICAMENTE:
    dato = account_services.save(acc)
    dato2 = account_schema.dump(dato)
    dato3 = {"account" : dato2 }
    return dato3 """



@coin.route('/delete',method=['DELETE'])
def delete():
    pass
    coin = coin_schema.load(request.jason)
    return{"coin": coin_schema.dump(coin_services, delete)}

@coin.route('/update', method =['UPDATE'])
def update():
    pass

@coin.route('/get_all', method=['GET'])
def get_all():
    pass

@coin.route('/find_by_id',method=['GET'])
def gind_by_id():
    pass


@coin.route('/find_by_name', method = ['GET'])
def find_by_name():
    pass

@coin.route('/find_by_symbol', method = ['GET'])
def find_by_symbol():
    pass

@coin.route('/get_active_coins',method = ['GET'])
def get_active_coins():
    pass

@coin.route('/get_inactive_coins',method = ['GET'])
def get_inactive_coins():
    pass