import requests
import smtplib


class Stock_Monitor:
    def __init__(self):
        self.USER = 'thegreatdeepakpoudel@gmail.com'
        self.PASS = 'DeepaK1236'
        self.percentage = 0
        self.number_of_news = 2
        self.stock_change = ''
        self.news = ''
        self.news_data_collection = {}
        self.API_STOCK_KEY = 'AHKI4626SVGRRVVZ'
        self.API_PRICE = 'https://www.alphavantage.co/query'
        self.STOCK_LIST = ['TSLA', "AMC", "GME", 'AMZN']
        self.STOCK = ''
        self.stock_parameters = {
            "apikey": self.API_STOCK_KEY,
            "function": "TIME_SERIES_DAILY",
            "interval": "60min",

        }
        self.API_NEWS_KEY = 'cdffc0c0aed14518ac29eb11fa48940c'
        self.API_NEWS_DATA = 'https://newsapi.org/v2/everything'

        self.news_parameters = {
            "apikey": self.API_NEWS_KEY,
        }

    def set_parameters(self, stock):
        self.STOCK = stock
        self.stock_parameters['symbol'] = stock
        self.news_parameters['q'] = stock

    def stock_price_finder(self):
        stock_history = requests.get(url=self.API_PRICE, params=self.stock_parameters)
        data = stock_history.json()
        req_data = data['Time Series (Daily)']
        dates = []
        for data in req_data:
            dates.append(data)

        today = dates[0]
        yesterday = dates[1]
        tod_data_close = float(req_data[today]['4. close'])
        yes_data_close = float(req_data[yesterday]['4. close'])
        self.percentage = (((tod_data_close - yes_data_close) / yes_data_close) * 100).__round__(2)

    def get_news(self):
        news_response = requests.get(url=self.API_NEWS_DATA, params=self.news_parameters)
        news_data = news_response.json()
        self.news = (f"Subject: STOCK ALERT!! {self.STOCK}\n\n\n"
                     f"    {self.STOCK}: {self.stock_change}\n")
        for i in range(self.number_of_news):
            self.news += (f"    Headline: {news_data['articles'][i]['title'] }\n"
                          f"    Brief: {news_data['articles'][i]['description']}\n"
                          f"  -------------------------\n ")

    def send_news(self):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=self.USER, password=self.PASS)
            message = self.news
            connection.sendmail(from_addr=self.USER, to_addrs='dipupoudel1@gmail.com', msg=message.encode("utf-8"))
            connection.close()
