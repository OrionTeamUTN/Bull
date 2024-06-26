import requests

class CoinPrices:

    connect = 'https://api.binance.com/'

    # Esta api solo acepta los valores de coin en mayúscula y el par siempre
    # se debe escribir como el simbolo de la cripto primero y la stable coin segunda

    # Función para conocer el precio actual
    def actual_price(self, coin: str, stable: str) -> float:

        # Reconstruye el endpoint para el precio actual
        con= f'{self.connect}api/v3/ticker/price?symbol={(coin + stable).upper()}'
        # Genera la conexión al endpoint
        resp = requests.get(con).json()
        
        if 'code' in resp.keys()  and resp['code'] == -1121:
            # Si el par no existe o está mal enviado el formato admitido
            return resp['msg']
        else:
            # Devuelve el precio actual
            return float(resp['price'])


    # Función para conocer los precios de las últimas 24 hs
    def historical_price(self, coin: str, stable: str) -> tuple:
        
        # Reconstruye el endpoint para el cambio de precio en las últimas 24 hs
        con= f'{self.connect}api/v3/ticker/24hr?symbol={(coin + stable).upper()}'
        resp = requests.get(con).json()
        
        # Si el par no existe o está mal enviado el formato admitido
        if 'code' in resp.keys() and resp['code'] == -1121:
            return resp['msg']
        else:
            # Devuelve el precio de apertura
            openPrice = float(resp['openPrice'])
            # Devuelve el precio de cierre
            closePrice = float(resp['openPrice'])
            # Devuelve el porcentaje de cambio
            changeRate = float(resp['priceChangePercent'])
            # Devuelve el precio promedio de las últimas 24hs
            avgPrice = float(resp['weightedAvgPrice'])
            return(openPrice, closePrice, changeRate, avgPrice)


    # Función para pasar de cripto a stable
    def crypto_to_stable(self, coin: str, qty_cripto: float, stable: str) -> float:
        # Primero traemos el precio actual para hacer el cambio
        price = self.actual_price(coin, stable)

        # Verificamos que price no nos haya devuelto error
        if not isinstance(price, str):    
            # Realizamos la conversión
            return qty_cripto * price
        else:
            return price




    # Función para pasar de stable a cripto
    def stable_to_crypto(self, coin: str, stable: str, qty_stable: float) -> float:
        # Primero traemos el precio actual para hacer el cambio
        price = self.actual_price(coin, stable)

        # Verificamos que price no nos haya devuelto error
        if not isinstance(price, str):    
            # Realizamos la conversión
            return qty_stable / price
        else:
            return price

