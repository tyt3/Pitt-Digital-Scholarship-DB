from flask_marshmallow import Marshmallow


# Create marshmallow object
ma = Marshmallow()


"""Schema Classes"""
class AddressSchema(ma.Schema):
    class Meta:
        fields = ('address_id', 'building_name', 'room_number', 'street_address', 
                 'address_2', 'city', 'state', 'zipcode', 'campus', 'date_added')

address_schema = AddressSchema()
addresses_schema = AddressSchema(many=True)


class PersonSchema(ma.Schema):
    class Meta:
        fields = ('person_id', 'public_id', 'first_name', 'last_name', 'title', 
                 'pronouns', 'email', 'web_address', 'phone', 'scheduler_address', 
                 'preferred_contact', 'support_type', 'bio', 'date_added', 
                 'last_modified', 'notes')

person_schema = PersonSchema()
people_schema = PersonSchema(many=True)


class UnitSchema(ma.Schema):
    class Meta:
        fields = ('unit_id', 'public_id', 'unit_name', 'unit_type', 'email', 
                  'phone', 'other_contact', 'preferred_contact', 'web_address', 
                  'description', 'date_added', 'last_modified')

unit_schema = UnitSchema()
units_schema = UnitSchema(many=True)


class FundingSchema(ma.Schema):
    class Meta:
        fields = ('funding_id', 'public_id', 'funding_name', 'funding_type',
                  'payment_type', 'payment_amount', 'payment_frequency', 'amount', 
                  'career_level', 'duration', 'frequency', 'web_address', 
                  'last_modified', 'notes', 'date_added')

funding_schema = FundingSchema()
fundings_schema = FundingSchema(many=True)
