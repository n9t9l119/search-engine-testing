from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from TestConfig import TestConfig


class BasePage:
    def __init__(self, browser, base_url=''):
        self.browser = browser
        self.base_url = base_url

    def open_base_url(self):
        return self.browser.get(self.base_url)

    def find_element(self, locator, time=10):
        return WebDriverWait(self.browser, time).until(EC.presence_of_element_located(locator),
                                                       message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.browser, time).until(EC.presence_of_all_elements_located(locator),
                                                       message=f"Can't find element by locator {locator}")


class SearchPage(BasePage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)

    def search(self, search_button_locator=(), phrase=TestConfig.REQUEST):
        search_input = self.browser.find_element(*TestConfig.search_page_input_locator)
        search_input.clear()
        search_input.send_keys(phrase)

        if search_button_locator == () or search_button_locator[1] == "*":
            search_input.send_keys(Keys.ENTER)
        else:
            self.browser.find_element(*search_button_locator).click()


class ResultPage(SearchPage):
    def __init__(self, browser, base_url):
        super().__init__(browser, base_url)

    def get_results_count(self, locator=TestConfig.result_list_locator):
        return len(self.browser.find_elements(*locator))

    def get_search_input_value(self, input_locator):
        search_input = self.browser.find_element(*input_locator)
        return search_input.get_attribute('value')

    def get_request_presence_in_results(self, locator=TestConfig.result_relevance_locator):
        search_results = self.find_elements(locator)
        search_results = [link for link in search_results if TestConfig.REQUEST in link.text]
        return search_results
