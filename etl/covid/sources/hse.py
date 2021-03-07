import json

import requests

from etl.sources import Source
from etl.covid.items import HSESwab, HSECase


class HSE(Source):

    def __init__(self):
        Source.__init__(self)
        urls = {
            'cases': 'https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/CovidStatisticsProfileHPSCIrelandOpenData/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
            'swabs': 'https://services-eu1.arcgis.com/z6bHNio59iTqqSUY/arcgis/rest/services/LaboratoryLocalTimeSeriesHistoricView/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json',
        }
        self.extract_url = urls[self.dataset]

    def extract(self):
        response = requests.get(self.extract_url).json()
        return response

    def transform(self, response):
        if self.dataset == 'cases':
            data = self._transform_cases(response)
        elif self.dataset == 'swabs':
            data = self._transform_swabs(response)
        return data

    def load(self, data):
        status = {'successes': 0, 'errors': 0}
        data = json.dumps(data)
        response = requests.post(self.load_url, data=data)
        if response.status_code == 200:
            status['successes'] += 1
        else:
            status['errors'] += 1
        return status

    def _transform_cases(self, response):
        data = []
        for feature in response['features']:
            attribute = feature['attributes']
            print(attribute)
            print('---')
            case = HSECase(
                date=attribute['Date'],
                confirmed_covid_cases=attribute['ConfirmedCovidCases'],
                total_confirmed_covid_cases=attribute['TotalConfirmedCovidCases'],
                confirmed_covid_deaths=attribute['ConfirmedCovidDeaths'],
                total_covid_deaths=attribute['TotalCovidDeaths'],
                statistics_profile_date=attribute['StatisticsProfileDate'],
                covid_cases_confirmed=attribute['CovidCasesConfirmed'],
                hospitalised_covid_cases=attribute['HospitalisedCovidCases'],
                requiring_icu_covid_cases=attribute['RequiringICUCovidCases'],
                healthcare_workers_covid_cases=attribute['HealthcareWorkersCovidCases'],
                clusters_notified=attribute['ClustersNotified'],
                hospitalised_aged_5=attribute['HospitalisedAged5'],
                hospitalised_aged_5_to_14=attribute['HospitalisedAged5to14'],
                hospitalised_aged_15_to_24=attribute['HospitalisedAged15to24'],
                hospitalised_aged_25_to_34=attribute['HospitalisedAged25to34'],
                hospitalised_aged_35_to_44=attribute['HospitalisedAged35to44'],
                hospitalised_aged_45_to_54=attribute['HospitalisedAged45to54'],
                hospitalised_aged_55_to_64=attribute['HospitalisedAged55to64'],
                hospitalised_aged_65_up=attribute['HospitalisedAged65up'],
                male=attribute['Male'],
                female=attribute['Female'],
                unknown=attribute['Unknown'],
                aged_1_to_4=attribute['Aged1to4'],
                aged_5_to_14=attribute['Aged5to14'],
                aged_15_to_24=attribute['Aged15to24'],
                aged_25_to_34=attribute['Aged25to34'],
                aged_35_to_44=attribute['Aged35to44'],
                aged_45_to_54=attribute['Aged45to54'],
                aged_55_to_64=attribute['Aged55to64'],
                aged_65_up=attribute['Aged65up'],
                median_age=attribute['Median_Age'],
                community_transmission=attribute['CommunityTransmission'],
                close_contact=attribute['CloseContact'],
                travel_abroad=attribute['TravelAbroad'],
                fid=attribute['FID'],
            )
            data.append(case.__dict__)
        
        print(data)
        return data

    def _transform_swabs(self, response):
        data = []
        for feature in response['features']:
            attribute = feature['attributes']
            swab = HSESwab(
                date=attribute['Date_HPSC'],
                hospitals=attribute['Hospitals'],
                non_hospitals=attribute['NonHospitals'],
                labs=attribute['TotalLabs'],
                positive_all=attribute['Positive'],
                positive_rate_all=attribute['PRate'],
                test_24=attribute['Test24'],
                test_7=attribute['Test7'],
                positive_7=attribute['Pos7'],
                positive_rate_7=attribute['PosR7'],
                fid=attribute['FID']
            )
            data.append(swab.__dict__)

        return data
