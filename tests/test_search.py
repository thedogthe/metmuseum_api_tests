# tests/test_search.py
import pytest
from metmuseum_api_tests.utils.api_client import MetMuseumApiClient
from models.search import SearchResponse

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