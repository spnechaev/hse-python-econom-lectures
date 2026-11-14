#!/usr/bin/env python3
"""Пересоздать синтетические CSV для лекции 12. Сеть и библиотеки не нужны."""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIELDS = [
    "event_id", "date", "order_id", "product_id", "channel", "event",
    "units", "unit_price_kopecks",
]


def write_csv(name, fields, rows):
    with (ROOT / name).open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    products = [
        {"product_id": "001", "product_name": "чайник", "unit_cost_kopecks": "150000"},
        {"product_id": "002", "product_name": "кабель", "unit_cost_kopecks": "32000"},
        {"product_id": "003", "product_name": "лампа", "unit_cost_kopecks": "65000"},
        {"product_id": "004", "product_name": "кружка", "unit_cost_kopecks": "12000"},
    ]
    rows = []

    def add(month, day, order, product, channel, event, units, price):
        row = dict(zip(FIELDS, [
            f"{len(rows) + 1:06d}", f"2026-{month:02d}-{day:02d}", order,
            product, channel, event, str(units), str(price),
        ]))
        rows.append(row)
        return row

    # Январь: основную выручку дают чайники, в соцсетях продаются лампы.
    january_kettles = [add(1, i + 1, f"01{i + 1:04d}", "001", "поиск", "sale", 1, 240000) for i in range(20)]
    january_lamps = [add(1, i + 5, f"01{i + 1:04d}", "003", "соцсети", "sale", 2, 120000) for i in range(10)]
    january_mugs = [add(1, i + 10, f"01{i + 11:04d}", "004", "прямой", "sale", 3, 30000) for i in range(10)]

    for day, sale in zip([25, 26, 27], [january_kettles[0], january_lamps[0], january_mugs[0]]):
        add(1, day, sale["order_id"], sale["product_id"], sale["channel"], "return", sale["units"], sale["unit_price_kopecks"])
    for i, product in enumerate(["001", "002", "003"]):
        add(1, 28, f"0190{i + 1:02d}", product, "поиск", "cancelled", 1, 100000)

    # Февраль: больше дешёвых кабелей, выше рекламные затраты и возвраты.
    february_kettles = [add(2, i + 1, f"02{i + 1:04d}", "001", "поиск", "sale", 1, 240000) for i in range(20)]
    february_cables = [add(2, i + 2, f"02{i + 1:04d}", "002", "поиск", "sale", 5, 40000) for i in range(20)]
    february_mugs = [add(2, i + 10, f"02{i + 21:04d}", "004", "прямой", "sale", 3, 30000) for i in range(10)]
    add(2, 10, february_mugs[0]["order_id"], "004", "прямой", "sale", 1, 0)

    returns = february_kettles[:3] + february_cables[:2] + february_mugs[:1]
    for i, sale in enumerate(returns):
        add(2, 23 + i % 5, sale["order_id"], sale["product_id"], sale["channel"], "return", sale["units"], sale["unit_price_kopecks"])
    for i, product in enumerate(["001", "002", "004"]):
        add(2, 28, f"0290{i + 1:02d}", product, "соцсети", "cancelled", 1, 100000)

    assert len(rows) == 106

    # Пересекающиеся выгрузки дали три повтора. Один отличается пробелами,
    # которые по договору удаляются до поиска точных повторов.
    duplicate = rows[0].copy()
    duplicate["channel"] = " поиск "
    duplicate["units"] = " 1 "
    rows.extend([duplicate, rows[29].copy(), rows[73].copy()])

    # Один идентификатор, но две разные цены. Обе версии нужно отложить.
    conflict = dict(zip(FIELDS, ["009000", "2026-01-15", "009000", "002", "поиск", "sale", "1", "40000"]))
    rows.append(conflict)
    rows.append({**conflict, "unit_price_kopecks": "45000"})

    # Шесть разных отказов: каждый оставляет понятный след в журнале.
    bad_base = dict(zip(FIELDS, ["", "2026-02-18", "009100", "001", "поиск", "sale", "1", "240000"]))
    defects = [
        {"date": "2026-02-30"},
        {"units": ""},
        {"units": "1.5"},
        {"product_id": "999"},
        {"unit_price_kopecks": "-100"},
        {"event": "reserve"},
    ]
    for i, defect in enumerate(defects, start=1):
        rows.append({**bad_base, "event_id": f"00910{i}", **defect})

    advertising = [
        {"month": "2026-01", "channel": "поиск", "ad_spend_kopecks": "800000"},
        {"month": "2026-01", "channel": "соцсети", "ad_spend_kopecks": "300000"},
        {"month": "2026-01", "channel": "прямой", "ad_spend_kopecks": "0"},
        {"month": "2026-02", "channel": "поиск", "ad_spend_kopecks": "1800000"},
        {"month": "2026-02", "channel": "соцсети", "ad_spend_kopecks": "400000"},
        {"month": "2026-02", "channel": "прямой", "ad_spend_kopecks": "0"},
    ]
    write_csv("transactions.csv", FIELDS, rows)
    write_csv("products.csv", ["product_id", "product_name", "unit_cost_kopecks"], products)
    write_csv("advertising.csv", ["month", "channel", "ad_spend_kopecks"], advertising)
    print(f"Созданы три CSV: {len(rows)} строк событий, {len(products)} товаров, {len(advertising)} строк рекламы.")


if __name__ == "__main__":
    main()
