import etl


def main():
    nyt = etl.extract.csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    jh = etl.extract.csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

    nyt = etl.transform.new_york_times(nyt)
    jh = etl.transform.john_hopkins(jh)
    # print(jh)

    df = etl.transform.combine(nyt, jh)
    # print(df[df.date == '2020-12-14'])


if __name__ == '__main__':
    main()
