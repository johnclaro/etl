import extractor
import transformer


def main():
    ny = extractor.extract('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    jh = extractor.extract('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

    ny = transformer.transform(ny)
    jh = transformer.transform(jh)

    df = transformer.combine(ny, jh)


if __name__ == '__main__':
    main()
