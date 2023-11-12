from datetime import date, timedelta
from pprint import pprint
import aiohttp
import asyncio
import logging

sale_purchase_dictUSD = {}
sale_purchase_dictEUR = {}
resultUSD = {}
resultEUR = {}
currency_list = []
result_currency = {}

def build_currency_dictUSD(res_list):
    for dict in res_list:
        currency = dict['currency']
        sale = dict['saleRate']
        purchase = dict['purchaseRate']
        sale_purchase_dictUSD['sale'] = sale
        sale_purchase_dictUSD['purchase'] = purchase
        resultUSD[currency] = sale_purchase_dictUSD
    return resultUSD

def build_currency_dictEUR(res_list):
    for dict in res_list:
        currency = dict['currency']
        sale = dict['saleRate']
        purchase = dict['purchaseRate']
        sale_purchase_dictEUR['sale'] = sale
        sale_purchase_dictEUR['purchase'] = purchase
        resultEUR[currency] = sale_purchase_dictEUR
    return resultEUR


async def request(url):

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    r = await response.json()
                    return r
        except aiohttp.ClientConnectionError as e:
            logging.error(f'Connection error {url}: {e}')
        return None

async def get_exchange():
    while True:
        try:
            user_input =input('Введите количество за которое хотите посмотреть курс валют -> ')
            if int(user_input) <= 10:
                break
            text = 'Количество дней не может быть больше 10'
            print(text)
        except ValueError as err:
            print(f'{err}: Введите целое число')
    rng = int(user_input)
    string = 'https://api.privatbank.ua/p24api/exchange_rates?date='
    for i in range(rng):
        currency_list.clear()
        today = date.today()
        last_day = today - timedelta(i)
        day = "{}.{}.{}".format(last_day.day, last_day.month, last_day.year)
        if len(day) == 9:
            day = '0' + "{}.{}.{}".format(last_day.day, last_day.month, last_day.year)
        url_new = "{}{}".format(string, day)
        res = await request(url_new)
        res_list = res.get('exchangeRate')
        res_list_USD =list(filter(lambda x: x['currency'] == 'USD', res_list))
        result_USD = build_currency_dictUSD(res_list_USD)
        currency_list.append(result_USD)
        result_currency[day] = result_USD
        res_list_EUR =list(filter(lambda x: x['currency'] == 'EUR', res_list))
        result_EUR = build_currency_dictEUR(res_list_EUR)
        currency_list.append(result_EUR )
        result_currency[day] = currency_list
    return result_currency                     


if __name__=="__main__":
    r = asyncio.run(get_exchange())
    pprint(r, width= 1)