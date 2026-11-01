# «Алгоритмы и сложность»: обзорный постер к лекции 3

Источник содержания: текущий `lesson03/lecture.ipynb`.
Создано встроенным инструментом `image_gen`; основной материал отделён от дополнительных тем.
Визуальная преемственность: учебная доска, студент и питон из постера к лекции 1.

## Промпт

Use case: scientific-educational.
Asset type: Russian overview poster for lecture 3 of a university Python course.
Create a polished, highly legible illustrated educational poster, portrait 2:3, ideally 2048 × 3072. This is a finished poster for viewing and printing, not a photograph of a printed poster.

VISUAL STYLE AND COMPOSITION
Continue the visual language of an illustrated Python course: a warm university classroom, one enormous cream-colored teaching board in a thin wooden frame, dark navy headings, warm paper texture, fine dark ink outlines and restrained watercolor shading. The course's recurring dark-haired university student in a blue hoodie and friendly green python snake with round spectacles are small supporting figures in the two lower corners. The snake has no arms or legs. Reserve about 85 percent of the image for clearly readable teaching content. Keep room details and characters minimal. This is ONE cohesive classroom poster, not a narrative comic. Use clean aligned teaching zones on the same board, with calm pale blue, green and ochre accents and generous whitespace. Avoid cramped text. Main headings may use a confident condensed serif; body Russian text must be crisp, regular, readable. Code and formulas in monospace. The content is the focus.

At the top, large title exactly:
«АЛГОРИТМЫ И СЛОЖНОСТЬ»
Subtitle:
«Лекция 3 · Как растёт объём работы»
A short full-width introduction below:
«n — размер входа. Считаем действия и сравниваем рост затрат.»

Arrange SIX teaching zones in a spacious two-column, three-row layout on the single board. Use the exact Russian text below, with meaningful simple diagrams. These are compact, coherent sections, not separate narrative frames. Do not add text of your own.

TOP LEFT — 1. СЧИТАЕМ ДЕЙСТВИЯ
Heading: «1. Считаем действия»
Three rows with miniature square-cell diagrams:
«Один проход: n»
«Два прохода подряд: 2n»
«Полные вложенные циклы: n²»
For n=4 show respectively one row of 4 cells, two rows of 4 cells, a 4-by-4 square. Diagrams must have precisely those cell counts.
Bottom note:
«При n = 4: 4, 8 и 16 действий»
«Один цикл со срезами тоже может дать O(n²).»

TOP RIGHT — 2. СМОТРИМ НА РОСТ
Heading: «2. Смотрим на рост»
Caption: «Если n увеличить вдвое»
A neat two-column comparison table, exact:
«O(1)» | «почти без изменений»
«O(log n)» | «примерно +1 шаг»
«O(n)» | «примерно ×2»
«O(n log n)» | «немного больше ×2»
«O(n²)» | «примерно ×4»
Bottom:
«3n + 20 → O(n)»
«O описывает рост, а не секунды.»
Avoid drawing misleading measured timing plots. The table is the visual.

MIDDLE LEFT — 3. ВЫБИРАЕМ ПОИСК
Heading: «3. Выбираем поиск»
Two clearly distinguished approaches:
«Линейный: проверяем по очереди»
«O(n) в худшем случае»
Show a simple row of cells with a sequential scan arrow.
«Бинарный: отбрасываем половину»
«O(log n) в худшем случае»
Show successively halved horizontal bars and labels:
«16 → 8 → 4 → 2 → 1»
Caption for those bars: «Сужаем круг кандидатов»
Emphasized condition at bottom:
«Бинарному поиску нужен отсортированный список.»
Do not show unsorted values in a binary-search illustration. Do not claim the 16-to-1 reductions alone include the final comparison.

MIDDLE RIGHT — 4. ЦЕНА ОПЕРАЦИЙ PYTHON
Heading: «4. Цена операций Python»
A clean compact table. Exact rows, with code-like expressions in monospace:
«a[i], len(a)» | «O(1)»
«sum(a)» | «O(n)»
«a[l:r]» | «O(k), k — длина среза»
«sorted(a)» | «O(n log n), худший случай»
«x in list» | «O(n), худший случай»
«x in set / dict» | «O(1), в среднем»
Below table, readable notes:
«Для set и dict худший случай — O(n).»
«У словаря in проверяет ключи.»
Tiny but readable context under heading or table:
«a — список обычных целых чисел»
The expressions x in list and x in set / dict are schematic container-type labels, not executable code samples; render list, set, dict as container names, with no syntax highlighting suggesting runnable code.

BOTTOM LEFT — 5. УЧИТЫВАЕМ ПОДГОТОВКУ
Heading: «5. Учитываем подготовку»
Caption: «q запросов «есть ли значение?» к одним данным»
Two visual routes from the same stack of data:
«Искать в списке каждый раз»
«до O(nq)»
and
«Один раз построить set → q проверок»
«O(n + q) в среднем»
Bottom note:
«Строим множество перед циклом.»
«Сортировка перед поиском тоже стоит времени.»

BOTTOM RIGHT — 6. МЕНЯЕМ СПОСОБ РЕШЕНИЯ
Heading: «6. Меняем способ решения»
Caption: «Сравнить списки с учётом повторов»
A small visual contrast between tangled permutation arrows and two neatly ordered rows. Exact text:
«Перебор перестановок»
«4! = 24»
«14! = 87 178 291 200»
Label these numbers explicitly: «Число вариантов»
Below, a clear directional arrow to the improved approach:
«Сортировка обоих списков и сравнение»
«O(n log n) в худшем случае»
Bottom caution:
«Повторы важны: множество их теряет.»
Do not label the full running time of permutation comparison as O(n!) and do not suggest it is a measured number of seconds.

FULL-WIDTH BOTTOM STRIP, above the small corner characters
Main line in bold:
«Сначала корректность → затем оценка → затем замер»
Smaller but readable:
«time.perf_counter() · повторяем измерения · меняем n · учитываем подготовку»
Final narrow footer:
«Дополнительно: строгие O, Ω, Θ · память · lower_bound · bisect»

ACCURACY AND FINISH
Flawless Cyrillic spelling. Preserve all complexity notation, superscripts and arithmetic exactly. No arbitrary additional captions, decorative writing, fake university logos, slogans, speech bubbles, signatures or watermarks. No cropped text, overlaps or tiny illegible disclaimers. Be especially careful that set/dict O(1) is explicitly AVERAGE and linear/binary search are explicitly WORST CASE. Keep mathematical content accurate and the visual hierarchy clear. The result must read as an inviting, well-designed overview of algorithms and complexity, with the warm student-and-python classroom illustration quietly supporting the information.

## Уточнение: простой разбор нотации и исправление схемы поиска

Use case: scientific-educational, targeted poster edit.
Input image: the supplied Russian "АЛГОРИТМЫ И СЛОЖНОСТЬ" lecture-3 poster is the EDIT TARGET.
Preserve its warm illustrated university classroom style, navy typography, cream board, wooden frame, student in blue hoodie, green python with glasses, and the SIX existing teaching sections. Preserve all correct Russian wording, complexity values, factorial numbers, average/worst-case qualifiers and the footer. Produce a polished portrait poster, ideally 2048 × 3072 or larger readable equivalent.

MAIN CHANGE: Add a simple, memorable visual explanation of the notation O(F(n)).
Replace the narrow introductory strip below the subtitle with a spacious full-width teaching band titled:
«Как читать O(F(n))»
Move the six existing sections down and modestly adjust their size to make room. Reduce background and character area if needed; all content must remain easily readable. Keep the main title and subtitle.

In this new band place a VERY LARGE expression:
O(F(n))
with clean, short, noncrossing annotation lines to its exact components, like an anatomy diagram of the formula:
1. An arrow to the OUTER CAPITAL O, label «Верхняя оценка роста».
2. A bracket under the entire F(n), label «Функция для сравнения».
3. A separate small arrow to the inner lowercase n, label «Размер входа».
Make O, F and n visually distinct with restrained matching navy, green and ochre accents. Keep every letter and parenthesis correct: O(F(n)), uppercase letter O, not zero. Use generous spacing so pointers do not touch unrelated symbols.

Under the annotated expression, print this exact plain-language explanation on one or two lines:
«При больших n число действий не превышает C · F(n).»
«C — постоянный множитель.»

Then show one large illustrated simplification example:
«3n + 20 → O(n)»
Visually emphasize n in both parts in green, and make 3 and +20 muted gray. Under it print:
«Линейный рост: постоянные множители и слагаемые не меняют порядок.»
This is the key memorable image. No formal quantifiers, no big mathematical proof, no additional Greek letters in this new band. Do not claim O is an exact time, an equality with F(n), or inherently the worst case. Do not imply that O(n) means exactly n actions.

SECOND TARGETED CORRECTION:
In section 3 ("Выбираем поиск"), correct the visual row labelled 16 → 8 → 4 → 2 → 1. The current subdivided bars have the wrong number of cells. REMOVE ALL vertical subdivision lines from these five bars. Instead draw FIVE SOLID UNSEGMENTED green horizontal bars, with identical height and lengths in ratio 16:8:4:2:1; each bar is exactly half the preceding length. Keep the labels 16, 8, 4, 2, 1 and short arrow connectors, and keep «Сужаем круг кандидатов». The bars represent remaining quantities, not discrete cells. Do not accidentally change the correct 4-, 8-, and 16-cell diagrams in section 1.

Remove the now-duplicated 3n + 20 → O(n) example from section 2, since it appears prominently in the new notation band. Keep section 2's doubling table and «O описывает рост, а не секунды.». All other substantive educational text stays.

Keep typography sharp and flawless in Russian. Preserve readability across the full poster. No new decorative writing, no watermark. This is one revised overview poster with an integrated, simple notation diagram.

## Финальная проверка геометрии схем

Use case: precise-object-edit.
This is a surgical correction of ONLY TWO small diagrams in the supplied Russian lecture poster. Preserve absolutely all text, formula notation O(F(n)), all callouts, colors, characters, layout, and every other part. Do not reflow or redesign.

1. Essential correction in section 1 ("Считаем действия"): the green grid next to "Полные вложенные циклы: n²" currently has FOUR COLUMNS BUT ONLY THREE ROWS (12 cells), contradicting n=4 and the label 16 actions.
REPLACE JUST THIS GREEN GRID with exactly FOUR COLUMNS AND FOUR ROWS = 16 individual green cells.
In the supplied 1024×1536 image its area is approximately x=291..407, y=596..674. Keep those area bounds; reduce cell HEIGHT so all four rows fit without moving any text.
Draw four columns with x-ranges approximately [292,316], [322,346], [352,376], [382,406].
Draw FOUR rows with y-ranges approximately [596,612], [616,632], [636,652], [656,672].
This makes exactly 16 separate pale-green rectangular cells, a visible 4×4 grid. All four rows must be complete, all four columns must be complete. Count them before finishing. Preserve the "n = 4" to the right, the other two diagrams above, and all captions. It is fine for these 16 small cells to be wider than tall.

2. In section 3, the FIVE SOLID bars above labels 16, 8, 4, 2, 1 must shrink by a factor of TWO each step. Keep their height constant, their existing horizontal positions broadly similar, their labels and connecting arrows unchanged. Render them unsegmented with widths proportional to 16:8:4:2:1, for example 112, 56, 28, 14, and 7 pixels respectively at the input resolution. No internal cell divisions. The final bar should be very narrow. Keep all bars inside their panel and aligned on the same baseline.

No other changes. In particular keep the large, correctly annotated O(F(n)) diagram and its Russian wording EXACTLY unchanged. Preserve the poster's original resolution and visual crispness.
