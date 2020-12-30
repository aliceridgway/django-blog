
class CountryName():
    overrides = {
        'United States of America': 'USA',
        'United Kingdom': 'UK',
        'United Arab Emirates': 'UAE',
    }

    @classmethod
    def get_country_name(cls, name):
        if name in cls.overrides:
            return cls.overrides[name]
        else:
            return name
