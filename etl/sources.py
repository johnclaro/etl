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
        response = self.load(data)
        task = {'items': len(data), 'status': response.status_code}
        return task
