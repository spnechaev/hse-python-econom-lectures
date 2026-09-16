# «Дзен Питона»: промпты

Создано встроенным инструментом генерации изображений.

Референс персонажей и стиля: `lecture01-comic.png`.

## Страница 1

Use case: illustration-story.
Create a NEW educational comic using the supplied image solely as a CHARACTER AND DRAWING-STYLE REFERENCE. Redraw every scene and replace all lecture-1 content. Keep the recognizable dark-haired university student wearing a blue hoodie and the friendly green python with small round glasses. The python is a snake, gesturing with its tail, never given human arms or legs. Keep warm paper, polished expressive ink artwork, muted turquoise/ochre colors and subtle dry humor, but use uncluttered workshop backgrounds instead of copying reference posters or props.
Portrait page, exactly SIX large panels in TWO COLUMNS and THREE ROWS. Reading order left-to-right, top-to-bottom. High resolution ideally 2048x3072. Clear consistent character faces, expressive action, carefully drawn hands, ample white speech balloons. All SIX panels fully visible. Large readable Russian text. This is a comic for university students, not a slide deck or mystical spiritual poster. NO meditation, lotus poses, magic or religious imagery.
Every panel has a short caption strip for the principle and a comic action explaining it. Only draw the exact specified visible words, code labels and dialogue. No extra slogans, fake code, watermarks, signatures or motivational wall posters. Don't repeat any old captions from the reference.
Source of ideas: Tim Peters, PEP 20, The Zen of Python. These are judgment-guiding principles, not rigid rules. The apparent qualifications and tensions are deliberate and must remain clear.

PAGE ONE OF TWO.
Main title: «ДЗЕН ПИТОНА»
Subtitle: «1. Как сделать код понятным»
Small header note: «Идеи Тима Петерса • PEP 20 • import this»

PANEL 1 — beauty, sparseness and readability:
Caption: «Красиво. Просторно. Читаемо.»
Student finds his own old handwritten tangled draft and looks genuinely bewildered. Python holds a clean, comfortably spaced code card. The contrast is organization and readable names, NOT decorative prettiness.
Student: «Кто это написал?!»
Python: «Ты. Во вторник.»
The clean code card, EXACT: pages_left = total_pages - pages_read
The old draft is abstract tangled pen strokes, NOT tiny illegible fake letters.
This panel combines Beautiful is better than ugly, Sparse is better than dense, Readability counts.

PANEL 2 — explicitness:
Caption: «Явное лучше неявного.»
Two distinguishable data boxes sit on a desk: one contains a solid number 0; the other is empty with a tag None. Student mistakenly reaches to throw both away; python stops him by pointing at the solid zero.
Student: «Ноль — значит данных нет?»
Python: «Ноль есть. Нет данных — None.»
Code label, EXACT: if pages_read is None:
Do not visually imply 0 and None are equal.

PANEL 3 — simple versus complex versus convoluted:
Caption: «Проще — хорошо. Запутаннее — плохо.»
Student tries to cut a CSV strip at every comma with ordinary scissors. The strip reads exactly: 1,"чай, кофе"
Python presents a tidy purpose-built parsing tool labelled csv.reader. It produces exactly TWO compartments, 1 and чай, кофе. The quotation marks protect the internal comma.
Student: «Резать по запятым проще!»
Python: «Но кавычки тоже часть задачи.»
Necessary complexity must be handled, not wished away; a clear library interface can handle complex rules. This illustrates both Simple is better than complex and Complex is better than complicated. No claim that simplistic incorrect code is better.

PANEL 4 — flattening unnecessary nesting:
Caption: «Плоское лучше вложенного.»
Student is stuck inside three concentric office cubicles, each entrance labelled if. Python stands at an open reception desk, with a clear early exit marked return for unsuitable cases. This is a visual metaphor, not executable code.
Student: «Я всё ещё внутри if?»
Python: «Отсеки неподходящее на входе.»
Only other text: if (three times), return (once).
Do not suggest every nested condition is forbidden.

PANEL 5 — consistency and practical exceptions:
Caption: «Общие правила. Практичные исключения.»
Student brings an external-system package labelled userName to a workshop where neat storage is labelled user_name. Python points to a small adapter at the entrance that translates the name and lets the internal system stay consistent.
Student: «У них поля названы иначе!»
Python: «Переведём на границе. Внутри — один порядок.»
Adapter sign, EXACT: userName → user_name
This illustrates the pair Special cases aren't special enough to break the rules / Although practicality beats purity. Don't show refusal to cooperate with external systems.

PANEL 6 — errors, including deliberate suppression:
Caption: «Ошибки не должны исчезать незаметно.»
Student sweeps a red error warning under a carpet and proudly presents a fake numeric answer 0. Python lifts the carpet with its tail so the error is visible again. The red card reads ValueError, associated with a small label int("кот"). This is clearly the WRONG way to get a numerical answer.
Student: «Спрятал ошибку. Теперь всё работает!»
Python: «А правильные данные появились?»
A small legible footnote inside this panel: «Подавлять ошибку можно только осознанно.»
This illustrates both Errors should never pass silently and Unless explicitly silenced. Intentionally permitted suppression is a deliberate design choice, not a blanket catch-all exception policy.


## Страница 2

Use case: illustration-story.
Create a NEW educational comic using the supplied image solely as a CHARACTER AND DRAWING-STYLE REFERENCE. Redraw every scene and replace all lecture-1 content. Keep the recognizable dark-haired university student wearing a blue hoodie and the friendly green python with small round glasses. The python is a snake, gesturing with its tail, never given human arms or legs. Keep warm paper, polished expressive ink artwork, muted turquoise/ochre colors and subtle dry humor, but use uncluttered workshop backgrounds instead of copying reference posters or props.
Portrait page, exactly SIX large panels in TWO COLUMNS and THREE ROWS. Reading order left-to-right, top-to-bottom. High resolution ideally 2048x3072. Clear consistent character faces, expressive action, carefully drawn hands, ample white speech balloons. All SIX panels fully visible. Large readable Russian text. This is a comic for university students, not a slide deck or mystical spiritual poster. NO meditation, lotus poses, magic or religious imagery.
Every panel has a short caption strip for the principle and a comic action explaining it. Only draw the exact specified visible words, code labels and dialogue. No extra slogans, fake code, watermarks, signatures or motivational wall posters. Don't repeat any old captions from the reference.
Source of ideas: Tim Peters, PEP 20, The Zen of Python. These are judgment-guiding principles, not rigid rules. The apparent qualifications and tensions are deliberate and must remain clear.

PAGE TWO OF TWO.
Main title: «ДЗЕН ПИТОНА»
Subtitle: «2. Как выбирать решения»
Small header note: «Идеи Тима Петерса • PEP 20 • import this»

PANEL 1 — ambiguity:
Caption: «При неоднозначности не угадывай.»
Student examines a user's date card reading 03/04. Two equally plausible calendar cards show «3 апреля» and «4 марта». Python points toward the user to request a clear format, not a fortune-telling device.
Student: «Третье апреля?»
Python: «Или четвёртое марта. Уточни формат.»
Only these labels and dialogue; don't accidentally mark one interpretation as inherently correct.

PANEL 2 — one obvious way, and the beginner's perspective:
Caption: «Предпочитай очевидный способ.»
A tidy standard tool labelled sum(numbers) sits beside a student's needlessly tangled adding mechanism. The student is learning to recognize the standard tool, not being punished for alternatives.
Student: «А если мне пока не очевидно?»
Python: «Ты учишься. Очевидность приходит с опытом.»
This interprets There should be one—and preferably only one—obvious way to do it and its humorous qualification Although that way may not be obvious at first unless you're Dutch. Do not add a national stereotype or claim Python permits only one syntactically valid solution.

PANEL 3 — now versus reckless haste:
Caption: «Не откладывай. Но и не торопись вслепую.»
Student has begun constructing a small working program on the bench but reaches for a large release button. Python points to a short pending test checklist before releasing it. A clear visual separation between starting work and submitting an unchecked result.
Student: «Значит, срочно отправляем?»
Python: «Сейчас — начать. Отправить — после проверки.»
Only other labels: «Отправить», «Проверки».
This illustrates Now is better than never and Although never is often better than right now; no implication that endless procrastination is good.

PANEL 4 — explainability is evidence, not proof:
Caption: «Объяснить просто — хороший признак.»
Student has replaced a tangled planning sheet with a simple, understandable flow on the board. Python holds test cases still to be run.
Student: «Теперь могу объяснить!»
Python: «Хорошо. Осталось проверить.»
The flow board, EXACT: «Ввод → проверка → результат»
This illustrates both If the implementation is hard to explain, it's a bad idea and If the implementation is easy to explain, it MAY be a good idea. Make clear that a simple explanation does not guarantee correctness. Do not draw a passed-test stamp yet.

PANEL 5 — namespaces:
Caption: «Пространства имён наводят порядок.»
Two clearly separate project-module cabinets, one labelled game.py and the other report.py. Each cabinet contains its own distinct tool labelled save. They can coexist because their full names are different. These are TWO FICTIONAL MODULES OF THE SAME PROJECT, not claims about Python standard-library modules.
Student: «Две функции save. Кто из них кто?»
Python: «game.save и report.save.»
Other labels exactly: game.py, report.py, save (on each of the two tools).
This illustrates Namespaces are one honking great idea—let's do more of those. No merging the cabinets into one global name.

PANEL 6 — synthesis:
Caption: «Дзен помогает задавать правильные вопросы.»
Student closes a book labelled import this and looks at an actual modest program on his laptop, ready to work rather than worship the book. Python calmly points to a small practical checklist.
Student: «Теперь знаю, как писать любой код?»
Python: «Теперь знаешь, о чём себя спрашивать.»
The checklist, exactly three lines:
Понятно?
Явно?
Работает?
This is the ending of the full two-page comic: judgment, clarity and checking work together. No new dogmas, no guarantee that following slogans automatically makes a program correct.


## Исправление подписей на первой странице

Edit the supplied Russian Zen of Python comic page. Preserve the entire page EXACTLY: six panels, every character, all artwork, colors, composition, titles, speech bubbles and text except the two small labels specified below. This is a surgical TEXT CORRECTION, not a redraw.

1. In the TOP LEFT panel, replace the erroneous three-line text on the cream card held by the green python with this syntactically valid Python expression ON ONE SINGLE LINE:
pages_left = 120 - 35
Make the cream card slightly wider if necessary to keep this one line large and legible, without covering any face or speech bubble. Do NOT wrap after the equals sign or minus sign. Do NOT change any dialogue.

2. In the BOTTOM LEFT panel, ensure the label on the outgoing small parcel is EXACTLY:
user_name
There must be a visible underscore between user and name, matching the target name already printed on the adapter above it. Preserve the incoming parcel label userName and the adapter sign userName → user_name.

Everything else is invariant. Return the complete corrected comic page, not a crop. No added explanatory notes or watermark.

