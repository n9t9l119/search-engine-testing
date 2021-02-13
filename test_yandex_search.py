import pytest
import allure
from allure_commons.types import AttachmentType

from TestConfig import TestConfig


@allure.feature('Старт тестирования сценария')
@pytest.mark.usefixtures('browser', 'search_page', 'result_page')
@pytest.mark.incremental
class TestUserHandling:
    @allure.story('Открываем стартовую страницу')
    @allure.link(name="Стартовая страница", url=TestConfig.SEARCH_ENGINE)
    def test_open_start_page(self, browser, search_page):
        search_page.open_base_url()
        with allure.step('Делаем скриншот'):
            allure.attach(browser.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)

    @allure.story('Проверяем, что не произошел редирект')
    def test_being_on_desired_page(self, browser):
        with allure.step('Убедимся, что мы находимся на нужной ссылке'):
            assert browser.current_url == TestConfig.SEARCH_ENGINE
        with allure.step(f'Проверим, что в титле присутсвует текст "{TestConfig.TEXT_IN_TITLE}"'):
            assert TestConfig.TEXT_IN_TITLE in browser.title

    @allure.story('Проверяем присутствие необходимых DOM элементов поисковой системы')
    def test_presence_of_DOM_search_elems(self, search_page):
        with allure.step('Проверим присутствие контейнера поиска'):
            assert bool(search_page.find_element(TestConfig.search_container_locator))
        with allure.step('Проверим присутствие инпута'):
            assert bool(search_page.find_element(TestConfig.search_page_input_locator))
        with allure.step('Проверим присутствие кнопки'):
            assert bool(search_page.find_elements(TestConfig.search_button_locator))

    @allure.story('Отправляем запрос')
    def test_send_query(self, browser, search_page):
        search_page.search(search_button_locator=TestConfig.search_button_locator)
        with allure.step('Делаем скриншот'):
            allure.attach(browser.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)

    @allure.story('Проверяем, что не произошла потеря инпута и введенных данных')
    def test_valid_input_presence(self, result_page):
        result_page.find_element(TestConfig.result_page_input_locator)

    @allure.story(
        'Если тестируемая поисковая система - русский яндекс, '
        'то проверяем корректность сгенерированной ссылки,'
        ' по которой мы перешли')
    @pytest.mark.skipif(TestConfig.SEARCH_ENGINE != "https://yandex.ru/", reason="Test only for yandex.ru")
    def test_current_url(self, browser):
        assert browser.current_url == "https://yandex.ru/search/?lr=2&text=" + TestConfig.REQUEST.replace(' ', '%20')

    @allure.story('Проверяем корректность полученных результатов')
    def test_search_results_correctness(self, result_page):
        with allure.step('Проверим наличие результатов поиска'):
            assert result_page.get_results_count() > 0

        with allure.step('Проверим присутствие текста запроса в выдаче результатов поиска'):
            assert len(result_page.get_request_presence_in_results()) > 0

        with allure.step('Проверим присутствие необходимого сайта в выдаче'):
            assert result_page.get_results_count(TestConfig.required_site_locator) > 0

    @allure.story('Проверяем наличие целевой ссылки в результатах выдачи')
    def test_find_link(self, result_page):
        assert bool(result_page.find_element(TestConfig.required_site_link_locator))

    @allure.link(name="Ссылка, на которой нужно оказаться", url=TestConfig.LINK_TO_FIND)
    @allure.story('Проверяем корректность перехода по ссылке')
    def test_open_link(self, browser, result_page):
        with allure.step('Кликнем по целевой ссылке'):
            result_page.find_element(TestConfig.required_site_link_locator).click()
        with allure.step('Перейдем на новую открывшуюся вкладку'):
            browser.switch_to.window(browser.window_handles[-1])

    @allure.story('Проверяем, что не произошел редирект')
    def test_opened_site_url(self, browser, result_page):
        with allure.step('Убедимся, что мы находимся на нужной ссылке'):
            assert browser.current_url == TestConfig.LINK_TO_FIND

    @allure.story('Проверяем наличие необходимого контента')
    def test_opened_site_content(self, browser, result_page):
        with allure.step('Делаем скриншот'):
            allure.attach(browser.get_screenshot_as_png(), name='screenshot', attachment_type=AttachmentType.PNG)
        search_results = result_page.find_elements(TestConfig.required_site_content_locator)
        assert len(search_results) > 0
