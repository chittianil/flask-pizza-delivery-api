from flask import Flask
from .orders.views import order_namespace
from flask_restx import Api
from .auth.views import auth_namespace
from .config.config import config_dict

from .utils.db import db
from .models.orders import Order
from .models.users import User

from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound ,MethodNotAllowed

def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    app.config.from_object(config)
    authorizations = {
        "Bearer Auth" :{
            "type" : "apiKey",
            "in" : "header",
            "name" : "Authorization",
            "description":  "Add a JWT with ** Bearer &lt:JWT&gt: to authorize"
        }
    }
    
    db.init_app(app)
    jwt =JWTManager(app)
    migrate=Migrate(app,db)
    
    
        
        
    api =Api(app, 
             title="Pizza Delivery Api",
             description="A Rest Api for pizza delivery service",
             authorizations=authorizations,
             security="Bearer Auth")
    api.add_namespace(order_namespace)
    api.add_namespace(auth_namespace, path='/auth')
    
    
    @api.errorhandler(NotFound)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'Method not Allowed'}, 405
    
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': User, 'Order': Order}
    return app