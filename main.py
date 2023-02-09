import time
import threading
from datetime import datetime
from binance.cm_futures import CMFutures


def get_price(client: CMFutures = None,
              symbol: str = None, price_percent: float = 0) -> float:
    """
    Получение цены для пары
    """
    price = float(client.ticker_price(symbol)[0].get('price'))
    if price < price_percent:
        return price


def get_index_max_price(client: CMFutures,
                        symbol: str = None, time: int = None) -> float:
    """
    Получение индекса для пары за последний час
    """
    # Вычисляем пару из символа
    pair = symbol.split('_')[0]

    # Получаем индексы цен за последний час
    index_price = client.index_price_klines(symbol=symbol,
                                            pair=pair,
                                            interval='1h',
                                            endTime=time)[::-1]

    return float(index_price[1][2])


def price_percent_deviation(price: float = 0, percent: float = 0) -> float:
    """
    Вычисляем цену таргета по проценту
    """
    return price + (price * percent) / 100


def main(symbol: str = None, percent: float = 0):
    # Инициализируем клиент
    client = CMFutures()

    # Получаем время сервера
    server_time = client.time().get('serverTime')

    # Получаем максимальную цену за час
    max_price = get_index_max_price(client=client,
                                    symbol=symbol, time=server_time)

    # Получаем цену отличную на указанный процент
    price_percent = price_percent_deviation(max_price, percent)

    print('Server time:', datetime.utcfromtimestamp(server_time / 1000)
          .strftime('%Y-%m-%d %H:%M:%S'))
    print('Index maximum price: ', max_price)
    print('Deviation price: ', price_percent)

    while True:
        price = get_price(client, symbol, price_percent)
        if price:
            print(f"The bidding price changed by {price} !")
        if event.is_set():
            print('thread end')
            event.clear()
            break


if __name__ == '__main__':
    pair = 'XRPUSD_PERP'
    percent = -1
    event = threading.Event()
    while True:
        thread = threading.Thread(target=main,
                                  name='thread',
                                  args=(pair, percent,))
        thread.start()
        time.sleep(3600)
        event.set()
        thread.join()
