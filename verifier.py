import json
from collections import OrderedDict
from slugify import slugify
from random import randint


class WorldDataVerifier(object):
    STATE_FIELDS = ['country', 'name']

    def __init__(self, update_file=False):
        self.update_file = update_file
        self.countries = self._load_data(key='countries')
        self.states = self._load_data(key='states')
        self.cities = self._load_data(key='cities')

    def _load_data(self, key):
        with open(f'data/{key}.json', 'r+') as f:
            data = json.load(f)
        return data

    def _sort(self, data):
        if isinstance(data, dict):
            return OrderedDict(sorted(data.items()))
        return data

    def _dump_data(self, key, data):
        sorted_data = self._sort(data)
        with open(f'data/{key}.json', 'w+') as f:
            json.dump(sorted_data, f, indent=4)

    def verify(self):
        self.verify_states()
        self.verify_cities()
        self.set_place()
        if self.update_file:
            self.update()

    def update(self):
        self._dump_data(key='countries', data=self.countries)
        self._dump_data(key='states', data=self.states)
        self._dump_data(key='cities', data=self.cities)

    def verify_states(self):
        for country in self.countries:
            if not self.states.get(country.get('code')):
                print(f'No state found for country "{country.get("name")}" and code "{country.get("code")}"')
        slugs = set()
        for country, states in self.states.items():
            print(f'Running for country {country}')
            for state in states:
                for field in self.STATE_FIELDS:
                    if not state.get(field):
                        print(f'Field {field} missing in State {state.get("name")}')
                slug_key = f'{state.get("country")} {state.get("name")}'
                slug = slugify(slug_key)
                if slug not in slugs:
                    state['slug'] = slug
                else:
                    state['slug'] = slugify(f'{slug_key} {randint(100, 10000)}')

    def verify_cities(self):
        for country in self.countries:
            if country['code'] == 'IN':
                self.verify_city_of_country(country)
                break

    def verify_city_of_country(self, country):
        country = country.get('code')
        states = self.states.get(country)
        states = {state.get('name').encode('utf-8') for state in states}
        cities = self.cities.get(country, [])
        if not cities:
            print(f'No city found for {country}')
        for city in cities:
            if city.get('state').encode('utf-8') not in states:
                print(
                    f'State {city.get("state")} for city {city.get("name")} and country {country} not found in states'
                )

    def set_place(self):
        places = self._load_data(key='places/PK')
        selected = []
        states = self.states.get('PK')
        state_slug = {state.get('name'): state.get('slug') for state in states}
        for place in places:
            place.pop('id')
            place.pop('objectID')
            slug_key = f'PK {place.get("name")} {place.get("state")} {randint(100, 10000)}'
            if place['name'] != 'Others':
                place['slug'] = slugify(slug_key)
                place['state'] = {
                    'slug': state_slug.get(place.get('state')),
                    'name': place.get('state')
                }
                selected.append(place)
        self._dump_data(key='places/PK-1', data=selected)


WorldDataVerifier(update_file=False).verify()