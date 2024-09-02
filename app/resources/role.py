from flask import Blueprint, request
from app.schemas.role_schema import role_schema, roles_schema
from app.services.role_services import RoleServices 

role = Blueprint('role',__name__, url_prefix='api/roles')
role_services = RoleServices()

@role.route('/save',method=['POST'])
def save():
    pass

@role.route('/delete',method=['DELETE'])
def save():
    pass

@role.route('/update',method=['GET'])
def save():
    pass


@role.route('/find_by_id',method=['GET'])
def save():
    pass

@role.route('/find_by_role_name',method=['GET'])
def save():
    pass

@role.route('/get_all_roles',method=['GET'])
def save():
    pass