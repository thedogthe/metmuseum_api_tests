import pytest
from metmuseum_api_tests.utils.api_client import get_departments
from models.department import DepartmentsResponse, Department

def test_get_departments():
    """Проверка получения списка департаментов"""
    response = get_departments()
    
    # Проверка кода статуса
    assert response is not None, "Expected a response"
    assert isinstance(response, DepartmentsResponse)
    assert len(response.departments) > 0, "Expected at least one department"

def test_get_departments_ids():
    """Проверка на наличие departmentId в каждом департаменте"""
    response = get_departments()
    
    # Проверка каждого департамента
    for department in response.departments:
        assert isinstance(department.departmentId, int), f"Invalid departmentId for {department.displayName}"
        assert department.departmentId > 0, f"Invalid departmentId value for {department.displayName}"

def test_get_departments_display_names():
    """Проверка на наличие displayName в каждом департаменте"""
    response = get_departments()
    
    # Проверка наличия displayName
    for department in response.departments:
        assert isinstance(department.displayName, str), f"Invalid displayName for {department.departmentId}"
        assert len(department.displayName) > 0, f"Display name is empty for department {department.departmentId}"

def test_get_department_by_id():
    """Проверка получения департамента по ID"""
    department_id = 1  # Пример департамента
    response = get_departments()
    
    department = next((dept for dept in response.departments if dept.departmentId == department_id), None)
    
    assert department is not None, f"Department with id {department_id} not found"
    assert department.departmentId == department_id, f"Expected departmentId {department_id}, but got {department.departmentId}"
    assert isinstance(department.displayName, str), "Invalid department displayName"

def test_get_departments_empty_response():
    """Тест обработки пустого ответа от API"""
    # Можно смокировать пустой ответ
    with pytest.raises(Exception):  # Замените на более конкретную ошибку
        # Мокируем пустой ответ
        get_departments()
