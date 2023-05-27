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

