from flask_jwt_extended import create_access_token, jwt_required
from abc import ABC, abstractmethod
import datetime
import jwt
import pytz
import os

from app.models import Account

class AbstractJWT(ABC):
    """
    Clase abstracta con métodos abstractos para generar y verificar JWT
    """

    @abstractmethod
    def generate_token(self, account: Account) -> str:
        pass 

    @abstractmethod
    def verify_token(self, token: str):
        pass

class PyJWT(AbstractJWT):
    """
    Clase que hereda de AbstractJWT y define sus metodos utilizando la libreria PyJWT
    """

    __secret_key = os.getenv('JWT_SECRET_KEY') # llave secreta desde el .env
    tz = pytz.timezone('America/Argentina/Mendoza') # zona horaria (necesario especificar para cambiar la zona horaria en la decodificación del token, que por defecto es en zona UTC)

    def generate_token(self, account: Account) -> str:
        """
        Genera y devuelve un token con el payload: 
            'username': username del parámtero account
            'id_rol': id del rol que tiene la cuenta
            'iat': fecha de creación 
            'exp': fecha de expiración
        Parametro: objeto account
        """
        payload = {
            'username': account.username,
            'id_role': account.id_role,
            'iat': datetime.datetime.now(tz=self.tz), # fecha de emisión/creación (indicando zona horaria)
            'exp': datetime.datetime.now(tz=self.tz) + datetime.timedelta(hours=1) # fecha de expiración: fecha actual + tiempo de expiracion 
        }
        token = jwt.encode(payload, self.__secret_key, algorithm='HS256')
        return token
    
    def verify_token(self, token: str):
        """
        Verifica el token. Utiliza algoritmo HS256.
        Si es válido, devuelve el payload
        Si no lo es, devuelve la excepción que corresponda
        """
        try:
            payload = jwt.decode(token, self.__secret_key, algorithms=['HS256'])
            return payload
        except jwt.exceptions.InvalidTokenError as error: # es la excepción básica
            return error
        
class JWTSecurity:
    """
    Clase encargada de generación y verificación de JWT
    """

    def __init__(self, jwt_security: AbstractJWT):
        """ Recibe y se define por objeto del tipo AbstractJWT o que herede de este"""
        self.jwt_security = jwt_security

    def generate_token(self, account: Account) -> str:
        """
        Genera y devueve un token con el payload: 
            'username': username del parámtero account
            'id_rol': id del rol que tiene la cuenta
            'iat': fecha de creación 
            'exp': fecha de expiración
        """
        return self.jwt_security.generate_token(account)
    
    def verify_token(self, token: str):
        """
        Verifica el token. 
            Si es válido, devuelve el payload
            Si no lo es, devuelve la excepción que corresponda
        """
        return self.jwt_security.verify_token(token)
    