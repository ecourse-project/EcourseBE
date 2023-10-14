from apps.system.model_choices import import_db_model
import json

def apply_action(model, data: dict, action: str, extra_data, extra_action: str = "", ):
    if action == "all":
        data = model.objects.all()
    elif action == "first":
        data = model.objects.first()
    elif action == "last":
        data = model.objects.last()
    elif action == "get":
        data = model.objects.get(**data)
    elif action == "filter":
        data = model.objects.filter(**data)
    elif action == "create":
        data = model.objects.create(**data)
    else:
        data = ""

    if extra_action and data:
        if extra_action == "count":
            return data.count()
        # elif extra_action == "values_list":
        #     return data.values_list("name", flat=True)
        elif extra_action == "delete":
            data.delete()
            return data

    return data


def import_database(json_file):
    data = json.load(open(json_file, "r"))

    choices = import_db_model

    for key, model in choices.items():
        items = [item for item in data if item["model"] == key]
        field_names = [field.name for field in model._meta.get_fields()]
        model_field = set(items[0]["fields"]).intersection(set(field_names))

        m2m_field = []
        json_field = []
        fk_key_field = []
        for field in model_field:
            field_type = model._meta.get_field(field).get_internal_type()
            if field_type == "ManyToManyField":
                m2m_field.append(field)
            elif field_type == "ArrayField" or field_type == "JSONField":
                json_field.append(field)
            elif field_type == "ForeignKey" or field_type == "OneToOneField":
                fk_key_field.append(field)

        for item in items:
            for field in json_field:
                value = item["fields"][field]
                item["fields"][field] = json.loads(value) if value is not None else value
            for field in fk_key_field:
                item["fields"][field + "_id"] = item["fields"].pop(field)

        if m2m_field:
            for item in items:
                m2m_value = {}
                fields = item["fields"]
                for field in m2m_field:
                    m2m_value[field] = fields.pop(field)
                record = model.objects.create(pk=item["pk"], **fields)
                for key, val in m2m_value.items():
                    exec(f"record.{key}.set({val})")

        else:
            obj_create = [model(pk=dt["pk"], **dt["fields"]) for dt in items]
            model.objects.bulk_create(obj_create)
