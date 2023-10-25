from typing import Dict
import subprocess
import json

from django.contrib.auth.models import Permission, ContentType

from apps.system.model_choices import import_db_model


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


def get_field_type(fields, model_class):
    m2m_field = []
    json_field = []
    array_field = []
    fk_key_field = []

    for field in fields:
        field_type = model_class._meta.get_field(field).get_internal_type()
        if field_type == "ManyToManyField":
            m2m_field.append(field)
        elif field_type == "JSONField":
            json_field.append(field)
        elif field_type == "ArrayField":
            array_field.append(field)
        elif field_type == "ForeignKey" or field_type == "OneToOneField":
            fk_key_field.append(field)

    return fk_key_field, m2m_field, array_field, json_field


def handle_data(data, model_name, model_class):
    res = {}

    items = [item for item in data if item["model"] == model_name]
    if not items:
        return

    all_fields_name = [field.name for field in model_class._meta.get_fields()]
    model_field = set(items[0]["fields"]).intersection(set(all_fields_name))
    fk_key_field, m2m_field, array_field, json_field = get_field_type(model_field, model_class)

    for item in items:
        pk = item["pk"]
        attr = item["fields"]
        m2m = {}
        for field in fk_key_field:
            attr[field + "_id"] = attr.pop(field)
        for field in m2m_field:
            m2m[field] = attr.pop(field)
        for field in array_field:
            attr[field] = json.loads(attr[field]) if isinstance(attr[field], str) else attr[field]
        for field in json_field:
            attr[field] = json.loads(attr[field]) if isinstance(attr[field], str) else attr[field]

        res[pk] = {
            "instance": model_class(pk=pk, **attr),
            "m2m": m2m
        }

    return res


def store_model_data(data: Dict, model_class):
    if not data:
        return

    model_class.objects.bulk_create([info["instance"] for info in data.values()])
    for info in data.values():
        instance = info["instance"]
        for m2m_field, val in info["m2m"].items():
            exec(f"instance.{m2m_field}.set({val})")


def import_database(json_file):
    data = json.load(open(json_file, "r"))
    choices = import_db_model

    Permission.objects.all().delete()
    ContentType.objects.all().delete()

    for key, model in choices.items():
        dict_data = handle_data(data, key, model)
        store_model_data(dict_data, model)
