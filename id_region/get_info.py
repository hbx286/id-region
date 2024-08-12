from typing import TypedDict, Annotated
from datetime import date, datetime

from .data import address_code
from .helper import check_is_valid, process_id_number, get_address_info


class RegionMessage(TypedDict):
    sex: Annotated[int, '0-unknow, 1-male, 2-female']
    birthday: Annotated[date, 'birthday']
    abandoned: Annotated[bool, 'is_abandoned: True if is_abandoned == yes else False']
    address: Annotated[str, 'region']
    country: Annotated[str, 'country']
    province: Annotated[str, 'province']
    city: Annotated[str, 'city']
    district: Annotated[str, 'district']


def get_id_info(id_number: str) -> RegionMessage:
    if check_is_valid(id_number):
        raise ValueError('Invalid ID number')

    code = process_id_number(id_number)
    birthday = datetime.strptime(code['birthday'], '%Y%m%d')
    info = get_address_info(code['address_code'], birthday)
    province, city, district = info.get('province', ''), info.get('city', ''), info.get('district', '')

    return {
        'sex': 2 if int(code['sequence_code']) % 2 == 0 else 1,
        'birthday': birthday,
        'abandoned': False if address_code.get(code['address_code']) else True,
        'address': f'{province}{city}{district}',
        'country': '中国',
        'province': province,
        'city': city,
        'district': district
    }


