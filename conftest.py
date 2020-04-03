

import pytest
from get_apiData import get_api_key_data

API_KEY_DATA = get_api_key_data()
print(API_KEY_DATA)

def pytest_generate_tests(metafunc):

    if 'name' in metafunc.fixturenames:
        for k, v in API_KEY_DATA.items():
            metafunc.parametrize(k, v)


@pytest.fixture(scope="session")
def test_cases():
    content = """
    import allure

    from conftest import CaseMetaClass

    @allure.feature('{}接口测试({}项目)')
    class Test{}API(object, metaclass=CaseMetaClass):

        test_cases_data = {}
    """





