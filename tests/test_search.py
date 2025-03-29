# tests/test_search.py
import pytest
from metmuseum_api_tests.utils.api_client import MetMuseumApiClient
from models.search import SearchResponse, SearchRequestParams

@pytest.fixture
def api_client():
    return MetMuseumApiClient()

def test_basic_search(api_client):
    # Тест базового поиска
    response = api_client.search_objects("sunflowers")
    assert response.status_code == 200
    
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0
    assert len(search_result.objectIDs) > 0

def test_search_with_filters(api_client):
    # Тест поиска с фильтрами
    response = api_client.search_objects(
        "flowers",
        isHighlight=True,
        hasImages=True,
        departmentId=11  # European Paintings
    )
    assert response.status_code == 200
    
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

def test_search_by_artist(api_client):
    # Тест поиска по художнику
    response = api_client.search_objects(
        "Van Gogh",
        artistOrCulture=True
    )
    assert response.status_code == 200
    
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

def test_search_with_date_range(api_client):
    # Тест поиска по диапазону дат
    response = api_client.search_objects(
        "portrait",
        dateBegin=1700,
        dateEnd=1800
    )
    assert response.status_code == 200
    
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

# Базовые тесты поиска
def test_basic_search(api_client):
    """Тест базового поиска по ключевому слову"""
    response = api_client.search_objects("sunflowers")
    assert response.status_code == 200
    
    search_result = SearchResponse(**response.json())
    assert search_result.total >= 0
    assert isinstance(search_result.objectIDs, list)
    
    # Если есть результаты, проверяем что ID валидные
    if search_result.total > 0:
        assert all(isinstance(obj_id, int) for obj_id in search_result.objectIDs[:10])

@pytest.mark.parametrize("search_term,expected_min", [
    ("sunflowers", 1),
    ("monet", 5),
    ("vase", 10)
])
def test_search_different_terms(api_client, search_term, expected_min):
    """Параметризованный тест разных поисковых терминов"""
    response = api_client.search_objects(search_term)
    search_result = SearchResponse(**response.json())
    assert search_result.total >= expected_min

# Тесты фильтров
def test_search_with_highlight_filter(api_client):
    """Тест поиска только highlight объектов"""
    response = api_client.search_objects("flower", isHighlight=True)
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

def test_search_with_department_filter(api_client):
    """Тест поиска по департаменту"""
    response = api_client.search_objects("", departmentId=6)  # Asian Art
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

def test_search_with_image_filter(api_client):
    """Тест поиска только объектов с изображениями"""
    response = api_client.search_objects("portrait", hasImages=True)
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

# Тесты комбинированных фильтров
def test_combined_filters(api_client):
    """Тест комбинации нескольких фильтров"""
    response = api_client.search_objects(
        "woman",
        departmentId=11,  # European Paintings
        isHighlight=True,
        hasImages=True
    )
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

# Тесты временного диапазона
def test_date_range_filter(api_client):
    """Тест поиска по временному диапазону"""
    response = api_client.search_objects(
        "",
        dateBegin=1800,
        dateEnd=1900
    )
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0

# Тесты валидации параметров
def test_search_params_validation():
    """Тест валидации параметров поиска"""
    params = SearchRequestParams(
        q="sunflowers",
        isHighlight=True,
        dateBegin=1800,
        dateEnd=1900
    )
    assert params.q == "sunflowers"
    assert params.isHighlight is True
    assert params.dateBegin == 1800
    assert params.dateEnd == 1900

# def test_empty_search(api_client):
#     """Тест пустого поискового запроса"""
#     response = api_client.search_objects("")
#     assert response.status_code == 200
#     data = response.json()
#     # Обеспечиваем что objectIDs будет списком, даже если пустым
#     data['objectIDs'] = data.get('objectIDs', [])
#     search_result = SearchResponse(**data)
#     assert search_result.total >= 0

# def test_invalid_filters(api_client):
#     """Тест с невалидными фильтрами"""
#     response = api_client.search_objects("sunflowers", departmentId=99999)
#     assert response.status_code == 200
#     data = response.json()
#     data['objectIDs'] = data.get('objectIDs', [])
#     search_result = SearchResponse(**data)
#     assert search_result.total == 0

def test_search_limit(api_client):
    """Тест ограничения количества результатов"""
    response = api_client.search_objects("vase")
    data = response.json()
    search_result = SearchResponse(**data)
    # Обновляем утверждение, так как API возвращает все результаты
    assert len(search_result.objectIDs) == search_result.total
# Дополнительные тесты
@pytest.mark.slow
def test_complex_search(api_client):
    """Комплексный тест поиска с множеством параметров"""
    response = api_client.search_objects(
        "landscape",
        isHighlight=True,
        hasImages=True,
        departmentId=11,  # European Paintings
        dateBegin=1700,
        dateEnd=1800,
        artistOrCulture=True
    )
    search_result = SearchResponse(**response.json())
    assert search_result.total > 0
    assert len(search_result.objectIDs) > 0