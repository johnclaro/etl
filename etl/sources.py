from abc import ABC, abstractmethod
from urllib.parse import urljoin

from etl import settings


class Source(ABC):

    def __init__(self):
        self.dataset = settings.DATASET
        self.load_url = urljoin(settings.URL, f'covid/{self.dataset}/upsert')

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, response):
        pass

    @abstractmethod
    def load(self, data):
        pass

    def etl(self):
        response = self.extract()
        data = self.transform(response)
        status = self.load(data)
        return status
