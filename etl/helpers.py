def convert_fields_for_django(response):
    for field in response['fields']:
        name = field['name']
        field_type = field['type']
        if field_type in ['esriFieldTypeDate', 'esriFieldTypeOID']:
            django_field = 'models.DateTimeField()'
        elif field_type == 'esriFieldTypeInteger':
            django_field = 'models.IntegerField()'

        print(name, '=', django_field)
