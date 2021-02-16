from selenium.webdriver.common.by import By


class TestConfig:
    REQUEST = "ViPNet Coordinator HW5000"
    SEARCH_ENGINE = "https://yandex.ru/"
    LINK_TO_FIND = "https://infotecs.ru/upload/iblock/db0/ViPNet_Coordinator_HW_5000_web_july_2018.pdf"
    TEXT_IN_TITLE = "Яндекс"

    search_page_input_locator = (By.XPATH, "//*[@id='text']")
    search_button_locator = (By.XPATH, "//div[@class = 'search2__button']/button[text()='Найти']")

    result_page_input_locator = (By.XPATH, f"//div[@class='search2__input']//input[@value='{REQUEST}']")
    result_list_locator = (By.XPATH, "//*[@id='search-result']//li")
    result_relevance_locator = (By.XPATH, "//*[contains(text(),'ViPNet')]/parent::div")

    required_site_locator = (By.XPATH, "//a[contains(@href,'infotecs.ru')]")
    required_site_link_locator = (By.XPATH, f"//a[contains(@href,'{LINK_TO_FIND}')]")
    required_site_content_locator = (By.XPATH, "//embed[contains(@type,'application/pdf')]")

# # Example of a config for testing a script on Google
#
# class TestConfig:
#     REQUEST = "ViPNet Coordinator HW5000"
#     SEARCH_ENGINE = "https://www.google.com/"
#     LINK_TO_FIND = "https://infotecs.ru/upload/iblock/db0/ViPNet_Coordinator_HW_5000_web_july_2018.pdf"
#
#     TEXT_IN_TITLE="Google"
#
#     search_container_locator = (By.XPATH, "//*[contains(@class, 'RNNXgb')]")
#     search_page_input_locator = (By.XPATH, "//*[contains(@class, 'gLFyf')][contains(@class, 'gsfi')]")
#     search_button_locator = (By.XPATH, "*")
#
#     result_page_input_locator = (By.XPATH, f"//div[@class='RNNXgb']//input[@value='{REQUEST}']")
#     result_list_locator = (By.XPATH, "//*[@id = 'rso']//*[contains(@class, 'g')]")
#     result_relevance_locator = (By.XPATH, f"//*[contains(@class, 'g')]//*[contains(text(),'{REQUEST}')]")
#
#     required_site_locator = (By.XPATH, "//a[contains(@href,'infotecs.ru')]")
#     required_site_link_locator = (By.XPATH, f"//a[contains(@href,'{LINK_TO_FIND}')]")
#     required_site_content_locator = (By.XPATH, "//embed[contains(@type,'application/pdf')]")
