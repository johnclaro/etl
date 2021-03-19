from abc import ABC, abstractmethod


class Source(ABC):

    @abstractmethod
    def extract(self):
        pass

    @abstractmethod
    def transform(self, response):
        pass

    @abstractmethod
    def load(self, items):
        pass

    def etl(self):
        extractions = self.extract()
        for extraction in extractions:
            items = self.transform(extraction)
            loaded = self.load(items)
            result = {
                'items': len(items),
                'status_code': loaded.status_code
            }
            yield result
