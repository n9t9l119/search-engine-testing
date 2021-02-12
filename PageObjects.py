from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver, base_url=''):
        self.driver = driver
        self.base_url = base_url

    def open_base_url(self):
        return self.driver.get(self.base_url)

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    # def get_title(self):
    #     return self.driver.title




class SearchPage(BasePage):
    SEARCH_INPUT = (By.ID, 'text')

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def search(self, phrase, search_button_locator=()):
        search_input = self.driver.find_element(*self.SEARCH_INPUT)
        search_input.clear()
        search_input.send_keys(phrase)
        if search_button_locator == ():
            search_input.send_keys(Keys.ENTER)
        else:
            self.driver.find_element(*search_button_locator).click()


class ResultPage(BasePage):
    inpute_locator = (By.ID, 'search_form_input')

    def __init__(self, driver, base_url):
        super().__init__(driver, base_url)

    def get_results_count_by_locator(self, locator):
        return len(self.browser.find_elements(*locator))

    def get_search_input_value(self):
        search_input = self.browser.find_element(*self.inpute_locator)
        return search_input.get_attribute('value')
