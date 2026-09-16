# «Питон наводит порядок»: промпт

Создано встроенным инструментом генерации изображений `image_gen`.

Заменяет прежний комикс к лекции 2. Стиль и персонажи сохранены по изображению `lecture02-comic.png`; содержание всех восьми кадров переработано под строки, списки, кортежи, множества и словари.

Use case: illustration-story.
Asset type: replacement educational comic page for lecture 02 in a Russian university Python course.
Input image: EDIT TARGET and visual style reference. Preserve the drawing style, warm paper, expressive ink, muted blue/ochre palette, dark-haired university student in blue hoodie, and friendly green python with round glasses. The snake has NO arms or legs and gestures with its tail. Rebuild the educational content of ALL EIGHT PANELS from the script below. The previous page's obsolete subject matter must disappear completely.

Title, exact Russian: «ПИТОН НАВОДИТ ПОРЯДОК».
Subtitle, exact Russian: «Лекция 2. Строки и коллекции».
Format: portrait comic, exactly two columns and four rows, reading left to right, top to bottom. Every panel fully visible, generous margins, large clear Cyrillic lettering, readable code labels. Use a high-resolution image. A lively comic with real action and dry humor, not a slide or sterile infographic. Same ordinary storeroom/workbench setting as the reference, but no files or mail-processing narrative. Only the student and python are needed. All speech tails unambiguously point to the correct speaker. Do not add decorative slogans or extra text.

PANEL 1 — STRINGS:
On a workbench a machine makes a new clean paper label from an existing label. The ORIGINAL label remains intact and reads exactly "  КОТ  ". The new label reads exactly "кот". Emphasize a new label, not modifying the original.
Student bubble: «А исходная строка?»
Python bubble: «Осталась как была.»
Single code label:
raw.strip().lower()
Small clear panel heading: str

PANEL 2 — LIST SLICES:
Three boxes on a shelf are labelled 10, 20, 30, respectively. Directly below them are index labels 0, 1, 2, respectively. A red selection bracket includes ONLY boxes 10 and 20. Box 30 remains outside.
Python bubble: «Правая граница не входит.»
Code label:
[10, 20, 30][:2] → [10, 20]
Panel heading: list

PANEL 3 — LIST SORTING:
Student has arranged three small numbered cards in ascending order 1, 2, 3. He looks at an EMPTY return tray marked None. Python points at the sorted cards. The list did change; None is the method's return value, not the list itself.
Student bubble: «А где результат?»
Python bubble: «Список уже изменён.»
One readable code block, exactly four lines:
a = [3, 1, 2]
result = a.sort()
a → [1, 2, 3]
result → None

PANEL 4 — ONE-ELEMENT TUPLE:
Two little display pedestals: the left holds a lone number card labelled (42); the right holds a single compartment with a number card and an emphatically visible comma, labelled (42,). Python points at the comma.
Student bubble: «Скобок недостаточно?»
Python bubble: «Кортеж создаёт запятая.»
Two accurate code labels:
(42) → int
(42,) → tuple
Panel heading: tuple

PANEL 5 — SETS:
On the input side lie three number tokens 2, 1, 2. On the output side, a loose circular area contains ONLY TWO tokens, 1 and 2, positioned freely, with no queue, no indices, no implied ordering. The equal repeated token is not preserved.
Python bubble: «Повторы убрали. Порядок не обещали.»
Code label, use the equality operator exactly:
set([2, 1, 2]) == {1, 2}
Panel heading: set

PANEL 6 — SET INTERSECTION:
Two overlapping hoops on the workbench: left hoop labelled a contains a token 1 in its left-only area; token 2 is in the shared overlap; right hoop labelled b contains token 3 in its right-only area. Exactly three tokens total, no duplicates.
Python bubble: «Пересечение — общие элементы.»
Code block:
a = {1, 2}
b = {2, 3}
a & b == {2}

PANEL 7 — DICTIONARY UPDATE:
A small cabinet has ONE drawer with key label чай. Its value card, formerly 2, has been replaced by 5. Student holds the removed old card 2; python points at the new card 5 in the SAME drawer. Do not create a second entry with the same key.
Student bubble: «А прежнее значение?»
Python bubble: «Заменили. Ключ остался.»
Code block:
stock = {"чай": 2}
stock["чай"] = 5
stock → {"чай": 5}
Panel heading: dict

PANEL 8 — DICTIONARY MEMBERSHIP:
The student and python stand at the same single drawer labelled чай with value card 5. Python points at the key label on the FRONT, emphasizing that ordinary membership tests keys.
Python bubble: «in проверяет ключи.»
Student bubble: «Теперь понятно, где искать.»
Code block:
"чай" in stock → True
5 in stock → False
5 in stock.values() → True
No additional footer dialogue.

Accuracy constraints:
Every code label, quote, comma, bracket, arrow, comparison operator, and Russian line must be exact and legible. Code identifiers are Latin. Use straight double quotes in code. Keep meanings unambiguous, especially a.sort() versus its return value, the trailing comma in (42,), set unorderedness, intersection placement, dictionary key replacement, and keys versus values membership.
Remove ALL text, labels, objects, and dialogue about match/case, guards, with, files, file paths, encoding, CSV, JSON, and tracebacks. Do not reuse any obsolete panels. No watermark, no signature, no extra panels, no cropped bubbles or edges.

## Финальное уточнение

Use case: precise-object-edit.
Edit the supplied finished comic page. Change ONLY the small new output paper label coming out of the string-cleaning machine in the TOP-LEFT panel.
It must read exactly: "кот"
Include the two straight double quotation marks and the three LOWERCASE Cyrillic letters к, о, т. Use an ordinary clean typeset monospace font with recognizably lowercase x-height, NOT uppercase comic lettering. The original separate wooden input label in that same panel must remain "  КОТ  ", with uppercase letters and spaces, so the contrast is unambiguous: original uppercase КОТ stays, new result is lowercase кот.
Preserve everything else pixel-for-pixel as much as possible: every other label, all code, speech, title, eight-panel layout, colors, characters, drawings, and exact text. Do not redraw or change any of the other seven panels. Do not modify the slice, tuple comma, None, set intersection, or dictionary code.
This is a single localized typography correction for educational accuracy.
