from marshmallow import Schema, fields


class ButtonFormSchema(Schema):
    label = fields.String(required=True)
    url = fields.String(required=True)
    primary = fields.Boolean(default=False)
    disabled = fields.Boolean(default=False)
    safe_click = fields.Boolean(default=False, dump_to="safeClick")
    submit = fields.Boolean(default=False)