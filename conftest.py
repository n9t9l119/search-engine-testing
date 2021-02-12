import pytest
from selenium import webdriver
from PageObjects import BasePage, SearchPage, ResultPage
from TestConfig import TestConfig

# сохраняем историю падений в разрезе имен классов и индексов в параметризации (если она используется)
_test_failed_incremental: [str, [[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # используется маркер incremental
        if call.excinfo is not None:
            # тест упал
            # извлекаем из теста имя класса
            cls_name = str(item.cls)
            # извлекаем индексы теста (если вместе с  incremental используется параметризация)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # извлекаем имя тестовой функции
            test_name = item.originalname or item.name
            # сохраняем в _test_failed_incremental оригинальное имя упавшего теста
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # извлекаем из теста имя класса
        cls_name = str(item.cls)
        # проверяем, падал ли предыдущий тест на этом классе
        if cls_name in _test_failed_incremental:
            # извлекаем индексы теста (если вместе с  incremental используется параметризация)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # извлекаем имя первой тестовой функции, которая должна упасть для этого имени класса и индекса
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # если нашли такое имя, значит, тест падал для такой комбинации класса & фукнкции
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))




@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome()
    return driver


@pytest.fixture(scope="session")
def yandex_search_page(browser):
    return SearchPage(browser, TestConfig.SEARCH_ENGINE)

