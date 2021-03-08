from abc import ABC, abstractmethod
from json.decoder import JSONDecodeError


class Source(ABC):

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
        task = {'items': len(data), 'message': None}
        response = self.load(data)
        try:
            task['message'] = response.json()
        except JSONDecodeError:
            task['message'] = 'Error response'
        return task
