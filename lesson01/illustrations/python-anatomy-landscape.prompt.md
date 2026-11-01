# «Анатомия Питона»: горизонтальный плакат

Создано встроенным инструментом `image_gen`. Новый горизонтальный плакат в стиле иллюстраций курса; существующий вертикальный постер сохраняется.

## Промпт

Use case: scientific-educational.
Create a NEW large HORIZONTAL illustrated educational wall poster titled exactly «АНАТОМИЯ ПИТОНА». It explains the anatomy of a Python PROGRAM, playfully presented with a friendly green python snake. This is a new wide composition, not a cropped or stretched portrait image.

FORMAT: LANDSCAPE 16:9, ideally native 3840 × 2160 pixels or the highest available resolution. A single continuous scene, no comic panels, no grid of separate scenes. Generous margins suitable for printing, very large clear text and accurate monospace code.

VISUAL CONCEPT: an elegant illustrated naturalist's field-guide plate meets a university programming workshop. Warm cream paper, precise dark ink outlines, restrained watercolor shading, muted teal/blue and ochre, small red and green accents for the control statements. A long lively green python with round spectacles curves through the outer margins of the wide poster, framing the content without covering any text. Its head is at the far right, its body extends around the lower edge; no human limbs. A small dark-haired university student wearing a blue hoodie sits at the lower left reading the program. These two characters match the educational comic series style: expressive, polished, warm, adult-friendly rather than childish. They are accents, not the main information. Do not depict real animal organs, dissection, skeletons or biological labels.

The CENTRAL main board is a large clean cream area containing the complete program. Large Russian callout headings surround it to the left and right with thin, precise, noncrossing leader lines. A balanced landscape infographic composition: the code is the readable central spine, educational annotations are the surrounding anatomy. No decorative background posters, no motivational slogans, no writing on cups, books or desks, no speech bubbles. Sparse setting. No logos, signatures or watermarks.

TEXT:
Main title, very large: АНАТОМИЯ ПИТОНА
Subtitle: Из чего состоит программа на Python

Render this ONE complete program EXACTLY as real monospace code, with clear four-space indentation and syntax highlighting:

# Читаем по дням
def read_pages(portion: int, goal=60) -> int:
    total = 0
    for day in range(1, 8):
        if day == 3:
            continue
        total += portion
        if total >= goal:
            break
    return total


daily_pages = 20
result = read_pages(daily_pages)
print(result)

Absolutely preserve all underscores, colons, parentheses, the double == operator, the >= comparison, += and ->. No fake code, ellipses or line numbers.
Indentation MUST be unambiguous: def and the final THREE lines daily_pages/result/print start at the SAME x-coordinate. total=0, for and return total are indented exactly four spaces; both if statements and total += portion exactly eight; continue and break exactly twelve. Two blank lines separate return from daily_pages. return is outside the loop but inside the function. Use discreet indentation guides only where they improve clarity.
There is ample landscape space: keep the entire definition on one line, without squeezing or omitting any character.

Include exactly the following TWELVE educational callouts. Large headings and short explanations, all in Russian, with leader lines to the precise code targets. No numbers are needed before the headings.

A. «Определение функции»
«def создаёт функцию»
Target: def read_pages in the definition.

B. «Параметры»
«portion — обязательный»
«goal=60 — по умолчанию»
«int — аннотация типа»
Targets: portion and goal=60 in the definition. Distinguish the default value from an argument at the call site.

C. «Отступы»
«Задают вложенность блоков»
Target: indentation of the function and loop body.

D. «Цикл for»
«Перебирает дни от 1 до 7»
Target: for day in range(1, 8).

E. «Условие if»
«Проверяет условие»
Target: if day == 3.

F. «continue»
«Пропускает остаток итерации»
Target: continue keyword.
Do not draw a control-flow arrow to the if line. A leader line from the annotation to the keyword is sufficient.

G. «break»
«Завершает ближайший цикл»
Target: break keyword. Do not imply that it terminates the whole function.

H. «return»
«Возвращает результат вызова»
Target: return total.

I. «Переменная и присваивание»
«daily_pages = 20»
Target: the assignment line daily_pages = 20.

J. «Вызов функции»
«Здесь выполняется её тело»
«goal не передан: берётся 60»
Target: read_pages(daily_pages), NOT the definition.

K. «Аргумент»
«Значение daily_pages: 20»
Target: daily_pages INSIDE the function call, NOT the parameter portion.

L. «print»
«Выводит значение на экран»
Target: print(result).

A small laptop or simple terminal area on the shared desk beneath the code shows exactly:
Вывод: 60
This is part of the same scene, not a separate comic panel.

ACCURACY:
This exact program reads 20 pages on day 1 and day 2, skips day 3 using continue, reaches 60 on day 4 and exits the loop with break. return then sends 60 to result, and print displays 60. The second argument is omitted, so goal uses 60. Defining the function alone does not run its body. Never conflate print, return, break and continue.
Keep educational text as the only writing in the image. All twelve labels, all code and the large title must be visible without overlap or cropping. The hierarchy must be immediately readable from a distance: title, code, labels. Make this a beautiful large landscape classroom poster, not a tiny dense cheat sheet.

