from mamba import *
from expects import *
from formsteps.utils import *


with description('An structure of errors'):
    with it('should be flatted to a simple dict'):
        errors_struct = {
            'owner': {
                'vat': ['not valid'],
                'type': ['required']
            },
            'owner_address': {
                'municipi': ['required']
            },
            'ref': ['not valid']
        }
        errors = make_errors_string(errors_struct, 'FormStep1')
        errors_string_keys = {
            'FormStep1.owner.vat': ['not valid'],
            'FormStep1.owner.type': ['required'],
            'FormStep1.owner_address.municipi': ['required'],
            'FormStep1.ref': ['not valid']
        }
        expect(errors).to(equal(errors_string_keys))


with description('A list of dictionaries'):
    with it('should be converted to an enum'):
        result = [
            {
                'id': 1,
                'name': 'Item 1',
                'other': 'Other 1'
            },
            {
                'id': 2,
                'name': 'Item 2',
                'other': 'Other 2'
            }
        ]
        enums_result = make_enums(result, 'id', 'name')
        enums = {
            'enum': [1, 2],
            'enumNames': ['Item 1', 'Item 2']
        }
        expect(enums_result).to(equal(enums))