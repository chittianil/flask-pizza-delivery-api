from flask_restx import Namespace, Resource,fields
from ..models.orders import Order
from ..models.users import User
from http import HTTPStatus
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..utils.db import db 

order_namespace = Namespace("orders",description="Namespace for orders")


order_model = order_namespace.model(
    'Orders',{
        'id':fields.Integer(description='Order id'),
        'size':fields.String(description = 'Size of Order', required = True),
        # 'price':fields.Float(description = 'Price of Order', required = True,
        #                      enum = ['SMALL','MEDIUM','LARGE','EXTRA_LARGE']),
        'order_status' : fields.String(description = 'Status of Order', required = True,
                                       enum = ['PENDING','IN_TRANSIT','DELIVERED']),
        
    }
    
)


order_status_model = order_namespace.model(
    
    'OrderStatus',{
        'order_status' : fields.String(required =True,description = "Order Status",
                                       enum = ['PENDING','IN_TRANSIT','DELIVERED'])
    }
    
    
)
   

@order_namespace.route('/orders')
class OrderGetcreate(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = "Retrive All orders")
    @jwt_required()
    def get(self):
        """ Get all orders"""
        orders = Order.query.all()
        return orders,HTTPStatus.OK
    
    
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = "Place an order")
    @jwt_required()
    def post(self):
        """
        Place a new order
        """
        username = get_jwt_identity()
        current_user = User.query.filter_by(username=username).first()
        data = order_namespace.payload
        new_order = Order(
            size = data['size'],
            quantity = data['quantity'],
            flavour = data['flavour']
        
        )
        new_order.user = current_user
        new_order.save()
        return new_order , HTTPStatus.CREATED
    
    
    
        
@order_namespace.route('/order/<int:order_id>')
class OrderGetUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = "Retrive an order by Id")
    @jwt_required()
    def get(self, order_id):
        """ Get order by id """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK
    
   
    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description = "Update an order given an order id",
        params = { "order_id": "An ID for given order"})
    
    @jwt_required()
    
    def put(self, order_id):
        """ Update order by id """
        order_to_update  = Order.get_by_id(order_id)
        data = order_namespace.payload
        order_to_update.quantity = data["quantity"]
        order_to_update.size = data["size"]
        order_to_update.flavour = data['flavour']
        db.session.commit()
        return order_to_update, HTTPStatus.OK
        
    
    @jwt_required()  
    @order_namespace.marshal_with(order_model)  
    @order_namespace.doc(description = "Delete an order given an order id",
                         params = { "order_id": "An ID for given order"})
    def delete(self, order_id):
        """ Delete order by id """
        
        order_to_delete = Order.get_by_id(order_id)
        order_to_delete.delete()
        return order_to_delete,HTTPStatus.NO_CONTENT
        
        
@order_namespace.route('/user/<int:user_id>/order/<int:order_id>/')
class GetSpecificOrderByUser(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = "Get a user's specific order",
                         params = { "order_id": "An ID for given order",
                                   "user_id": "An ID for given user"})
    @jwt_required()
    def get(self,user_id,order_id):
        """ get  user specific order"""
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()
        return order, HTTPStatus.OK

@order_namespace.route('/user/<int:user_id>/orders')
class UserOrders(Resource):
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description = "Get orders a user given the userid",
                         params = { "user_id": "An ID for given user"})
    @jwt_required()
    def get(self,user_id):
        """ get all orders by specific user"""
        user = User.get_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK
    
    
    
@order_namespace.route('/order/status/<int:order_id>')

class UpdateOrderStatus(Resource):
    @order_namespace.expect(order_status_model)
    @order_namespace.marshal_with(order_status_model)
    @order_namespace.doc(description = "Update an order status given the order id",
                         params = { "order_id": "An ID for given order"})
    @jwt_required()
    def patch(self,order_id):
        """ 
        Update order status
        """
        data = order_namespace.payload
        order_to_update = Order.get_by_id(order_id)
        order_to_update.order_status = data["order_status"]
        db.session.commit()
        return order_to_update, HTTPStatus.OK