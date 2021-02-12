import time

import pytest

from TestConfig import TestConfig


@pytest.mark.incremental
class TestUserHandling:
    def test_open_start_page(self, browser, yandex_search_page):
        yandex_search_page.open_base_url()

        assert "Яндекс" in browser.title
        assert browser.current_url == TestConfig.SEARCH_ENGINE
        # ! assert bool(yandex_search_page.find_element(TestConfig.search_container_locator))
        assert bool(yandex_search_page.find_element(TestConfig.search_page_input_locator))

        assert bool(yandex_search_page.find_elements(TestConfig.search_button_locator))

    # def test_find_container__search(browser):
    #     page = BasePage(browser)
    #     page.find_element((By.ID, "text"), 10)
    #     assert bool(browser.find_element_by_class_name("container__search"))
    #
    #
    # #
    # def test_find_button(browser):
    #     assert bool(browser.find_element_by_class_name("button"))
    #
    #
    # def test_find_inpute(browser):
    #     assert bool(browser.find_element_by_id("text"))
    #
    #
    # def test_check_current_url(browser):
    #     assert browser.current_url == TestConfig.SEARCH_ENGINE

    ###############################

    def test_send_query(self, browser, yandex_search_page):
        yandex_search_page.search(TestConfig.REQUEST)
        assert yandex_search_page.find_element(TestConfig.result_page_input_locator).get_property(
            "value") == TestConfig.REQUEST
        link_by_enter = browser.current_url
        yandex_search_page.open_base_url()
        yandex_search_page.search(TestConfig.REQUEST, TestConfig.search_button_locator)
        time.sleep(1)
        elem = yandex_search_page.find_element(TestConfig.result_page_input_locator)
        assert elem.get_property("value") == TestConfig.REQUEST
        assert link_by_enter != browser.current_url

    def test_search_results(self, yandex_search_page):
        assert len(yandex_search_page.find_elements(TestConfig.result_list_locator)) > 0

        search_results = yandex_search_page.find_elements(TestConfig.result_relevance_locator)
        search_results = [link for link in search_results if TestConfig.REQUEST in link.text]

        assert len(search_results) > 0

        search_results = yandex_search_page.find_elements(TestConfig.required_site_locator)
        assert len(search_results) > 0

    # def test_check_count_of_links(yandex_search_page):
    #     # yandex_search_page = SearchPage(browser, TestConfig.SEARCH_ENGINE)
    #     assert len(yandex_search_page.find_elements((By.CSS_SELECTOR, 'ul > .serp-item'))) > 0
    #
    #
    # def test_search_results(yandex_search_page):
    #     xpath = "//*[contains(text(),'ViPNet')]/parent::div"
    #
    #     search_results = yandex_search_page.find_elements((By.XPATH, xpath))
    #     search_results = [link for link in search_results if TestConfig.REQUEST in link.text]
    #
    #     assert len(search_results) > 0
    #
    #
    # def test_link_in_search_results(yandex_search_page):
    #     xpath = "//a[contains(@href,'infotecs.ru')]"
    #     search_results = yandex_search_page.find_elements((By.XPATH, xpath))
    #     assert len(search_results) > 0

    # #############################################################
    #
    def test_find_link(self, browser, yandex_search_page):
        link = yandex_search_page.find_element(TestConfig.required_site_link_locator)
        assert bool(link)
        link.click()
        browser.switch_to.window(browser.window_handles[-1])
        assert browser.current_url == TestConfig.LINK_TO_FIND

    # #############################################################
    #
    def test_opened_link(self, yandex_search_page):
        search_results = yandex_search_page.find_elements(TestConfig.required_site_content_locator)
        assert len(search_results) > 0
