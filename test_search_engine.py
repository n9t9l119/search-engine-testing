import pytest
import allure
from allure_commons.types import AttachmentType

from TestConfig import TestConfig


@allure.feature('Start testing the script')
@pytest.mark.usefixtures('browser', 'search_page', 'result_page')
@pytest.mark.incremental
class TestUserHandling:
    @allure.story('Opening the start page')
    @allure.link(name="Start page", url=TestConfig.SEARCH_ENGINE)
    def test_open_start_page(self, browser, search_page):
        search_page.open_base_url()
        with allure.step('Making a screenshot'):
            allure.attach(browser.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)

    @allure.story('Check that there was no redirect')
    def test_being_on_desired_page(self, browser):
        with allure.step('Make sure that we are on the right link'):
            assert browser.current_url == TestConfig.SEARCH_ENGINE, "current url not similar to config search engine"
        with allure.step(f'Check that the title contains the text "{TestConfig.TEXT_IN_TITLE}"'):
            assert TestConfig.TEXT_IN_TITLE in browser.title, \
                f"Config TEXT_IN_TITLE {TestConfig.TEXT_IN_TITLE} not in {browser.title}"

    @allure.story('Sending a request')
    def test_send_query(self, browser, search_page):
        search_page.search(search_button_locator=TestConfig.search_button_locator)
        with allure.step('Making a screenshot'):
            allure.attach(browser.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)

    @allure.story('Check that there was no loss of the input and the entered data')
    def test_valid_input_presence(self, result_page):
        assert bool(result_page.find_element(TestConfig.result_page_input_locator)), \
            f"element by locator {TestConfig.result_page_input_locator} not found"

    @allure.story(
        'If the search engine under test is Russian yandex'
        'then we check the correctness of the generated link,'
        'which we clicked on')
    @pytest.mark.skipif(TestConfig.SEARCH_ENGINE != "https://yandex.ru/", reason="Test only for yandex.ru")
    def test_current_url(self, browser):
        assert browser.current_url == "https://yandex.ru/search/?lr=2&text=" + TestConfig.REQUEST.replace(' ', '%20'), \
            f"current link {browser.current_url} not correct"

    @allure.story('Check the correctness of the results obtained')
    def test_search_results_correctness(self, result_page):
        with allure.step('Check the availability of search results'):
            assert result_page.get_results_count() > 0, f"there is no results by xpath {TestConfig.result_list_locator}"

        with allure.step('Check the presence of the query text in the search results output'):
            assert len(result_page.get_request_presence_in_results()) > 0, \
                f"there is no results by locator {TestConfig.result_relevance_locator}"

        with allure.step('Check the presence of the required site in the search results'):
            assert result_page.get_results_count(TestConfig.required_site_locator) > 0, \
                f"there is no results by locator {TestConfig.required_site_locator}"

    @allure.link(name="The link you need to be on", url=TestConfig.LINK_TO_FIND)
    @allure.story('Check the correctness of the click on the link')
    def test_open_link(self, browser, result_page):
        with allure.step('Click on the link'):
            result_page.find_element(TestConfig.required_site_link_locator).click()
        with allure.step('Go to the new tab that opens'):
            browser.switch_to.window(browser.window_handles[-1])

    @allure.story('Check that there was no redirect')
    def test_opened_site_url(self, browser, result_page):
        with allure.step('Make sure that we are on the right link'):
            assert browser.current_url == TestConfig.LINK_TO_FIND, \
                f" Current url {browser.current_url} not equal to LINK_TO_FIND in config {TestConfig.LINK_TO_FIND}"

    @allure.story('Check the availability of the necessary content')
    def test_opened_site_content(self, browser, result_page):
        with allure.step('Making a screenshot'):
            allure.attach(browser.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)
        search_results = result_page.find_elements(TestConfig.required_site_content_locator)
        assert len(search_results) > 0, \
            f"there is no results by locator {TestConfig.required_site_link_locator}"
