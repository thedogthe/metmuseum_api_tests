import pytest
from metmuseum_api_tests.utils.api_client import get_all_objects
from models.object_list import ObjectList
from metmuseum_api_tests.utils.api_client import get_object_by_id
from models.object import MetMuseumObject

def test_get_all_objects():
    """ Проверка получения списка всех объектов """
    response = get_all_objects()
    
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    data = response.json()
    object_list = ObjectList(**data)  # Валидация через Pydantic
    
    assert object_list.total > 0, "Expected at least one object"
    assert isinstance(object_list.objectIDs, list) and len(object_list.objectIDs) > 0

def test_get_objects_by_department():
    """ Проверка фильтрации по отделу """
    response = get_all_objects(department_ids="3|9|12")
    
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    data = response.json()
    object_list = ObjectList(**data)
    
    assert object_list.total > 0, "Expected at least one object for given departments"

def test_get_objects_by_metadata_date():
    """ Проверка фильтрации по дате обновления """
    response = get_all_objects(metadata_date="2018-10-22")
    
    assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
    
    data = response.json()
    object_list = ObjectList(**data)
    
    assert object_list.total > 0, "Expected at least one object updated after given date"


def test_get_valid_object():
    """Тест получения валидного объекта из API."""
    object_id = 437133  # Картина "Wheat Field with Cypresses" (Ван Гог)
    obj = get_object_by_id(object_id)
    
    assert isinstance(obj, MetMuseumObject)
    assert obj.objectID == object_id
    assert obj.title is not None
    assert obj.isPublicDomain is True
    assert obj.primaryImage is not None
    assert obj.objectURL.startswith("https://www.metmuseum.org")

def test_get_object_with_constituents():
    """Тест наличия списка авторов (constituents) в объекте."""
    object_id = 459123  # Объект с несколькими авторами
    obj = get_object_by_id(object_id)

    assert obj.constituents is not None
    assert isinstance(obj.constituents, list)
    assert len(obj.constituents) > 0
    for artist in obj.constituents:
        assert artist.name is not None
        assert isinstance(artist.name, str)

def test_get_invalid_object():
    """Тест обработки ошибки при запросе несуществующего объекта."""
    with pytest.raises(Exception):  # Можно заменить на requests.HTTPError
        get_object_by_id(9999999999)
