import covid


def lambda_handler():
    # nyt = covid.etl.extract(covid.datasets.NEW_YORK_TIMES)
    # jh = covid.etl.extract(covid.datasets.JOHN_HOPKINS)

    # nyt = covid.etl.transform(nyt)
    # jh = covid.etl.transform(jh)
    # df = covid.etl.join(nyt, jh)

    return {'status': 'Hello from Github Action'}


if __name__ == '__main__':
    lambda_handler()
