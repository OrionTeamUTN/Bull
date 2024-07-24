from app import ma
from wallet_schema import WalletSchema

class SwapSchema(ma.Schema):
    class Meta:
        fields = ('id_swap', 'operation_date', 'amount_send', 'amount_recv', 'id_wallet_send', 'id_wallet_recv')
    
    id_wallet_send = ma.Nested(WalletSchema)
    id_wallet_recv = ma.Nested(WalletSchema)

swap_schema = SwapSchema()   # Serializa solo un elemento
swaps_schema = SwapSchema(many=True)  # Serializa mas de un elemento al mismo tiempo