import requests
import logging
from typing import Optional
from models.object import MetMuseumObject
from models.departament import DepartmentsResponse
BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

logging.basicConfig(level=logging.INFO)

def get_artwork(object_id: int):
    """Запрос информации о произведении искусства по ID"""
    url = f"{BASE_URL}/objects/{object_id}"
    response = requests.get(url)
    logging.info(f"GET {url} -> {response.status_code}")
    return response

def search_artworks(query: str):
    """Поиск произведений искусства по ключевому слову"""
    url = f"{BASE_URL}/search?q={query}"
    response = requests.get(url)
    logging.info(f"GET {url} -> {response.status_code}")
    return response

def get_all_objects(metadata_date: Optional[str] = None, department_ids: Optional[str] = None):
    """
    Получение списка всех доступных объектов с возможностью фильтрации по дате обновления и отделам.
    
    :param metadata_date: Дата в формате YYYY-MM-DD (возвращает объекты, обновленные после этой даты).
    :param department_ids: ID отделов, разделенные "|", например "3|9|12".
    :return: Ответ API в формате JSON.
    """
    params = {}
    if metadata_date:
        params["metadataDate"] = metadata_date
    if department_ids:
        params["departmentIds"] = department_ids

    url = f"{BASE_URL}/objects"
    response = requests.get(url, params=params)
    logging.info(f"GET {response.url} -> {response.status_code}")
    return response

def get_object_by_id(object_id: int) -> MetMuseumObject:
    """Запрашивает объект по его ID и возвращает его в виде модели Pydantic."""
    url = f"{BASE_URL}/objects/{object_id}"
    response = requests.get(url)
    response.raise_for_status()  # Выбрасывает ошибку, если статус не 200
    return MetMuseumObject(**response.json())


def get_departments() -> DepartmentsResponse:
    url = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
    response = requests.get(url)
    response.raise_for_status()  # Если запрос не удался, возбуждаем исключение
    return DepartmentsResponse.parse_obj(response.json())
