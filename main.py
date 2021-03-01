import etl


def main():
    nyt = etl.extract.new_york_times()
    jh = etl.extract.john_hopkins()

    nyt = etl.transformation.transform(nyt)
    jh = etl.transformation.transform(jh)
    df = etl.transformation.join(nyt, jh)

    # print(df[df.date == '2020-12-14'])


if __name__ == '__main__':
    main()
