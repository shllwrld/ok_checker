from ok_checker import check_login


def test():
    result = check_login('test@mail.ru')
    assert result.get('masked_phone') == '99292984****'
    assert result.get('masked_email') == 'te**@mail.ru'
    assert result.get('masked_name') == 'Ховар Х******'
    assert result.get('profile_registred') == 'Профиль создан 10 декабря 2014'
    assert result.get('profile_info') == "47 лет, Худжанд"


if __name__ == '__main__':
    test()
