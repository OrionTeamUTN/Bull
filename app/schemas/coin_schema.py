from app import ma

class CoinSchema(ma.Schema):
    class Meta:
        fields = ('id_coin', 'coin_name', 'coin_symbol', 'is_active')

coin_schema = CoinSchema()   # Serializa solo un elemento
coins_schema = CoinSchema(many=True)  # Serializa mas de un elemento al mismo tiempo