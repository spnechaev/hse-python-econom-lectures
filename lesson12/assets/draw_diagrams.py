#!/usr/bin/env python3
"""Пересоздать пять SVG-схем лекции12, без сторонних библиотек."""
from html import escape
from math import hypot
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INK = '#243247'
BLUE = '#32667d'
GREEN = '#2c6b52'
RED = '#a34d38'
GOLD = '#93691d'

def text(x, y, value, size=22, color=INK, weight='400', anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>'

def box(x, y, w, h, lines, color=BLUE, fill='#edf3f7'):
    body=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{color}" stroke-width="2"/>'
    for i,line in enumerate(lines):
        body+=text(x+18,y+33+i*29,line,23 if i==0 else 19,color if i==0 else INK,'600' if i==0 else '400')
    return body

def arrow(x1,y1,x2,y2,color=BLUE):
    distance = hypot(x2-x1,y2-y1)
    dx,dy = (x2-x1)/distance,(y2-y1)/distance
    bx,by = x2-12*dx,y2-12*dy
    points = f"{x2},{y2} {bx-6*dy},{by+6*dx} {bx+6*dy},{by-6*dx}"
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{color}" stroke-width="3"/><polygon points="{points}" fill="{color}"/>'

def save(name,title,desc,body,height):
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="{height}" viewBox="0 0 1120 {height}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="context-stroke"/></marker></defs><rect width="1120" height="{height}" rx="18" fill="#fcfbf7"/><g font-family="Arial, Helvetica, sans-serif">{body}</g></svg>\n'''
    (ROOT/name).write_text(svg,encoding='utf-8')

def main():
    b=text(35,47,'Сначала строки событий, затем месячные расходы',29,weight='600')
    b+=box(35,85,310,100,['transactions.csv','117 исходных событий'])
    b+=box(405,85,310,100,['products.csv','4 уникальных товара'])
    b+=box(775,85,310,100,['advertising.csv','6 пар «месяц + канал»'])
    b+=arrow(190,185,220,290)+arrow(560,185,530,290)
    b+=box(35,300,680,110,['Проверить и посчитать товарные строки','3 повтора, 8 отказов и 6 отмен — отдельно','100 принятых событий для расчёта'],GREEN,'#edf5ed')
    b+=arrow(245,410,245,490)
    b+=box(35,500,400,100,['Свод продаж','5 пар «месяц + канал»'])
    b+=arrow(435,550,495,550)
    b+=box(505,500,580,100,['Свод + реклама → 6 групп','Расход без продаж тоже остаётся','По нему и собираем два месячных итога'],GREEN,'#edf5ed')
    b+=arrow(930,185,930,490)
    b+=text(35,657,'Сумму месячного бюджета нельзя повторять у каждой проданной вещи.',22,RED)
    save('data-to-report.svg','Уровни данных и порядок расчёта','События соединяются с товарами после проверок. Реклама присоединяется только к своду по месяцу и каналу; группа без продаж сохраняется.',b,695)

    b=text(35,47,'Соединение может размножить строки — и деньги',29,weight='600')
    b+=text(35,97,'Справа ключ уникален',23,GREEN,weight='600')
    b+=box(35,120,265,110,['Две продажи','A → товар 001','B → товар 001'])
    b+=arrow(305,175,355,175)
    b+=box(365,120,305,110,['Одна строка товара','001 → стоимость 1500'])
    b+=arrow(675,175,725,175)
    b+=box(735,120,350,110,['Две строки результата','Каждая нашла одну цену'],GREEN,'#edf5ed')
    b+=text(35,301,'Справа один ключ встречается дважды',23,RED,weight='600')
    b+=box(35,325,265,110,['Две продажи','A → товар 001','B → товар 001'])
    b+=arrow(305,380,355,380)
    b+=box(365,325,305,110,['Две строки товара','001 → стоимость 1500','001 → стоимость 1500'],RED,'#faefea')
    b+=arrow(675,380,725,380,RED)
    b+=box(735,325,350,110,['Без проверки: 4 строки','Каждая продажа удвоилась'],RED,'#faefea')
    b+=text(35,492,'validate="many_to_one" останавливает второй случай до расчёта.',24,GREEN)
    b+=text(35,535,'Но даже уникальный месячный расход нельзя суммировать у товарных строк.',20,RED)
    save('merge-cardinality.svg','Число совпадений при merge','Две продажи и одна строка товара дают две строки. Две строки того же товара справа дали бы четыре; validate many_to_one отклоняет такой справочник.',b,575)

    b=text(35,47,'Что именно должно иметь одинаковый вес?',29,weight='600')
    b+=box(35,90,500,100,['Одна строка: 1 лампа по 1200 руб.','Другая строка: 5 кабелей по 400 руб.'])
    b+=box(585,90,500,100,['Среднее по двум строкам','(1200 + 400) / 2 = 800 руб.'],GOLD,'#f8f2e3')
    b+=text(35,248,'Цена одной проданной единицы',25,GREEN,weight='600')
    for i in range(6):
        x=35+i*175
        fill='#f4e8d4' if i==0 else '#e4eef4'
        b+=box(x,280,150,95,['Лампа' if i==0 else 'Кабель','1200 руб.' if i==0 else '400 руб.'],GOLD if i==0 else BLUE,fill)
    b+=text(35,435,'(1 × 1200 + 5 × 400) / (1 + 5) = 533,33… руб.',28,GREEN,weight='600')
    b+=text(35,488,'Теперь каждая из шести проданных вещей имеет одинаковый вес.',22)
    b+=text(35,531,'При изменении состава продаж эта средняя меняется даже без изменения цен.',20,RED)
    save('weighted-price.svg','Средняя цена строки и средняя цена единицы','Среднее двух строк равно800рублям, но средняя цена одной из шести проданных единиц равна533,33рубля. Веса определяются смыслом показателя.',b,570)

    b=text(35,47,'Метки и позиции — два разных правила',29,weight='600')
    b+=box(35,90,285,130,['left','А →100','Б →200'])
    b+=box(415,90,285,130,['right','Б →10','А →20'])
    b+=box(795,90,290,130,['pandas: по меткам','А →100 +20 =120','Б →200 +10 =210'],GREEN,'#edf5ed')
    b+=text(365,166,'+',34,anchor='middle')+arrow(705,155,785,155)
    b+=text(35,290,'После to_numpy() у чисел больше нет подписей строк',24,RED,weight='600')
    b+=box(35,330,285,110,['[100,200]','Тот же порядок left'])
    b+=box(415,330,285,110,['[10,20]','Тот же порядок right'])
    b+=box(795,330,290,110,['NumPy: по позициям','[110,220]'],RED,'#faefea')
    b+=text(365,396,'+',34,anchor='middle')+arrow(705,385,785,385,RED)
    b+=text(35,502,'Одинаковая длина не доказывает соответствие клиентов, товаров или дат.',22)
    save('index-alignment.svg','Выравнивание Series и позиционные массивы','Series сопоставляет метки А и Б. После удаления индексов NumPy складывает числа на одинаковых позициях, что даёт другой результат.',b,545)

    b=text(35,47,'Broadcasting: скидки по строкам, объёмы по столбцам',28,weight='600')
    b+=box(35,95,285,155,['Скидки (3, 1)','0%','5%','10%'])
    b+=box(370,95,715,100,['Объёмы (1, 3)','100, 110, 130 штук'])
    b+=text(35,282,'Результат (3, 3)',24,GREEN,weight='600')
    for i, quantity in enumerate([100,110,130]):
        b+=text(375+i*280,282,f'{quantity} шт.',22,anchor='middle')
    values=[[8000,8800,10400],[6000,6600,7800],[4000,4400,5200]]
    for row in range(3):
        b+=text(75,341+row*85,f'{[0,5,10][row]}%',24,weight='600')
        for col in range(3):
            x=250+col*280;y=300+row*85
            fill='#edf5ed' if values[row][col]>=8000 else '#f8eee8'
            b+=box(x,y,250,65,[f'{values[row][col]:,} руб.'.replace(',',' ')],GREEN if values[row][col]>=8000 else RED,fill)
    b+=text(35,604,'В каждой клетке: количество × (цена после скидки − стоимость товара).',22)
    b+=text(35,647,'Это заданные сценарии, а не прогноз спроса. Другие расходы здесь не вычтены.',21,RED)
    save('broadcast-scenarios.svg','Сетка скидок и объёмов','Столбец трёх скидок и строка трёх объёмов дают девять сочетаний. Цвет показывает, сохраняется ли исходная маржа 8000рублей до рекламы и прочих расходов.',b,690)
    print('Созданы5SVG-схем')

if __name__=='__main__':main()
