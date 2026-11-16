"""2026 check of the 2023 forecast against the three years published since.

Run: python check_forecast.py
Needs only the standard library.
"""
import csv
from collections import defaultdict

TRAIN = ["2011-12", "2012-13", "2013-14", "2014-15", "2015-16", "2016-17",
         "2017-18", "2018-19", "2019-20", "2020-21", "2021-22"]
TEST = ["2022-23", "2023-24", "2024-25"]


def yearly_average(path="data/fly-tipping-borough.csv"):
    """Average enforcement actions per London authority, by year (what the Power BI visual passed to R)."""
    values = defaultdict(list)
    with open(path, encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            raw = row["total_action_taken"].replace(",", "").strip()
            if raw.isdigit():                      # ":" marks a missing return
                values[row["year"]].append(int(raw))
    return {year: sum(v) / len(v) for year, v in values.items()}


def drift_forecast(series, steps):
    """Random walk with drift, the model auto.arima picked: last value plus the average yearly change."""
    drift = (series[-1] - series[0]) / (len(series) - 1)
    return [series[-1] + drift * h for h in range(1, steps + 1)]


def mape(forecast, actual):
    return 100 * sum(abs(f - a) / a for f, a in zip(forecast, actual)) / len(actual)


avg = yearly_average()
history = [avg[y] for y in TRAIN]
actual = [avg[y] for y in TEST]

# The 2023 R scripts never sorted the rows by year. The values on the original charts
# (5,790 falling to 3,748) are the yearly averages ordered from largest to smallest.
as_modelled_2023 = sorted(history, reverse=True)

forecasts = {
    "2023 model (values not in year order)": drift_forecast(as_modelled_2023, 3),
    "Same model, years in order": drift_forecast(history, 3),
    "Baseline: repeat the last year": [history[-1]] * 3,
}

# self-check: the mis-ordered series reproduces the end points on the original charts
assert round(as_modelled_2023[0]) == 5790 and round(as_modelled_2023[-1]) == 3748
assert round(drift_forecast(as_modelled_2023, 10)[-1], -2) == 1700   # chart ends near 1,700 in 2031

print(f"{'':40}" + "".join(f"{y:>10}" for y in TEST) + f"{'MAPE':>8}")
print(f"{'Actual':40}" + "".join(f"{a:>10,.0f}" for a in actual))
for name, fc in forecasts.items():
    print(f"{name:40}" + "".join(f"{v:>10,.0f}" for v in fc) + f"{mape(fc, actual):>7.1f}%")
