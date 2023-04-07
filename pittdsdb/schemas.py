from flask_marshmallow import Marshmallow


# Create marshmallow object
ma = Marshmallow()


"""Schema Classes"""
class AddressSchema(ma.Schema):
    class Meta:
        fields = ('building_name', 'room_number', 'address_1', 
                 'address_2', 'address_3', 'city', 'state', 'zipcode', 'campus')

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


class PersonSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'title', 'pronouns', 'email',
                 'web_address', 'phone', 'scheduler_address', 
                 'preferred_contact', 'support_type', 'bio', 'added_by', 
                 'date_added', 'last_modified', 'notes')

person_schema = PersonSchema()
person_schema = PersonSchema(many=True)

