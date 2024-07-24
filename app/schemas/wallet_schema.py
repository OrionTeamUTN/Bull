from app import ma
from account_schema import AccountSchema
from coin_schema import CoinSchema

class WalletSchema(ma.Schema):
    class Meta:
        fields = ('id_wallet', 'balance', 'id_owner_account', 'id_wallet_coin')

    id_owner_account = ma.Nested(AccountSchema)
    id_wallet_coin = ma.Nested(CoinSchema)

wallet_schema = WalletSchema()   # Serializa solo un elemento
wallets_schema = WalletSchema(many=True)  # Serializa mas de un elemento al mismo tiempo