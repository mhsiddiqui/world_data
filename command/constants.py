class Fields(object):
    COUNTRY = [
        'code', 'code3', 'name', 'currency', 'currency_name', 'phone',
        'language_codes', 'currency_symbol'
    ]
    STATE = ['country', 'latitude', 'longitude', 'name', 'slug']
    CITY = ['state', 'latitude', 'longitude', 'name', 'slug']
    PLACE = ['city', 'latitude', 'longitude', 'name', 'slug', 'parent_place']
