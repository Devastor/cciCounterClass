from datetime import datetime

# Класс для подсчета индикатора CCI
class CCICounter:

    # Константы
    PERIOD = 300        # Период (сек.) для построения свечей
    LONG_PERIOD = 3000  # Временной интервал (сек.) большого периода для индекса CCI

    def __init__(self):
        self.prices = []            # Массив цен за PERIOD
        self.typical_price = []     # Массив типичных цен за PERIOD
        self.typical_price_avg = [] # Скользящая средняя цен за LONG_PERIOD
        self.mean_deviation = []    # Станд. отклонение ТЦ от СС за LONG_PERIOD
        self.cci_value = []         # Массив значений CCI за LONG_PERIOD
        self.num_period = 0         # Номер текущего LONG_PERIOD
        self.num_small_period = 0   # Номер текущего PERIOD

    # Метод сдвига массива на x элементов влево
    #  с удалением первого элемента
    #  чтобы сдвинуть вправо, необходимо
    #  указать отрицательно число
    def shiftArray(self, lst, steps):
        if steps < 0:
            steps = abs(steps)
            for i in range(steps):
                lst.append(lst.pop(0))
        else:
            for i in range(steps):
                lst.insert(0, lst.pop())
        return lst

    # По окончании PERIOD
    def newSmallPeriodSetup(self):
        # Очищаем массив цен
        self.prices.clear()

        self.num_small_period += 1

    # По окончании LONG_PERIOD
    def newLongPeriodSetup(self):
        # Обнуляем данные по массиву цен
        # self.num_small_period = 0

        # Удаляем первый элемент из массивов
        #  завязанных на LONG_PERIOD и
        #  сдвигаем соответствующие массивы на 1 влево
        self.shiftArray(self.typical_price, 1)
        self.shiftArray(self.typical_price_avg, 1)
        self.shiftArray(self.mean_deviation, 1)
        self.shiftArray(self.cci_value, 1)

        # Увеличиваем счетчик LONG_PERIOD на 1
        self.num_period += 1

    # Добавляем текущую цену закрытия в массив цен за PERIOD
    def addPrice(self, element):
        self.prices.append(element)
        log('Цена ', element, ' добавлена в массив цен')

    # Добавляем типичную цену за PERIOD в массив типичных цен
    def addTypicalPrice(self, element):
        self.typical_price.append(element)
        log('Типичная цена ', element, ' добавлена в массив типичных цен')

    # Добавляем среднюю типичную цену в массив ср. типичных цен
    def addTypicalPriceAvg(self, element):
        self.typical_price_avg.append(element)
        log('Типичная средняя цена ', element,
            ' добавлена в массив типичных средних цен')

    # Добавляем стандартное отклонение за LONG_PERIOD в массив ст. откл-ий
    def addMeanDeviation(self, element):
        self.mean_deviation.append(element)
        log('Станд. отклонение ', element, ' добавлено в массив станд. отклонений')

    # Добавляем рассчитанное за LONG_PERIOD значение CCI в массив cci
    def addCCIValue(self, element):
        self.cci_value.append(element)
        log('Значение CCI ', element, ' добавлено в массив индикатора CCI')

    # Функция подсчета типичной цены
    def countTypicalPrice(self):
        log('Расчет типичной цены...')
        close = self.prices[len(self.prices) - 1]
        high = max(self.prices)
        low = min(self.prices)

        return (float(high) + float(low) + float(close)) / 3

    # Функция подсчета средней типичной цены
    def countAvgTypicalPrice(self):
        log('Расчет средней типичной цены...')
        avg_price = 0
        for i in range (0, int(self.LONG_PERIOD / self.PERIOD)):
            avg_price += self.typical_price[i]

        avg_price = avg_price / int(self.LONG_PERIOD / self.PERIOD)

        return avg_price

    # Функция подсчета стандартного отклонения за period_num
    def countMeanDeviation(self, period_num):
        log('Расчет стандартного отклонения...')
        mean_dev = 0
        for i in range(0, int(self.LONG_PERIOD / self.PERIOD)):
            mean_dev += abs(self.typical_price[i] - self.typical_price_avg[period_num])

        return mean_dev / int(self.LONG_PERIOD / self.PERIOD)

    # Функция подсчета cci индикатора за period_num
    def countCCI(self, period_num):
        log('Расчет cci...')
        cci = (self.typical_price[period_num] - self.typical_price_avg[period_num]) /\
              (0.015 * self.mean_deviation[period_num])

        return cci


# Выводит всякую информацию на экран и пишет в файл log.txt
def log(*args):
    l = open("log.txt", 'a', encoding='utf-8')
    print(datetime.now(), *args, file=l)
    l.close()
