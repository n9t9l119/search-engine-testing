import time
import pytest

from TestConfig import TestConfig


@pytest.mark.usefixtures('browser', 'yandex_search_page', 'yandex_result_page')
@pytest.mark.incremental
class TestUserHandling:
    def test_open_start_page(self, browser, yandex_search_page):
        yandex_search_page.open_base_url()

    def test_being_on_desired_page(self, browser):
        assert browser.current_url == TestConfig.SEARCH_ENGINE
        assert "Яндекс" in browser.title

    def test_presence_of_DOM_search_elems(self, yandex_search_page):
        assert bool(yandex_search_page.find_element(TestConfig.search_container_locator))
        assert bool(yandex_search_page.find_element(TestConfig.search_page_input_locator))
        assert bool(yandex_search_page.find_elements(TestConfig.search_button_locator))

    def test_send_query(self, yandex_search_page):
        yandex_search_page.search(search_button_locator=TestConfig.search_button_locator)
        time.sleep(1)

    def test_request_correctness(self, yandex_result_page):
        current_inpute_value = yandex_result_page.get_search_input_value(TestConfig.result_page_input_locator)
        assert current_inpute_value == TestConfig.REQUEST

    def test_search_results_correctness(self, yandex_result_page):
        assert yandex_result_page.get_results_count() > 0

        assert len(yandex_result_page.get_request_presence_in_results()) > 0

        assert yandex_result_page.get_results_count(TestConfig.required_site_locator) > 0

    def test_find_link(self, yandex_result_page):
        assert bool(yandex_result_page.find_element(TestConfig.required_site_link_locator))

    def test_open_link(self, browser, yandex_result_page):
        yandex_result_page.find_element(TestConfig.required_site_link_locator).click()
        browser.switch_to.window(browser.window_handles[-1])
        assert browser.current_url == TestConfig.LINK_TO_FIND

    def test_opened_link(self, yandex_result_page):
        search_results = yandex_result_page.find_elements(TestConfig.required_site_content_locator)
        assert len(search_results) > 0
