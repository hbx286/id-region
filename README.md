## Installation
Create and activate a virtual environment and then install id_region
```shell
$ pip install id-region
```


## example
```python
from id_region import get_id_info

id_info = get_id_info('110101199003075678')
'''
id_info is a dict
output just like:
{
    'sex': 0-unknow, 1-male, 2-female,
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