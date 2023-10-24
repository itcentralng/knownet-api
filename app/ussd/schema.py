from app import ma
from app.ussd.model import *

class UssdSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ussd
        exclude = ('is_deleted',)