import logging
from typing import Dict, Any, List

from elasticsearch_dsl import Search
from elasticsearch_dsl.search_base import SearchBase

from bestcar.models.publishing_trip_dto import TripDTO

logger = logging.getLogger('duration_request_view')


class TripFilterService:
    """
    Производит фильтрацию на основе параметров который задал пользователь
    в форме на главной странице
    """
    def __init__(self,queryset: SearchBase, data: Dict[str, Any]) -> None:
        """
               Конструктор для инициализации объекта с queryset и данными.

               :param queryset: Запрос к Elasticsearch (объект Search).
               :param data: Словарь данных с ключами типа str и значениями любого типа.
        """
        self.queryset = queryset
        self.data = data

    @staticmethod
    def parse_elastic_hits(result: Search) -> List[TripDTO]:
        """
        Парсит результаты поиска из Elasticsearch и извлекает документы как объекты TripDTO.

            :param result: объект результата поиска, полученный от Elasticsearch.
            :return: список объектов TripDTO.
        """
        result = (result.execute().to_dict())
        hits = result['hits']['hits']
        documents = [TripDTO.from_dict(hit['_source']) for hit in hits]
        return documents


    def filter_trip(self)-> List[TripDTO]:
        """
            Основной метод для фильтрации поездок
        """
        search_query = self.queryset.query(
            'bool',
            must=[
                {'fuzzy': {'departure': {'value': self.data['departure'], 'fuzziness': 'AUTO'}}},
                {'fuzzy': {'arrival': {'value': self.data['arrival'], 'fuzziness': 'AUTO'}}}
            ],
            filter=[
                {'range': {'departure_time': {'gte': self.data['datetime_value']}}},
                {'range': {'free_seating': {'gte': self.data['seating']}}}
            ]
        )

        results = TripFilterService.parse_elastic_hits(search_query)
        return results
