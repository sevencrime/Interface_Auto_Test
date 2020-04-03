import pytest
from get_apiData import get_api_key_data

API_KEY_DATA = get_api_key_data()


def test_case(name, phone, age):
    param = {}
    param['name'] = name
    param['phone'] = phone
    param['age'] = age

    print(param)



if __name__ == '__main__':
    pytest.main(["-s", "-v", "test_autoapi.py::test_case", "--pdb"])