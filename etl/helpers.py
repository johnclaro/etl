def camel_to_snake(s):
    """
    name = field['name']
    field_type = field['type']
    if field_type in ['esriFieldTypeDate', 'esriFieldTypeOID']:
        django_field = 'models.DateTimeField()'
    elif field_type == 'esriFieldTypeInteger':
        django_field = 'models.IntegerField()'

    from etl.helpers import camel_to_snake
    print(camel_to_snake(name), '=', django_field)

    or

    for field in response['fields']:
        name = field['name']
        from etl.helpers import camel_to_snake
        print(f'{name},')
    """
    return ''.join(
        ['_' + c.lower() if c.isupper() else c for c in s]
    ).lstrip('_')
