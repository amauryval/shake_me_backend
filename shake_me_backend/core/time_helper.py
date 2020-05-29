import calendar
import datetime
from dateutil.relativedelta import relativedelta


class DatesToMonthDates:

    __ALL_DATES_FOUND = []
    __DAY_INCREMENT = relativedelta(days=1)
    __MONTH_INCREMENT = relativedelta(months=1)

    def __init__(self, start_date, end_date):

        self._start_date = datetime.datetime.fromisoformat(start_date)
        self._end_date = datetime.datetime.fromisoformat(end_date)

    def run(self):

        date = self._start_date
        while date < self._end_date:

            last_day_current_month = self._find_the_last_month_day_from_date(date)
            self.__ALL_DATES_FOUND.append([date , last_day_current_month])

            date = last_day_current_month + self.__DAY_INCREMENT

        return self.__ALL_DATES_FOUND

    def _find_the_last_month_day_from_date(self, date):
        first_day_next_month = datetime.datetime(date.year, date.month, 1) + self.__MONTH_INCREMENT
        last_day_current_month = first_day_next_month - self.__DAY_INCREMENT

        if last_day_current_month >= self._end_date:
            last_day_current_month = self._end_date

        return last_day_current_month



if __name__ == '__main__':
    a = Testdate("2000-01-06", "2001-01-09").run()
    assert True