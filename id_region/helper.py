from typing import List, Dict
from datetime import date

from .data import address_code_timeline, additional_address_code_timeline


def check_is_valid(id_number: str, country: str = 'zh') -> bool:
    id_number = str(id_number) if not isinstance(id_number, str) else id_number
    return True if len(id_number) == 18 or len(id_number) == 15 else False


def process_id_number(id_number: str) -> Dict:
    id_number = id_number.upper()
    if len(id_number) == 15:
        code = {
            'address_code': id_number[:6],
            'birthday': id_number[6:14],
            'sequence_code': id_number[14:17],
            'check_bit': id_number[-1]
        }
    else:
        code = {
            'address_code': id_number[:6],
            'birthday': f'19{id_number[6:12]}',
            'sequence_code': id_number[12:15],
            'check_bit': ''
        }
    return code


def get_address_info(address_code: str, birthday: date) -> Dict[str, str]:
    def _handle_timeline(timeline: List[Dict]) -> str:
        address = ''
        if timeline:
            for item in timeline:
                start_year = 0 if item['start_year'] == '' else item['start_year']
                end_year = 9999 if item['end_year'] == '' else item['end_year']
                if end_year >= birthday.year >= start_year:
                    address = item['address']
            if not address:
                address = timeline[0]['address']
        else:
            # 修复 \d\d\d\d01、\d\d\d\d02、\d\d\d\d11 和 \d\d\d\d20 的历史遗留问题
            # 以上四种地址码，现实身份证真实存在，但民政部历年公布的官方地址码中可能没有查询到
            # 如：440401 450111 等
            # 所以这里需要特殊处理
            # 1980年、1982年版本中，未有制定省辖市市辖区的代码，所有带县的省辖市给予“××××20”的“市区”代码。
            # 1984年版本开始对地级市（前称省辖市）市辖区制定代码，其中“××××01”表示市辖区的汇总码，同时撤销“××××20”的“市区”代码（追溯至1983年）。
            # 1984年版本的市辖区代码分为城区和郊区两类，城区由“××××02”开始排起，郊区由“××××11”开始排起，后来版本已不再采用此方式，已制定的代码继续沿用。
            suffixes = address_code[4:6]
            if suffixes == '01':
                address = '市辖区'
            if suffixes == '20':
                address = '市区'
            if suffixes == '02':
                address = '城区'
            if suffixes == '11':
                address = '郊区'
        return address

    province_code, city_code, = f'{address_code[:2]}0000', f'{address_code[0:4]}00'

    province_timeline = address_code_timeline.get(province_code, '')
    if not province_timeline:
        province_timeline = additional_address_code_timeline.get(province_code, '')

    city, district = '', ''
    if not address_code.startswith('8'):
        city_timeline = address_code_timeline.get(city_code, '')
        if not city_timeline:
            city_timeline = additional_address_code_timeline.get(city_code, '')

        district_timeline = address_code_timeline.get(address_code, '')
        if not district_timeline:
            district_timeline = additional_address_code_timeline.get(address_code, '')

        city = _handle_timeline(city_timeline)
        district = _handle_timeline(district_timeline)

    info = {
        'province': _handle_timeline(province_timeline),
        'city': city,
        'district': district
    }

    return info
