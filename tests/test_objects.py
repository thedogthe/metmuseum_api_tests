# TODO комметнарии 
import pytest
import allure
from metmuseum_api_tests.utils.api_client import MetMuseumApiClient
from models.object import ArtObject
from pydantic import HttpUrl
import requests 
from datetime import date, timedelta
from models.objects import ObjectIDsResponse, ObjectIDsRequestParams

@pytest.fixture
def api_client():
    return MetMuseumApiClient()

@allure.suite("API Тесты Метрополитен-музея")
@allure.feature("Работа с объектами")
class TestObjects:
    @allure.title("Получение объекта по ID")
    @allure.story("Позитивные тесты")
    def test_get_object_by_id(self, api_client):
        """Тест получения объекта по существующему ID"""
        test_id = 437133
        with allure.step(f"Запрос объекта с ID {test_id}"):
            response = api_client.get_object(test_id)
            
        with allure.step("Проверка кода ответа"):
            assert response.status_code == 200
            
        with allure.step("Валидация структуры ответа"):
            art_object = ArtObject(**response.json())
            assert art_object.objectID == test_id
            assert art_object.title
            assert art_object.artistDisplayName
            
            allure.attach(
                f"Название объекта: {art_object.title}\nХудожник: {art_object.artistDisplayName}",
                name="Информация об объекте",
                attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Попытка получения несуществующего объекта")
    @allure.story("Негативные тесты")
    def test_get_nonexistent_object(self, api_client):
        """Тест обработки несуществующего ID"""
        non_existent_id = 999999999
        with allure.step(f"Попытка запроса несуществующего объекта с ID {non_existent_id}"):
            try:
                response = api_client.get_object(non_existent_id)
                pytest.fail("Expected 404 error but request succeeded")
            except requests.exceptions.HTTPError as e:
                with allure.step("Проверка ошибки"):
                    assert e.response.status_code == 404
                    assert "Not Found" in str(e)
                    allure.attach(
                        str(e.response.json()),
                        name="Тело ошибки",
                        attachment_type=allure.attachment_type.JSON
                    )

    @allure.title("Проверка структуры данных объекта")
    @allure.story("Валидация данных")
    def test_object_data_structure(self, api_client):
        """Тест структуры данных объекта"""
        test_id = 45734
        with allure.step(f"Запрос объекта с ID {test_id}"):
            response = api_client.get_object(test_id)
            
        with allure.step("Проверка структуры данных"):
            art_object = ArtObject(**response.json())
            
            assert isinstance(art_object.objectID, int)
            assert isinstance(art_object.isHighlight, bool)
            assert art_object.primaryImage is None or isinstance(art_object.primaryImage, HttpUrl)
            assert art_object.primaryImageSmall is None or isinstance(art_object.primaryImageSmall, HttpUrl)
            
            allure.attach(
                str(art_object.dict()),
                name="Полные данные объекта",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.title("Валидация параметров запроса")
    @allure.story("Валидация данных")
    def test_objects_request_params_validation(self):
        """Тест валидации параметров запроса"""
        with allure.step("Создание тестовых параметров"):
            params = ObjectIDsRequestParams(
                metadataDate=date(2023, 1, 1),
                departmentIds="1|2|3"
            )
            
        with allure.step("Проверка параметров"):
            assert params.metadataDate == date(2023, 1, 1)
            assert params.departmentIds == "1|2|3"
            
            allure.attach(
                str(params.dict()),
                name="Параметры запроса",
                attachment_type=allure.attachment_type.JSON
            )

    @allure.title("Обработка пустого ответа")
    @allure.story("Валидация данных")
    def test_empty_response(self, api_client):
        """Тест обработки пустого ответа"""
        with allure.step("Создание пустого ответа"):
            empty_data = {"total": 0, "objectIDs": []}
            
        with allure.step("Проверка обработки пустого ответа"):
            objects = ObjectIDsResponse(**empty_data)
            assert objects.total == 0
            assert len(objects.objectIDs) == 0
            
            allure.attach(
                str(objects.dict()),
                name="Пустой ответ",
                attachment_type=allure.attachment_type.JSON
            )