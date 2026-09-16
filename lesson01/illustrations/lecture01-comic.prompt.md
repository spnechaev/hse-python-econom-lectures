# «Питон берётся за дело»: промпт

Создано встроенным инструментом генерации изображений.

Референс стиля и персонажей: `../../lesson02/illustrations/lecture02-comic.png`.

Use case: illustration-story.
Make a companion comic page for LECTURE 1 by redrawing the supplied comic reference with a NEW story. The input image is a style, composition and character reference, NOT source content to repeat.
Preserve the recognizable dark-haired university student in a blue hoodie and the green python with small round glasses, the expressive polished ink artwork, warm paper, turquoise/ochre colors, occasional red error marks, clean panel borders and visual humor. The snake is a snake without human arms or legs, gesturing with its tail. This is an adult university teaching comic, not a children's poster.
Output ONE finished tall portrait page, exactly TWO columns by FOUR rows, EIGHT panels, all visible, high resolution ideally 2048x3072. The title and all speech bubbles must remain fully inside the image. Large legible Russian lettering and exact monospace code; avoid tiny explanatory text.
Title exact: «ПИТОН БЕРЁТСЯ ЗА ДЕЛО»
Small subtitle: «Лекция 1. Первые программы»

New setting: an ordinary programming workshop adjoining a computer game registration desk and a book-reading corner. Make it a sequence of actual comic scenes with character reactions, not a collection of abstract diagrams. Only use the visible text specified below. Do NOT invent motivational posters, slogans, extra captions, logos or filler text. In particular do not copy text or the data mailroom of lecture 2 from the reference.

Panel 1, top left — values and types:
The student has two workbench trays: one with number blocks 10 and 20 combining into 30; another with two paper text labels "10" and "20" joining into "1020". Quotes around strings must be clearly visible.
Student bubble: «Один плюс — два результата?»
Python bubble: «Сначала посмотри на типы.»
Two exact code labels:
10 + 20 → 30
"10" + "20" → "1020"

Panel 2, top right — readable code, Zen and PEP 8:
The student holds a messy crumpled draft represented only by a tangled ink scribble; the snake points to a neatly written board. A small book on the desk is labelled import this; the board heading is PEP 8.
Student: «Работает же!»
Python: «А читать это кому?»
The tidy board contains exactly TWO lines of code, second line visibly indented:
if length < 3:
    status = "too short"
No bogus pseudo-code on the crumpled paper and no additional slogans.

Panel 3, second row left — a condition:
The student is at a game registration gate with a clear sign «От 3 до 12 символов». A badge reading «кот» is accepted with a green light. A separate badge «я» has a red light.
Student: «„Кот“ проходит?»
Python: «Три символа. Проходит.»
Exact code label: 3 <= len(name) <= 12
Use the actual Cyrillic lowercase name кот on the badge.

Panel 4, second row right — reusable function:
A little reliable tabletop checking machine is labelled nickname_status. Student inserts a card "кот", and a clearly visible output tray receives a card "ok". There are spare input cards "я" and "игрок" waiting on the desk, not already processed.
Student: «Один раз написал — вызываю снова?»
Python: «С другими данными.»
Exact code label: nickname_status("кот") → "ok"

Panel 5, third row left — print vs return:
A humorous demonstration with two distinct small gadgets on the same desk: a loudspeaker labelled print audibly displays the number 3 in an output balloon; its result tray visibly contains a card None. A separate delivery chute labelled return hands back a solid result card 3 to the waiting program, represented by the student's laptop. This contrast must be visually unambiguous: print shows a value to a person and its call returns None; return sends a function result to the caller.
Student: «Напечатал. А результат где?»
Python: «Для программы нужен return.»
Only gadget text: print, return, 3, None. Do not include an ambiguous code example suggesting return can appear outside a function.

Panel 6, third row right — for:
The student adds three reading portions, visibly labelled 10, 20 and 30, into a completed-pages tray labelled «60 страниц». Python watches a three-position mechanical counter.
Python: «for перебирает элементы.»
A readable code card contains exactly:
pages_read = 0
for pages in [10, 20, 30]:
    pages_read += pages
Preserve the indentation and the += operator. Three portions, not four.

Panel 7, bottom row left — while:
A book marked «65 страниц» and four calendar-day cards laid in order. The cards are labelled «День 1», «День 2», «День 3», «День 4». Under them the reading amounts are exactly 20, 20, 20, 5 respectively. This depicts reading up to 20 pages per day until finished.
Student: «На три дня хватит?»
Python: «На четвёртый останется пять.»
Code label: while pages_left > 0:
Do not show negative remaining pages or imply that a for loop must always be used with a known number of iterations.

Panel 8, bottom row right — boundaries:
At the game-name tester, student celebrates one successful example while python calmly points to a four-column boundary-check board.
Student: «На одном имени всё работало!»
Python: «Поэтому проверим границы.»
Board heading: «Длина имени»
Exactly four columns in order:
2 — too short
3 — ok
12 — ok
13 — too long
Arrange as four compact cards or a simple table with clear correspondence. Mark both ok cases green and too short/too long red. Red here means rejected name, NOT a failed test.
One code label at bottom: assert nickname_status("кот") == "ok"
No claim that the length-2 string is accepted. The rule is inclusive 3 through 12; functions use default bounds.

Accuracy and design constraints: depict all eight scenes in the exact reading order, no duplicate panels. Preserve characters and drawing style from reference but use the completely new lecture-1 content above. Every Russian and code label must be carefully spelled. No tracebacks, CSV or JSON from the reference page. No watermark or signature. Prioritize readable lettering and causally clear scenes over background detail.
