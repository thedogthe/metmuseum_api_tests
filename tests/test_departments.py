# TODO комметнарии 
import pytest
import allure
from metmuseum_api_tests.utils.api_client import MetMuseumApiClient
from models.department import DepartmentsResponse, Department
from models.search import SearchResponse 

@pytest.fixture
def api_client():
    return MetMuseumApiClient()

@allure.suite("API Тесты Метрополитен-музея")
@allure.feature("Департаменты")
def test_get_departments(api_client):
    with allure.step("Получить список всех департаментов"):
        response = api_client.get_departments()
        
    with allure.step("Проверить код ответа"):
        assert response.status_code == 200
    
    with allure.step("Парсинг ответа и проверка структуры"):
        departments = DepartmentsResponse(**response.json())
        assert len(departments.departments) > 0
        
        # Проверяем структуру данных департамента
        first_dept = departments.departments[0]
        assert isinstance(first_dept.departmentId, int)
        assert isinstance(first_dept.displayName, str)

@allure.suite("API Тесты Метрополитен-музея")
@allure.feature("Интеграционные тесты департаментов")
def test_department_integration(api_client):
    """Получаем департаменты и затем объекты из первого департамента"""
    with allure.step("Получить список департаментов"):
        dept_response = api_client.get_departments()
        departments = DepartmentsResponse(**dept_response.json())
        first_dept_id = departments.departments[0].departmentId
    
    with allure.step(f"Искать объекты в департаменте с ID {first_dept_id}"):
        search_response = api_client.search_objects("", departmentId=first_dept_id)
        search_result = SearchResponse(**search_response.json())
        
    with allure.step("Проверить что найдены объекты"):
        assert search_result.total > 0