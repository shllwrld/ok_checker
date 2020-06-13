from ok_checker import check_login


def test():
    result = check_login('test@test.com')
    assert result.get('masked_phone') == '7916233****'
    assert result.get('masked_email') == 'te**@test.com'
    assert result.get('masked_name') == 'Григорий Ж*****'
    assert result.get('profile_registred') == 'Профиль создан 23 ноября 2014'
    assert result.get('profile_info')


if __name__ == '__main__':
    test()
