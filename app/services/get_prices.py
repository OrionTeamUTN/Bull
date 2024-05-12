import requests

connect = 'https://api.binance.com/api/v3/ticker/'

# Función para conocer el precio actual
def actual_price(coin):
    con= f'{connect}price?symbol={coin}'    # Reconstruye el endpoint para el precio actual
    resp = requests.get(con)
    price = round(float(resp.json()['price']),2)    # Devuelve el precio actual
    
    return(price)

# Función para conocer los precios de las últimas 24 hs
def historical_price(coin):
    con= f'{connect}24hr?symbol={coin}' # Reconstruye el endpoint para el cambio de precio en las últimas 24 hs
    resp = requests.get(con)
    openPrice = round(float(resp.json()['openPrice']), 2)   # Devuelve el precio de apertura
    closePrice = round(float(resp.json()['openPrice']), 2)  # Devuelve el precio de cierre
    changeRate = round(float(resp.json()['priceChangePercent']), 2) # Devuelve el porcentaje de cambio
    avgPrice = round(float(resp.json()['weightedAvgPrice']), 2) # Devuelve el precio promedio de las últimas 24hs

    return(openPrice, closePrice, changeRate, avgPrice)

