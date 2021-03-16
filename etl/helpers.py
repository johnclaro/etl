def hse_convert_fields_for_django(response):
    for field in response['fields']:
        name = field['name'].lower()
        field_type = field['type']
        if field_type in ['esriFieldTypeDate']:
            django_field = 'models.DateField()'
        elif field_type in ['esriFieldTypeInteger', 'esriFieldTypeOID']:
            django_field = 'models.IntegerField()'
        elif field_type == 'esriFieldTypeDouble':
            django_field = 'models.FloatField()'
        elif field_type == 'esriFieldTypeString':
            django_field = 'models.CharField(max_length=255)'
        else:
            print('[!] Did not get field type of', field_type)

        print(name, '=', django_field)
