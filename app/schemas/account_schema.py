from app import ma
from role_schema import RoleSchema

class AccountSchema(ma.Schema):
    class Meta:
        fields = ('id_account', 'username', 'password', 'email', 'first_name', 'last_name', 'phone', 
                  'address', 'dni', 'birthdate', 'id_role')
        
    id_role = ma.Nested(RoleSchema)

account_schema = AccountSchema()   # Serializa solo un elemento
accounts_schema = AccountSchema(many=True)  # Serializa mas de un elemento al mismo tiempo