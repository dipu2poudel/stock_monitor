from stock_moniter import Stock_Monitor

monitor = Stock_Monitor()

for stock in monitor.STOCK_LIST:
    monitor.set_parameters(stock)
    monitor.stock_price_finder()
    if monitor.percentage >= 0:
        monitor.stock_change = f'🔺{monitor.percentage}%'
    else:
        monitor.stock_change = f'🔻{monitor.percentage * -1}%'
    monitor.get_news()
    monitor.send_news()
