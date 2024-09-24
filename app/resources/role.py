from flask import Blueprint, request
from app.schemas.role_schema import role_schema, roles_schema
from app.services.role_services import RoleServices 

role = Blueprint('role',__name__, url_prefix='api/roles')
role_services = RoleServices()


# OJO con el idadmin
@role.route('/save/<int:adminid>',methods=['POST'])
def save(idadmin: int):
    role = role_schema.load(request.json)
    return role_schema.dump(role_services.save(role, idadmin))s


# OJO aca hay problemas de seguridad
@role.route('/delete/<int:id>/<int:idadmin>',methods=['DELETE'])
def delte(id:int, idadmin: int):
    return role_services.delete(id, idadmin)



# OJO aca hay prolbemas de seguridad
# qué es el "New role" (parametro en el servicio tipo dict)
@role.route('/update/<int:id>/<int:idadmin>',methods=['PUT'])
def update(id: int, idadmin: int):
    role = role_schema.load(request.json)
    return role_schema.dump(role_services.update(id, idadmin))


@role.route('/find_by_id/<int:id>',methods=['GET'])
def find_by_id(id: int):
    return role_schema.dump(role_services.find_by_id(id))


@role.route('/find_by_role_name/<str:name>',methods=['GET'])
def find_by_role_name(name: str):
    return role_schema.dump(role_services.find_by_role_name(name))


@role.route('/get_all_roles',methods=['GET'])
def get_all_roles():
    return role_schema.dump(role_services.get_all_roles())
