# tests/test_search.py
import pytest
import allure
from metmuseum_api_tests.utils.api_client import MetMuseumApiClient
from models.search import SearchResponse, SearchRequestParams

@pytest.fixture
def api_client():
    return MetMuseumApiClient()

@allure.suite("API Тесты Метрополитен-музея")
@allure.feature("Поиск объектов")
class TestSearch:
    @allure.title("Базовый поиск по ключевому слову")
    @allure.story("Основные сценарии поиска")
    def test_basic_search(self, api_client):
        """Тест базового поиска по ключевому слову"""
        search_term = "sunflowers"
        
        with allure.step(f"Выполнение поиска по термину '{search_term}'"):
            response = api_client.search_objects(search_term)
            
        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200
            
        with allure.step("Парсинг и валидация ответа"):
            search_result = SearchResponse(**response.json())
            assert search_result.total >= 0
            assert isinstance(search_result.objectIDs, list)
            
            if search_result.total > 0:
                allure.attach(
                    f"Найдено объектов: {search_result.total}\n"
                    f"Пример ID: {search_result.objectIDs[:5]}",
                    name="Результаты поиска",
                    attachment_type=allure.attachment_type.TEXT
                )
                assert all(isinstance(obj_id, int) for obj_id in search_result.objectIDs[:10])

    @allure.title("Параметризованный тест разных поисковых терминов")
    @allure.story("Основные сценарии поиска")
    @pytest.mark.parametrize("search_term,expected_min", [
        ("sunflowers", 1),
        ("monet", 5),
        ("vase", 10)
    ])
    def test_search_different_terms(self, api_client, search_term, expected_min):
        """Параметризованный тест разных поисковых терминов"""
        with allure.step(f"Поиск по термину '{search_term}' (ожидаем минимум {expected_min} результатов)"):
            response = api_client.search_objects(search_term)
            search_result = SearchResponse(**response.json())
            
        with allure.step("Проверка количества результатов"):
            assert search_result.total >= expected_min
            allure.attach(
                f"Фактическое количество: {search_result.total}",
                name="Результаты поиска",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Поиск с фильтром по highlight объектам")
    @allure.story("Фильтрация результатов")
    def test_search_with_highlight_filter(self, api_client):
        """Тест поиска только highlight объектов"""
        with allure.step("Поиск 'flower' только среди highlight объектов"):
            response = api_client.search_objects("flower", isHighlight=True)
            search_result = SearchResponse(**response.json())
            
        with allure.step("Проверка результатов"):
            assert search_result.total > 0
            allure.attach(
                f"Найдено highlight объектов: {search_result.total}",
                name="Результаты",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Поиск по департаменту")
    @allure.story("Фильтрация результатов")
    def test_search_with_department_filter(self, api_client):
        """Тест поиска по департаменту"""
        department_id = 6  # Asian Art
        with allure.step(f"Поиск всех объектов в департаменте {department_id}"):
            response = api_client.search_objects("", departmentId=department_id)
            search_result = SearchResponse(**response.json())
            
        with allure.step("Проверка результатов"):
            assert search_result.total > 0
            allure.attach(
                f"Объектов в департаменте: {search_result.total}",
                name="Результаты",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Поиск с комбинированными фильтрами")
    @allure.story("Комплексные сценарии")
    def test_combined_filters(self, api_client):
        """Тест комбинации нескольких фильтров"""
        search_params = {
            "q": "woman",
            "departmentId": 11,  # European Paintings
            "isHighlight": True,
            "hasImages": True
        }
        
        with allure.step(f"Выполнение поиска с параметрами: {search_params}"):
            response = api_client.search_objects(**search_params)
            search_result = SearchResponse(**response.json())
            
        with allure.step("Проверка результатов"):
            assert search_result.total > 0
            allure.attach(
                str(search_params),
                name="Параметры поиска",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                f"Найдено объектов: {search_result.total}",
                name="Результаты",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Поиск по временному диапазону")
    @allure.story("Фильтрация результатов")
    def test_date_range_filter(self, api_client):
        """Тест поиска по временному диапазону"""
        date_range = {"dateBegin": 1800, "dateEnd": 1900}
        
        with allure.step(f"Поиск объектов в диапазоне {date_range}"):
            response = api_client.search_objects("", **date_range)
            search_result = SearchResponse(**response.json())
            
        with allure.step("Проверка результатов"):
            assert search_result.total > 0
            allure.attach(
                f"Найдено объектов в указанном периоде: {search_result.total}",
                name="Результаты",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Валидация параметров поиска")
    @allure.story("Валидация данных")
    def test_search_params_validation(self):
        """Тест валидации параметров поиска"""
        test_params = {
            "q": "sunflowers",
            "isHighlight": True,
            "dateBegin": 1800,
            "dateEnd": 1900
        }
        
        with allure.step("Создание параметров поиска"):
            params = SearchRequestParams(**test_params)
            
        with allure.step("Проверка параметров"):
            assert params.q == "sunflowers"
            assert params.isHighlight is True
            assert params.dateBegin == 1800
            assert params.dateEnd == 1900
            
            allure.attach(
                str(params.dict()),
                name="Параметры поиска",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.title("Комплексный тест поиска")
    @allure.story("Комплексные сценарии")
    @pytest.mark.slow
    def test_complex_search(self, api_client):
        """Комплексный тест поиска с множеством параметров"""
        search_params = {
            "q": "landscape",
            "isHighlight": True,
            "hasImages": True,
            "departmentId": 11,  # European Paintings
            "dateBegin": 1700,
            "dateEnd": 1800,
            "artistOrCulture": True
        }
        
        with allure.step(f"Выполнение комплексного поиска с параметрами: {search_params}"):
            response = api_client.search_objects(**search_params)
            search_result = SearchResponse(**response.json())
            
        with allure.step("Проверка результатов"):
            assert search_result.total > 0
            assert len(search_result.objectIDs) > 0
            
            allure.attach(
                str(search_params),
                name="Параметры поиска",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                f"Найдено объектов: {search_result.total}",
                name="Результаты",
                attachment_type=allure.attachment_type.TEXT
            )
