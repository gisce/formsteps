import copy
from marshmallow.fields import Nested


def make_form(obj, prefix=None):
    items = []
    form_map_key = {}
    if prefix is None:
        prefix = obj.__class__.__name__
    for fname, ftype in obj.fields.items():
        if ftype.dump_only:
            continue
        if isinstance(ftype, Nested):
            nested_prefix = '{}.{}'.format(
                prefix, fname
            )
            items.extend(make_form(ftype.schema, nested_prefix))
        else:
            key = '{}.{}'.format(prefix, fname)
            form = copy.deepcopy(ftype.metadata.get('form', {}))
            form_map_key[fname] = key
            if form:
                item = {'key': key}
                condition = form.pop('condition', None)
                if condition:
                    item['condition'] = 'model.{}.{}'.format(
                            prefix, condition
                        )
                item.update(dict((k, v) for k, v in form.items()))
                items.append(item)
            else:
                items.append(key)
    for item in items:
        if isinstance(item, dict):
            for k, v in item.get('onChange', {}).items():
                item['onChange'][k] = v.format(form=form_map_key)
    return items


def make_errors_string(errors, prefix=None):
    res = {}
    if prefix is None:
        prefix = ''
    for k, v in errors.items():
        if prefix:
            key = '{}.{}'.format(prefix, k)
        else:
            key = k
        if isinstance(v, dict):
            rec_errors = make_errors_string(v, prefix=key)
            res.update(rec_errors)
        else:
            res[key] = v
    return res


def make_enums(data, key, name_key=None):
    enum = []
    enum_names = []
    for element in data:
        enum.append(element[key])
        if name_key:
            enum_names.append(element[name_key])
    res = {'enum': enum}
    if enum_names:
        res['enumNames'] = enum_names
    return res