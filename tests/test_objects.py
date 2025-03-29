# tests/test_objects.py
import pytest
from metmuseum_api_tests.utils.api_client import MetMuseumApiClient
from models.object import ArtObject
from models.objects import ObjectIDsResponse
from pydantic import HttpUrl
@pytest.fixture
def api_client():
    return MetMuseumApiClient()

def test_get_object_by_id(api_client):
    # Тест получения объекта по существующему ID
    response = api_client.get_object(437133)
    assert response.status_code == 200
    
    art_object = ArtObject(**response.json())
    assert art_object.objectID == 437133
    assert art_object.title
    assert art_object.artistDisplayName

def test_get_nonexistent_object(api_client):
    # Тест обработки несуществующего ID
    response = api_client.get_object(999999999)
    assert response.status_code == 404

def test_object_data_structure(api_client):
    # Тест структуры данных объекта
    response = api_client.get_object(45734)
    art_object = ArtObject(**response.json())
    
    assert isinstance(art_object.objectID, int)
    assert isinstance(art_object.isHighlight, bool)
    # Измененная проверка для primaryImage:
    assert art_object.primaryImage is None or isinstance(art_object.primaryImage, HttpUrl)
    # Аналогично для primaryImageSmall:
    assert art_object.primaryImageSmall is None or isinstance(art_object.primaryImageSmall, HttpUrl)