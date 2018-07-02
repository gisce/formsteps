from formsteps.serializers import ButtonFormSchema
from formsteps.utils import make_form, make_errors_string
from marshmallow_jsonschema import JSONSchema


class ButtonForm(object):

    serializer = ButtonFormSchema

    def __init__(self, id, label, url, **kwargs):
        self.id = id
        self.label = label
        self.url = url
        self.primary = kwargs.pop('primary', False)
        self.disabled = kwargs.pop('disabled', False)
        self.safe_click = kwargs.pop('safe_click', False)
        self.submit = kwargs.pop('submit', False)

    def serialize(self):
        return self.serializer().dump(self).data


class FormStep(object):

    title = None
    serializer_class = None
    buttons = []
    step_url = None

    @property
    def serializer(self):
        return self.serializer_class()

    @property
    def schema(self):
        return JSONSchema().dump(self.serializer).data


    @classmethod
    def render_buttons(cls, buttons):
        return dict(
            (b.id, b.serialize()) for b in buttons
        )

    @property
    def definition(self):
        return {
            'result': {
                'schema': self.schema,
                'render': {
                    'step': self.step_url,
                    'title': self.title,
                    'errors': [],
                    'form': make_form(self.serializer),
                    'buttons': self.render_buttons(self.buttons)
                }
            }
        }
    
    def definition_with_errors(self, data):
        errors = self.validate(data)
        defintion = self.definition
        if errors:
            defintion['result']['render']['errors'] = errors
        return defintion

    def validate(self, data):
        errors = self.serializer.validate(data)
        return make_errors_string(errors, self.serializer_class.__name__)