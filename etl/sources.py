from abc import ABC, abstractmethod


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
        task['message'] = response.json()
        return task
