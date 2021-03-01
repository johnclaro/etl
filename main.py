import etl
from datasets import Dataset


def main():
    nyt = etl.extraction.extract(Dataset.NEW_YORK_TIMES)
    jh = etl.extraction.extract(Dataset.JOHN_HOPKINS)

    nyt = etl.transformation.transform(nyt)
    jh = etl.transformation.transform(jh)
    df = etl.transformation.join(nyt, jh)

    # print(df[df.date == '2020-12-14'])


if __name__ == '__main__':
    main()
