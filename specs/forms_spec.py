from mamba import *
from expects import *

from formsteps.serializers import ButtonFormSchema
from formsteps.forms import ButtonForm, FormStep
from marshmallow import Schema, fields


with description('A Form Step'):
    with before.each as self:
        class CustomFormStep1Schema(Schema):
            name = fields.String(
                title='Name',
                required=True,
                form={
                    'placeholder': 'Your Name'
                }
            )

        class CustomFormStep1(FormStep):
            title = 'Step 1'
            serializer_class = CustomFormStep1Schema
            buttons = [ButtonForm('step2', 'Next', '/step/2')]
            step_url = '/step/1'

        self.formstep1 = CustomFormStep1()
    with it('should render the buttons'):
        buttons = [
            ButtonForm('id1', 'Test Id', '/test/1'),
            ButtonForm(
                'id2', 'Test Id', '/test/2', primary=True, disabled=True,
                safe_click=True, submit=True)
        ]
        render_buttons = FormStep.render_buttons(buttons)
        expect(render_buttons).to(equal({
            'id1': {
                    'primary': False,
                    'disabled': False,
                    'safeClick': False,
                    'submit': False,
                    'label': 'Test Id',
                    'url': '/test/1'
                },
                'id2': {
                    'primary': True,
                    'disabled': True,
                    'safeClick': True,
                    'submit': True,
                    'label': 'Test Id',
                    'url': '/test/2'
                }
        }))
    with it('should have a title property'):
        required_properties = [
            'title',
            'serializer_class',
            'buttons',
            'serializer',
            'schema',
        ]
        expect(FormStep).to(have_properties(*required_properties))

    with it('should validate data'):
        result = self.formstep1.validate({'name': None})
        expect(result).to(equal(
            {'CustomFormStep1Schema.name': ['Field may not be null.']}
        ))

    with description('should return the definition'):
        with before.each as self:
            self.expected_definition = {
                'result': {
                    'schema': {
                        '$ref': '#/definitions/CustomFormStep1Schema',
                        'definitions': {
                            'CustomFormStep1Schema': {
                                'properties': {
                                    'name': {
                                        'type': 'string',
                                        'title': 'Name',
                                        'form': {
                                            'placeholder': 'Your Name'
                                        }
                                    }
                                },
                                'required': [
                                    'name'
                                ],
                                'type': 'object'
                            }
                        }
                    },
                    'render': {
                        'step': '/step/1',
                        'title': 'Step 1',
                        'errors': [],
                        'form': [
                            {
                                'key': 'CustomFormStep1Schema.name',
                                'placeholder': 'Your Name'
                            }
                        ],
                        'buttons': {
                            'step2': {
                                'disabled': False,
                                'label': 'Next',
                                'primary': False,
                                'safeClick': False,
                                'submit': False,
                                'url': '/step/2'
                            }
                        },
                    },
                }
            }
        with context('whitout errors'):
            with it('should return definition and empty errors'):
                expected = self.expected_definition
                expect(self.formstep1.definition).to(equal(expected))
        with context('with errors'):
            with it('should return definition and errors'):
                expected = self.expected_definition
                expected['result']['render']['errors'] = {
                    'CustomFormStep1Schema.name': ['Field may not be null.']
                }
                expect(self.formstep1.definition_with_errors({'name': None})).to(equal(
                    expected
                ))