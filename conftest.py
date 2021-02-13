import pytest
from selenium import webdriver
from configparser import ConfigParser
from typing import Dict, Tuple

from PageObjects import SearchPage, ResultPage
from TestConfig import TestConfig


@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    yield driver


@pytest.fixture(scope="session")
def yandex_search_page(browser):
    return SearchPage(browser, TestConfig.SEARCH_ENGINE)


@pytest.fixture(scope="session")
def yandex_result_page(browser):
    return ResultPage(browser, TestConfig.SEARCH_ENGINE)


#  Следующий код взят с ресурса https://docs.pytest.org/en/stable/example/simple.html
#  Строка 40 была изменена для продолжения тестирования в случае, когда какой-либо тест
#  пропускается

# сохраняем историю падений в разрезе имен классов и индексов в параметризации (если она используется)


# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None and not call.excinfo.errisinstance(pytest.skip.Exception):
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))
