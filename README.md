## example
```python
from id_region import get_id_info
id_info = get_id_info('110101199003075678')
'''
id_info is a dict
output just like:
{
    'sex': int,
    'birthday': date,
    'abandoned': False if address_code.get(code['address_code']) else True,
    'address': '',
    'country': '中国',
    'province': 'xx',
    'city': 'xx',
    'district': 'xxx'
}
'''
```