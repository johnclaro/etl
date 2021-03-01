import covid


def main():
    nyt = covid.extract.new_york_times()
    jh = covid.extract.john_hopkins()

    nyt = covid.transformation.transform(nyt)
    jh = covid.transformation.transform(jh)
    df = covid.transformation.join(nyt, jh)

    # print(df[df.date == '2020-12-14'])


if __name__ == '__main__':
    main()
