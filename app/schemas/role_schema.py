from app import ma

class RoleSchema(ma.Schema):
    class Meta:
        fields = ('id_role', 'role_name')

role_schema = RoleSchema()   # Serializa solo un elemento
roles_schema = RoleSchema(many=True)  # Serializa mas de un elemento al mismo tiempo