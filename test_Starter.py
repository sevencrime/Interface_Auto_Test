
import pytest

@pytest.mark.usefixtures('te', 'test_cases')
class TestStarter(object):

    def test_start(self):
        pytest.skip('此为测试启动方法, 不执行')

