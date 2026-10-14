"""Rebuild the sorting lecture's vector diagrams using only the standard library.

Run: python3 lesson06/assets/draw_diagrams.py
"""
from html import escape
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent
INK, BLUE, GREEN, ORANGE = '#203047', '#2764b7', '#197568', '#b66b13'


class Diagram:
    def __init__(self, title, subtitle, height=600):
        self.parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img">', f'<title>{escape(title)}</title><desc>{escape(subtitle)}</desc>', '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="#63768b"/></marker></defs>', '<style>text{font-family:Arial,DejaVu Sans,sans-serif}.mono{font-family:Menlo,DejaVu Sans Mono,monospace}</style>', f'<rect width="1200" height="{height}" rx="20" fill="#f5f7fb"/>']
        self.text(40, 52, title, 30, bold=True)
        self.text(40, 88, subtitle, 20)

    def text(self, x, y, s, size=22, color=INK, bold=False, mono=False, anchor='start'):
        self.parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{700 if bold else 400}" text-anchor="{anchor}" class="{"mono" if mono else ""}">{escape(str(s))}</text>')

    def box(self, x, y, w, h, fill='#ffffff', stroke='#cdd7e4'):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')

    def arrow(self, x1, y1, x2, y2, label=None):
        self.parts.append(f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="#63768b" stroke-width="2.3" marker-end="url(#arrow)"/>')
        if label:
            self.text((x1+x2)/2+10, (y1+y2)/2-8, label, 18, color=BLUE)

    def row(self, x, y, values, active=(), fixed=(), width=64):
        for i, value in enumerate(values):
            fill = '#dbf0e8' if i in fixed else '#fff0d8' if i in active else '#ffffff'
            self.box(x+i*(width+10), y, width, 46, fill)
            self.text(x+i*(width+10)+width/2, y+31, value, 24, anchor='middle', mono=True)

    def card(self, x, y, w, lines, color=BLUE):
        self.box(x, y, w, 38+34*len(lines))
        for i, line in enumerate(lines):
            self.text(x+18, y+34+i*34, line, 21, color=color if i==0 else INK, bold=i==0)

    def save(self, filename):
        xml='\n'.join(self.parts+['</svg>'])+'\n'
        ElementTree.fromstring(xml)
        (HERE/filename).write_text(xml, encoding='utf-8')


def purpose():
    d=Diagram('Один набор участников — разные вопросы', 'Сортировка меняет порядок записей. Поля внутри записи остаются вместе.', 580)
    for x, title, records in [(40,'Порядок регистрации',[('Вера',80),('Аня',95),('Борис',80),('Глеб',90)]),(440,'Баллы по убыванию',[('Аня',95),('Глеб',90),('Вера',80),('Борис',80)]),(840,'Имена по алфавиту',[('Аня',95),('Борис',80),('Вера',80),('Глеб',90)])]:
        d.text(x,145,title,22,color=BLUE,bold=True)
        for j,(name,score) in enumerate(records):
            d.box(x,170+j*75,320,58)
            d.text(x+20,207+j*75,name)
            d.text(x+225,207+j*75,str(score),color=GREEN,mono=True)
    d.text(40,540,'Рейтинг отвечает «кто набрал больше?», алфавит помогает найти имя.',22)
    d.save('sorting-purpose.svg')


def bubble():
    d=Diagram('Пузырёк: весь первый проход', 'Сравниваем соседей слева направо. Если левый больше — меняем их местами.', 650)
    rows=[([5,1,4,2,3],(0,1),'5 > 1 → обмен'),([1,5,4,2,3],(1,2),'5 > 4 → обмен'),([1,4,5,2,3],(2,3),'5 > 2 → обмен'),([1,4,2,5,3],(3,4),'5 > 3 → обмен'),([1,4,2,3,5],(),'Максимум уже на своём месте')]
    for j,(values,active,label) in enumerate(rows):
        y=135+j*88
        d.text(45,y+30,'Старт' if j==0 else f'После {j}',20)
        d.row(170,y,values,active,fixed=(4,) if j==4 else ())
        d.text(600,y+30,label,22,color=GREEN if j==4 else ORANGE)
        if j<4: d.arrow(350,y+49,350,y+79)
    d.text(40,608,'Остальная часть ещё не отсортирована: 4 стоит перед 2. Нужны следующие проходы.',20)
    d.save('bubble-pass.svg')
    d=Diagram('Работа пузырька: уменьшаем несортированную часть', 'Для n = 5 верхняя граница — 4 + 3 + 2 + 1 = 10 сравнений.',620)
    for j,count in enumerate([4,3,2,1]):
        y=145+j*75
        d.text(40,y+30,f'Проход {j+1}',21)
        for i in range(4):
            d.box(200+i*75,y,60,44,'#dce8fa' if i<count else '#edf0f5')
            if i<count: d.text(230+i*75,y+29,'?',22,anchor='middle',color=BLUE)
        d.text(540,y+29,f'{count} сравнений',21)
    d.card(785,145,370,['В общем случае','(n − 1) + … + 1','n(n − 1) / 2','Худший случай: O(n²)'])
    d.box(40,477,1120,97,'#dbf0e8')
    d.text(60,514,'Ни одного обмена за проход? Можно закончить.',23,color=GREEN,bold=True)
    d.text(60,549,'Уже отсортированный список: один проход, n − 1 сравнений, O(n).',21)
    d.save('bubble-work.svg')


def quicksort():
    d=Diagram('Quicksort: одно разбиение по опорному', 'Опорный элемент — 3. Здесь внутри каждой группы сохраняем исходный порядок.',520)
    d.row(325,135,[5,2,5,1,4,3],active=(5,))
    for x,label,vals in [(70,'Меньше 3',[2,1]),(470,'Равны 3',[3]),(870,'Больше 3',[5,5,4])]:
        d.arrow(585,200,x+120,265)
        d.text(x,305,label,24,color=BLUE,bold=True)
        d.row(x,330,vals)
    d.text(70,448,'Сортируем рекурсивно',20)
    d.text(470,448,'Уже готовы',20,color=GREEN)
    d.text(870,448,'Сортируем рекурсивно',20)
    d.save('quicksort-partition.svg')
    d=Diagram('Quicksort: глубина зависит от разбиений', 'Полоски показывают размеры подзадач; для схемы пренебрегаем уже выделенными опорными.',640)
    d.text(40,140,'Разбиения примерно пополам',23,color=GREEN,bold=True)
    d.text(650,140,'Отделяется только один элемент',23,color=ORANGE,bold=True)
    for level in range(4):
        y=170+level*66
        count=2**level
        for j in range(count):
            w=500/count-6
            d.box(40+j*500/count,y,w,34,'#dbf0e8')
        d.box(650,y,460-level*65,34,'#fff0d8')
        d.text(1130,y+25,['n','n − 1','n − 2','…'][level],18,anchor='end')
    d.card(40,455,510,['Около log n уровней','Суммарно O(n) работы на уровень','Итого O(n log n)'],GREEN)
    d.card(650,455,510,['До n уровней','n + (n − 1) + … + 1','Итого O(n²)'],ORANGE)
    d.save('quicksort-levels.svg')


def quicksort_return():
    d=Diagram('Quicksort: вызовы возвращают готовые части', 'Для ручной трассировки фиксируем опорные. В программе опорный выбирается случайно.',800)
    d.box(40,125,540,355)
    d.text(60,160,'1. quick_sort([2, 1]), опорный 1',23,color=BLUE,bold=True)
    d.text(60,202,'Разбиение: []    [1]    [2]',23,mono=True)
    d.arrow(165,220,165,265)
    d.arrow(440,220,440,265)
    d.text(80,298,'quick_sort([])',20,mono=True)
    d.text(330,298,'quick_sort([2])',20,mono=True)
    d.text(80,334,'возвращает []',20,color=GREEN)
    d.text(330,334,'возвращает [2]',20,color=GREEN)
    d.text(60,375,'Длина 0 или 1: список уже отсортирован.',21)
    d.box(60,402,500,55,'#dbf0e8')
    d.text(80,437,'[] + [1] + [2] = [1, 2]',23,mono=True)
    d.box(620,125,540,355)
    d.text(640,160,'2. quick_sort([5, 5, 4]), опорный 5',23,color=BLUE,bold=True)
    d.text(640,202,'Разбиение: [4]    [5, 5]    []',23,mono=True)
    d.arrow(740,220,740,265)
    d.arrow(1030,220,1030,265)
    d.text(650,298,'quick_sort([4])',20,mono=True)
    d.text(930,298,'quick_sort([])',20,mono=True)
    d.text(650,334,'возвращает [4]',20,color=GREEN)
    d.text(930,334,'возвращает []',20,color=GREEN)
    d.text(640,375,'Равные опорному [5, 5] уже готовы.',21)
    d.box(640,402,500,55,'#dbf0e8')
    d.text(660,437,'[4] + [5, 5] + [] = [4, 5, 5]',22,mono=True)
    d.text(40,531,'3. Возвращаемся в quick_sort([5, 2, 5, 1, 4, 3]), опорный 3',24,color=BLUE,bold=True)
    for x,w,label,value in [(40,310,'Вернулась левая часть','[1, 2]'),(445,220,'Равные опорному','[3]'),(760,400,'Вернулась правая часть','[4, 5, 5]')]:
        d.text(x,578,label,21)
        d.box(x,600,w,55,'#dbf0e8')
        d.text(x+w/2,636,value,25,mono=True,anchor='middle')
    d.text(394,638,'+',30,anchor='middle'); d.text(710,638,'+',30,anchor='middle')
    d.arrow(600,665,600,707)
    d.text(600,749,'[1, 2, 3, 4, 5, 5]',28,color=GREEN,bold=True,mono=True,anchor='middle')
    d.save('quicksort-return.svg')


def quicksort_level_work():
    d=Diagram('Quicksort: считаем работу всего уровня', 'Пример: n = 7, опорные 4, затем 2 и 6. Числа справа — элементы в проходах разбиения.',740)
    d.text(40,163,'Глубина 0',22,color=BLUE,bold=True)
    d.row(260,130,[1,2,3,4,5,6,7],active=(3,),width=60)
    d.text(900,161,'7 элементов',23,color=BLUE,bold=True)
    d.arrow(480,190,360,252); d.arrow(580,190,700,252)
    d.text(40,307,'Глубина 1',22,color=BLUE,bold=True)
    d.row(260,275,[1,2,3],active=(1,),width=60)
    d.row(600,275,[5,6,7],active=(1,),width=60)
    d.text(900,306,'3 + 3 = 6',23,color=BLUE,bold=True)
    d.text(430,365,'4 уже выделена: в дочерние части не входит.',20,color=GREEN)
    for source,target in [(290,280),(430,450),(630,620),(770,790)]:
        d.arrow(source,385,target,430)
    d.text(40,477,'Глубина 2',22,color=BLUE,bold=True)
    for x,v in [(250,1),(420,3),(590,5),(760,7)]: d.row(x,445,[v],fixed=(0,),width=60)
    d.text(900,467,'0 проходов',23,color=GREEN,bold=True)
    d.text(900,499,'Длина каждой части — 1.',19,color=GREEN)
    d.box(40,555,1120,142,'#dbf0e8')
    d.text(60,592,'На одной глубине части не пересекаются: сумма их длин ≤ n.',24,color=GREEN,bold=True)
    d.text(60,632,'Поэтому проходы всех вызовов этого уровня вместе требуют O(n) работы.',23)
    d.text(60,671,'Склеивание готовых частей тоже линейно по их суммарной длине.',21)
    d.save('quicksort-level-work.svg')


def tree():
    d=Diagram('Три различных значения: шесть возможных порядков', 'Лист a b c означает a < b < c: это порядок исходных элементов после сортировки.',670)
    def node(x,y,label,w=135,leaf=False):
        d.box(x-w/2,y,w,44,'#dbf0e8' if leaf else '#ffffff')
        d.text(x,y+29,label,21,anchor='middle',mono=True)
    node(600,125,'a < b?')
    for x,label in [(300,'да'),(900,'нет')]:
        d.arrow(600,170,x,235,label); node(x,235,'b < c?' if x==300 else 'a < c?')
    for x,parent,label,s in [(140,300,'да','a b c'),(440,300,'нет','a < c?'),(760,900,'да','b a c'),(1060,900,'нет','b < c?')]:
        d.arrow(parent,280,x,355,label); node(x,355,s,leaf=x in (140,760))
    for x,parent,label,s in [(345,440,'да','a c b'),(530,440,'нет','c a b'),(960,1060,'да','b c a'),(1130,1060,'нет','c b a')]:
        d.arrow(parent,400,x,490,label); node(x,490,s,125,leaf=True)
    d.text(40,594,'Не более h сравнений → не более 2ʰ листьев. Нужно различить n! порядков.',22)
    d.text(40,634,'2ʰ ≥ n!  ⇒  h ≥ log₂(n!)  ⇒  Ω(n log n) в худшем случае.',24,color=BLUE,bold=True)
    d.save('comparison-tree.svg')


def counting():
    d=Diagram('Сортировка подсчётом: сначала частоты', 'Значения — целые числа от 0 до 3. Индекс счётчика обозначает само значение.',625)
    d.text(40,157,'Вход',22,color=BLUE,bold=True); d.row(245,125,[3,1,3,0,2,1])
    d.arrow(465,180,465,230,'Посчитать каждое значение')
    d.text(40,280,'Значение / индекс',21,color=BLUE)
    d.text(40,345,'Сколько раз встретилось',19,color=GREEN)
    for i,count in enumerate([1,2,1,2]):
        x=335+i*155
        d.text(x+32,280,str(i),26,anchor='middle',color=BLUE,mono=True)
        d.box(x,305,64,55,'#dbf0e8'); d.text(x+32,341,str(count),26,anchor='middle',mono=True)
        d.text(x+32,395,f'{count} шт.',19,anchor='middle')
    d.arrow(570,414,570,465,'Выписать значения по частотам')
    d.text(40,521,'Результат',22,color=BLUE,bold=True); d.row(245,490,[0,1,1,2,3,3],fixed=range(6))
    d.text(40,590,'Два прохода по данным и проход по диапазону: O(n + k), здесь n = 6, k = 4.',22)
    d.save('counting-sort.svg')
    d=Diagram('Цена подсчёта зависит от диапазона', 'k = максимум − минимум + 1, если под каждое значение выделяется отдельный счётчик.',500)
    d.card(40,140,540,['Баллы от 0 до 100','n = 1 000 000 записей','k = 101 счётчик','Диапазон мал по сравнению с n.'],GREEN)
    d.card(620,140,540,['[0, 1 000 000 000]','n = 2 значения','k = 1 000 000 001 счётчик','Почти все счётчики будут нулевыми.'],ORANGE)
    d.text(40,390,'Время O(n + k), дополнительная память O(k) для счётчиков.',24,color=BLUE,bold=True)
    d.text(40,439,'Мало элементов ещё не означает мало работы. Сначала оцените размер диапазона.',21)
    d.save('counting-range.svg')


def python_sorting():
    d=Diagram('sorted() и .sort(): что происходит со списком', 'Два независимых продолжения: source = [5, 1, 4]; alias = source.',585)
    for x,title in [(40,'ordered = sorted(source)'),(640,'result = source.sort()')]:
        d.text(x,150,title,25,color=BLUE,mono=True)
    d.text(40,227,'source, alias',22,mono=True); d.arrow(215,220,260,220); d.row(270,195,[5,1,4])
    d.text(40,327,'ordered',22,mono=True); d.arrow(170,320,260,320); d.row(270,295,[1,4,5],fixed=range(3))
    d.text(640,227,'source, alias',22,mono=True); d.arrow(815,220,860,220); d.row(870,195,[1,4,5],fixed=range(3))
    d.text(640,327,'result → None',24,mono=True)
    d.card(40,405,520,['Новый внешний список','Исходный список не меняется.','Элементы глубоко не копируются.'])
    d.card(640,405,520,['Тот же объект списка','Изменение видно через alias.','Метод возвращает None.'])
    d.save('sorted-vs-sort.svg')
    d=Diagram('key: сравниваем ключи, возвращаем записи', 'sorted(participants, key=score_key) — по баллам по возрастанию.',655)
    for x,title in [(40,'Исходные записи'),(490,'Ключи'),(790,'Результат')]: d.text(x,145,title,23,color=BLUE,bold=True)
    original=[('Вера',80),('Аня',95),('Борис',80),('Глеб',90)]
    for j,(name,score) in enumerate(original):
        y=175+j*85
        d.box(40,y,310,55); d.text(58,y+35,f'{name} · {score}')
        d.arrow(365,y+28,480,y+28)
        d.box(490,y,90,55,'#fff0d8'); d.text(535,y+35,score,24,anchor='middle',mono=True)
    for j,(name,score) in enumerate(sorted(original,key=lambda r:r[1])):
        y=175+j*85; d.box(790,y,350,55,'#dbf0e8'); d.text(810,y+35,f'{name} · {score}')
    d.arrow(605,290,765,290)
    d.text(685,270,'Сортировка',18,color=BLUE,anchor='middle')
    d.text(40,578,'Функция key вызывается один раз для каждого входного элемента.',23,color=GREEN,bold=True)
    d.text(40,618,'При равных ключах Вера остаётся раньше Бориса, как в исходном списке.',21)
    d.save('key-pipeline.svg')
    d=Diagram('Составной ключ: сначала баллы, затем имя', 'key=lambda row: (-row["score"], row["name"]) — обычное сравнение кортежей.',665)
    for j,(name,score,key) in enumerate([('Аня',95,'(-95, "Аня")'),('Глеб',90,'(-90, "Глеб")'),('Борис',80,'(-80, "Борис")'),('Вера',80,'(-80, "Вера")')]):
        y=145+j*78; d.text(50,y+31,f'{j+1}.  {name} · {score}',24); d.box(390,y,350,48,'#dbf0e8'); d.text(410,y+31,key,24,mono=True)
    d.text(50,462,'Только баллы: Вера → Борис. Добавили имя: Борис → Вера.',21,color=GREEN)
    d.card(40,495,540,['Борис и Вера','−80 = −80 → сравниваем имена.','«Борис» раньше «Вера».'])
    d.card(620,495,540,['Аня и Борис','−95 < −80 → решение уже принято.','До сравнения имён дело не доходит.'])
    d.save('tuple-key.svg')
    d=Diagram('Стабильность: равные ключи сохраняют порядок', 'Сортируем по баллам. Буквы A, B, C, D — идентификаторы записей, а не часть ключа.',600)
    rows=[('Исходный порядок',[('A',80),('B',95),('C',80),('D',95)]),('По возрастанию',[('A',80),('C',80),('B',95),('D',95)]),('reverse=True',[('B',95),('D',95),('A',80),('C',80)])]
    for j,(label,items) in enumerate(rows):
        y=150+j*110; d.text(40,y+36,label,22,color=BLUE,mono=j==2)
        for i,(name,score) in enumerate(items):
            x=330+i*205; d.box(x,y,175,60,'#dbf0e8' if score==80 else '#dce8fa'); d.text(x+88,y+39,f'{name} · {score}',24,anchor='middle')
    d.text(40,520,'В обоих результатах A раньше C, а B раньше D.',24,color=GREEN,bold=True)
    d.text(40,560,'reverse=True меняет направление сортировки, сохраняя порядок равных ключей.',21)
    d.save('stable-sort.svg')


def merge():
    d=Diagram('Слияние: два отсортированных потока', 'Каждый раз забираем меньшую из двух голов. Готовый префикс больше не меняется.',550)
    d.text(40,152,'Первый список',22,color=BLUE); d.row(280,120,[1,4,7],active=(0,))
    d.text(40,232,'Второй список',22,color=BLUE); d.row(280,200,[2,4,8],active=(0,))
    d.text(640,155,'1 < 2 → берём 1',24,color=GREEN)
    d.text(640,205,'Затем 2 < 4 → берём 2',24,color=GREEN)
    d.text(640,255,'Затем 4 = 4 → берём слева',24,color=GREEN)
    d.arrow(500,285,500,345)
    d.text(40,404,'Результат',22,color=BLUE); d.row(280,370,[1,2,4,4,7,8],fixed=range(6))
    d.text(40,499,'Каждый элемент переносится один раз: O(n + m) времени для длин n и m.',23)
    d.save('merge-streams.svg')


if __name__ == '__main__':
    purpose(); bubble(); quicksort(); quicksort_return(); quicksort_level_work(); tree(); counting(); python_sorting(); merge()
    print('Generated 15 SVG diagrams.')
