import json
from .constants import Fields
from collections import OrderedDict
from slugify import slugify
from random import randint


class WorldDataVerifier(object):
    STATE_FIELDS = ['country', 'name']

    def __init__(self, country, data, save=False):
        self.update_file = save
        self.country = country
        self.data = data
        # self.countries = self._load_data(key='countries')
        # self.states = self._load_data(key='states')
        # self.cities = self._load_data(key='cities')
        # self.places = self._load_data(key='places/PK')

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
        if self.data == 'state':
            self.verify_states()
        if self.data == 'city':
            self.verify_cities()
        if self.data == 'place':
            self.set_place()
        if self.update_file:
            self.update()

    def update(self):
        # self._dump_data(key='countries', data=self.countries)
        # self._dump_data(key='states', data=self.states)
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
            if country['code'] == 'PK':
                self.verify_city_of_country(country)
                break

    def verify_city_of_country(self, country):
        country = country.get('code')
        states = self.states.get(country)
        states = {state.get('name'): state for state in states}
        cities = self.cities.get(country, [])
        if not cities:
            print(f'No city found for {country}')
        for city in cities:
            if city.get('state').encode('utf-8') not in states:
                print(
                    f'State {city.get("state")} for city {city.get("name")} and country {country} not found in states'
                )
            slug_key = f'{country} {city.get("state")} {city.get("name")} {randint(100, 1000)}'
            city['slug'] = slugify(slug_key)
            city['state'] = {
                'slug': states.get(city.get('state')).get('slug'),
                'name': city.get('state')
            }

    def set_place(self):
        selected = []
        states = self.states.get('PK')
        state_slug = {state.get('name'): state.get('slug') for state in states}
        for place in self.places:
            place.pop('id')
            place.pop('objectID')
            slug_key = f'PK {place.get("name")} {place.get("state")} {randint(100, 10000)}'
            place['slug'] = slugify(slug_key)
            place['state'] = {
                'slug': state_slug.get(place.get('state')),
                'name': place.get('state')
            }
            selected.append(place)
        self.places = selected


WorldDataVerifier(update_file=True).verify()