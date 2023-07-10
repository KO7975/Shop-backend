import requests

def get_rate(currency) -> float:
    url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
    data = requests.get(url=url).json()
    currency_rate = [i['rate'] for i in data if i['cc'] == f'{currency}'][0]
    return currency_rate
