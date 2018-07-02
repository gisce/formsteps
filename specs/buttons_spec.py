from mamba import *
from expects import *

from formsteps.serializers import ButtonFormSchema
from formsteps.forms import ButtonForm


with description('Form buttons'):

    with before.each as self:
        self.basic_button = ButtonForm(
            'id1', 'Test Id', '/test/1'
        )
        self.properties_button = ButtonForm(
            'id2', 'Test Id', '/test/2',
            primary=True,
            disabled=True,
            safe_click=True,
            submit=True
        )
    
    with it('should have all required properties'):
        req_properties = [
            'id',
            'primary',
            'disabled',
            'safe_click',
            'submit',
            'label',
            'url'
        ]
        b = self.basic_button
        expect(b).to(have_properties(*req_properties))

    with description('when serializing'):
        with context('if is a basic button'):
            with it('should complain the schema'):
                b = self.basic_button
                expect(b.serialize()).to(equal({
                        'primary': False,
                        'disabled': False,
                        'safeClick': False,
                        'submit': False,
                        'label': 'Test Id',
                        'url': '/test/1'
                }))
        with context('if is a properties button'):
            with it('should complain the schema'):
                b = self.properties_button
                expect(b.serialize()).to(equal({
                    'primary': True,
                    'disabled': True,
                    'safeClick': True,
                    'submit': True,
                    'label': 'Test Id',
                    'url': '/test/2'
                }))

        with it('should allow custom serializer'):

            from marshmallow import post_dump
            class ButtonFormSchemaCustom(ButtonFormSchema):
                @post_dump(pass_many=False)
                def force_url_prefix(self, data):
                    if data.get('url'):
                        data['url'] = '/api/v1{}'.format(data['url'])

            b = self.basic_button
            b.serializer = ButtonFormSchemaCustom
            expect(b.serialize()).to(equal({
                'primary': False,
                'disabled': False,
                'safeClick': False,
                'submit': False,
                'label': 'Test Id',
                'url': '/api/v1/test/1'
            }))

