# tests/test_departments.py
import pytest
from metmuseum_api_tests.utils.api_client import MetMuseumApiClient
from models.department import DepartmentsResponse, Department
from models.search import SearchResponse 

@pytest.fixture
def api_client():
    return MetMuseumApiClient()

def test_get_departments(api_client):
    response = api_client.get_departments()
    assert response.status_code == 200
    
    departments = DepartmentsResponse(**response.json())
    assert len(departments.departments) > 0
    
    # Проверяем структуру данных департамента
    first_dept = departments.departments[0]
    assert isinstance(first_dept.departmentId, int)
    assert isinstance(first_dept.displayName, str)

def test_department_integration(api_client):
    """Получаем департаменты и затем объекты из первого департамента"""
    dept_response = api_client.get_departments()
    departments = DepartmentsResponse(**dept_response.json())
    first_dept_id = departments.departments[0].departmentId
    
    search_response = api_client.search_objects("", departmentId=first_dept_id)
    search_result = SearchResponse(**search_response.json())
    assert search_result.total > 0