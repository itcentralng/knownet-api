from app import ma
from app.search.model import *

class SearchSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Search
        exclude = ('is_deleted',)