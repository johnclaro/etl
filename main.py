import etl


def main():
    ny = etl.extract.website('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    jh = etl.extract.website('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

    ny = etl.transform.new_york_times(ny)
    jh = etl.transform.john_hopkins(jh)

    df = etl.transform.combine(ny, jh)


if __name__ == '__main__':
    main()
