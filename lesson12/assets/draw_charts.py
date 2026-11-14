#!/usr/bin/env python3
"""Построить иллюстрацию контрольных итогов учебного кейса.

Расчёт CSV показан в lecture.ipynb. Здесь читаются уже независимо проверенные
контрольные итоги expected.json: скрипт нужен для пересоздания файлов картинки,
а не является программой анализа произвольной новой выгрузки.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent


def main():
    expected = json.loads((ROOT.parent / 'data' / 'expected.json').read_text(encoding='utf-8'))
    monthly = expected['monthly']
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), layout='constrained')
    months = [row['month'] for row in monthly]
    plots = [('revenue_kopecks', 'Выручка принятых событий', '#376b84'),
             ('after_ads_kopecks', 'После товара и рекламы', '#a45535')]
    for ax, (column, title, color) in zip(axes, plots):
        values = [row[column] / 100 for row in monthly]
        bars = ax.bar(months, values, color=color, width=.55)
        ax.set_title(title)
        ax.set_ylabel('рубли')
        ax.set_ylim(0, max(values) * 1.18)
        ax.spines[['top', 'right']].set_visible(False)
        ax.bar_label(bars, labels=[f'{value:,.0f}'.replace(',', ' ') for value in values], padding=5)
    target = ROOT / 'charts'
    target.mkdir(exist_ok=True)
    fig.savefig(target / 'monthly-result.png', dpi=160)
    fig.savefig(target / 'monthly-result.svg', metadata={'Date': None})
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), layout='constrained')
    fig.suptitle('Февраль вырос. Увеличиваем бюджет?', fontsize=17, fontweight='bold')
    opening_plots = [
        ('units', 'Продано минус возвращено', 'штуки', 1, '#376b84'),
        ('revenue_kopecks', 'Выручка', 'рубли', 100, '#42785b'),
    ]
    for ax, (column, title, unit, divisor, color) in zip(axes, opening_plots):
        values = [row[column] / divisor for row in monthly]
        growth = (values[1] / values[0] - 1) * 100
        ax.set_title(f'{title}: +{growth:.1f}%'.replace('.', ','))
        bars = ax.bar(months, values, color=color, width=.55)
        ax.set_ylabel(unit)
        ax.set_ylim(0, max(values) * 1.18)
        ax.spines[['top', 'right']].set_visible(False)
        ax.bar_label(bars, labels=[f'{value:,.0f}'.replace(',', ' ') for value in values], padding=5)
    fig.supxlabel('Предварительная сводка по 100 принятым событиям. Расходы здесь не показаны.', fontsize=10)
    fig.savefig(target / 'opening-dashboard.png', dpi=160)
    fig.savefig(target / 'opening-dashboard.svg', metadata={'Date': None})
    plt.close(fig)
    print('Созданы charts/monthly-result и charts/opening-dashboard в PNG и SVG')


if __name__ == '__main__':
    main()
