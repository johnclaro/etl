from abc import ABC, abstractmethod

from etl import settings


class Source(ABC):

    def __init__(self):
        self.dataset = settings.DATASET

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
        message = {'items': len(data), 'success': False}
        response = self.load(data)
        if response.status_code == 200:
            message['success'] = True
        return message
