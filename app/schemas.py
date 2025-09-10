def get_ma():
    from app import ma
    return ma

from app.models import Customer, ServiceTicket, ServiceMechanic, Mechanic

class CustomerSchema(get_ma().SQLAlchemySchema):
    class Meta:
        model = Customer
    id = get_ma().auto_field()
    name = get_ma().auto_field()
    email = get_ma().auto_field()
    phone = get_ma().auto_field()

class ServiceTicketSchema(get_ma().SQLAlchemySchema):
    class Meta:
        model = ServiceTicket
    id = get_ma().auto_field()
    vin = get_ma().auto_field()
    service_date = get_ma().auto_field()
    service_description = get_ma().auto_field()
    customer_id = get_ma().auto_field()

class ServiceMechanicSchema(get_ma().SQLAlchemySchema):
    class Meta:
        model = ServiceMechanic
    ticket_id = get_ma().auto_field()
    mechanic_name = get_ma().auto_field()

class MechanicSchema(get_ma().SQLAlchemySchema):
    class Meta:
        model = Mechanic
    id = get_ma().auto_field()
    name = get_ma().auto_field()
    salary = get_ma().auto_field()
    phone = get_ma().auto_field()
    email = get_ma().auto_field()

from app import ma
from app.models import Customer

class LoginSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
    email = ma.auto_field()
    password = ma.auto_field()