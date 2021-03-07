
from etl.covid.items import Item


class Swab(Item):

    def __init__(
        self,
        date,
        hospitals,
        non_hospitals,
        labs,
        positive_all,
        positive_rate_all,
        test_24,
        test_7,
        positive_7,
        positive_rate_7,
        fid
    ):
        Item.__init__(self, date)
        self.hospitals = hospitals
        self.non_hospitals = non_hospitals
        self.labs = labs
        self.positive_all = positive_all
        self.positive_rate_all = positive_rate_all
        self.test_24 = test_24
        self.test_7 = test_7
        self.positive_all = positive_7
        self.positive_rate_7 = positive_rate_7
        self.fid = fid


class Case(Item):

    def __init__(
        self,
        date,
        confirmed_covid_cases,
        total_confirmed_covid_cases,
        confirmed_covid_deaths,
        total_covid_deaths,
        statistics_profile_date,
        covid_cases_confirmed,
        hospitalised_covid_cases,
        requiring_icu_covid_cases,
        healthcare_workers_covid_cases,
        clusters_notified,
        hospitalised_aged_5,
        hospitalised_aged_5_to_14,
        hospitalised_aged_15_to_24,
        hospitalised_aged_25_to_34,
        hospitalised_aged_35_to_44,
        hospitalised_aged_45_to_54,
        hospitalised_aged_55_to_64,
        hospitalised_aged_65_up,
        male,
        female,
        unknown,
        aged_1_to_4,
        aged_5_to_14,
        aged_15_to_24,
        aged_25_to_34,
        aged_35_to_44,
        aged_45_to_54,
        aged_55_to_64,
        aged_65_up,
        median_age,
        community_transmission,
        close_contact,
        travel_abroad,
        fid,
    ):
        Item.__init__(self, date)
        self.date = date
        self.confirmed_covid_cases = confirmed_covid_cases
        self.total_confirmed_covid_cases = total_confirmed_covid_cases
        self.confirmed_covid_deaths = confirmed_covid_deaths
        self.total_covid_deaths = total_covid_deaths
        self.statistics_profile_date = statistics_profile_date
        self.covid_cases_confirmed = covid_cases_confirmed
        self.hospitalised_covid_cases = hospitalised_covid_cases
        self.requiring_icu_covid_cases = requiring_icu_covid_cases
        self.healthcare_workers_covid_cases = healthcare_workers_covid_cases
        self.clusters_notified = clusters_notified
        self.hospitalised_aged_5 = hospitalised_aged_5
        self.hospitalised_aged_5_to_14 = hospitalised_aged_5_to_14
        self.hospitalised_aged_15_to_24 = hospitalised_aged_15_to_24
        self.hospitalised_aged_25_to_34 = hospitalised_aged_25_to_34
        self.hospitalised_aged_35_to_44 = hospitalised_aged_35_to_44
        self.hospitalised_aged_45_to_54 = hospitalised_aged_45_to_54
        self.hospitalised_aged_55_to_64 = hospitalised_aged_55_to_64
        self.hospitalised_aged_65_up = hospitalised_aged_65_up
        self.male = male
        self.female = female
        self.unknown = unknown
        self.aged_1_to_4 = aged_1_to_4
        self.aged_5_to_14 = aged_5_to_14
        self.aged_15_to_24 = aged_15_to_24
        self.aged_25_to_34 = aged_25_to_34
        self.aged_35_to_44 = aged_35_to_44
        self.aged_45_to_54 = aged_45_to_54
        self.aged_55_to_64 = aged_55_to_64
        self.aged_65_up = aged_65_up
        self.median_age = median_age
        self.community_transmission = community_transmission
        self.close_contact = close_contact
        self.travel_abroad = travel_abroad
        self.fid = fid