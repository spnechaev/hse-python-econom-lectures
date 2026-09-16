# «Программа на Python»: постер к лекции 1

Создано встроенным инструментом `image_gen`. Один кадр с подписанными конструкциями программы, в стиле комиксов курса.

## Код на постере

```python
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
```

## Промпт

Use case: scientific-educational.
Asset type: a single-frame illustrated Python teaching poster for lecture 1, in Russian.
Create ONE continuous illustrated scene, NOT a comic strip, NOT a multi-panel page, and NOT a grid of cards. The whole poster is one shot of a university programming workshop: a large upright cream-colored coding board at its center, an expressive dark-haired university student wearing a blue hoodie beside its bottom left, and a friendly green python snake with round spectacles at bottom right. The snake has no human arms or legs. Characters are small compared with the code and annotations, standing in the SAME room. Warm paper texture, elegant dark ink outlines, soft watercolor shading, muted turquoise/blue and ochre palette, restrained red and green for meaningful arrows, light ordinary workshop details in the background. It should look like the polished educational comic series starring this student and python, but this page is ONE SINGLE SCENE. Adult university audience. No unrelated objects, mascots, slogans, speech bubbles, watermark or signature.

Portrait poster, high resolution ideally 2048x3072, generously spaced. The central code board and its surrounding labeled callouts dominate almost the entire page. Prioritize large flawless Russian typography, exact monospace code, and clean noncrossing leader lines over ornament. Keep every element fully inside the image and allow printing. Annotations should look like pinned educational labels around ONE board, not bordered comic panels.

Title exactly: «ПРОГРАММА НА PYTHON».
Subtitle exactly: «Лекция 1. Что здесь что».

The board contains ONE complete Python program with EXACTLY the following text. Render it as real typeset monospace code with four-space indentation, no line numbers, no invented punctuation, no abbreviated ellipses. It must be large and easy to read, with coherent syntax highlighting. The nesting levels are essential: 0 spaces for def and the last three lines, 4 spaces for total=0, for, and return; 8 spaces for both if statements and total+=portion; 12 spaces for continue and break. There are two blank lines before daily_pages.

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

Surround this single program with the following TWELVE concise callouts, with precision leader lines to the exact target listed. Their arrangement can adapt to avoid crossings. All callout headings and explanations must be in Russian and spelled verbatim. Use clear readable black typography; headings can be heavier and colored. Do NOT put explanations inside the code or over any code character.

1. Heading «Определение функции». Explanation «def создаёт функцию». Point to def read_pages on the function-definition line.
2. Heading «Параметры». Explanation lines: «portion — обязательный», «goal=60 — по умолчанию», «int — аннотация типа». Point specifically to portion and goal=60 in the definition, not in the call.
3. Heading «Отступы». Explanation «Показывают вложенность блоков». Point to the indentation guides at the left of the function body. Show correct indentation clearly, especially return at the same indentation as for.
4. Heading «Цикл for». Explanation «Перебирает дни от 1 до 7». Point to the for line. Ensure range(1, 8) correctly implies day 1 through 7.
5. Heading «Условие if». Explanation «Проверяет условие». Point to if day == 3. Preserve the DOUBLE equality sign ==.
6. Heading «continue». Explanation «Следующая итерация цикла». Point to continue. Do not add a curved flow arrow: the annotation describes the transition.
7. Heading «break». Explanation «Выход из ближайшего цикла». Point to break. A restrained red flow arrow may additionally go from break DOWN TO return total, the statement immediately after the for loop; it must not suggest ending the whole program.
8. Heading «return». Explanation «Возвращает результат вызова». Point to return total.
9. Heading «Переменная и присваивание». Explanation «daily_pages = 20». Point to the daily_pages = 20 line. Underline or bracket the name and = sign without obscuring them.
10. Heading «Вызов функции». Explanation «Здесь выполняется её тело». Add «goal не передан: берётся 60». Point to read_pages(daily_pages) in the result-assignment line, NOT to the definition.
11. Heading «Аргумент». Explanation «Значение daily_pages: 20». Point to daily_pages INSIDE THE CALL read_pages(daily_pages), not the parameter portion.
12. Heading «print». Explanation «Выводит результат на экран». Point to print(result). A small real laptop on the shared workshop desk below the main board shows a terminal with the exact text: «Вывод: 60».

Important correctness:
The function definition itself does NOT execute its body; the function call does.
The parameter portion receives 20 from the argument daily_pages. The second parameter goal uses its default 60 because the call does not supply it. Days 1 and 2 bring total to 40, day 3 is skipped, day 4 brings total to 60 and breaks the loop. return gives 60 to result, print displays 60.
continue, break and return must remain three separate concepts. Do NOT imply break terminates the function; control next reaches return. Do not put return inside the for loop.
This poster must depict variables, function definition and call, parameter vs argument, loop, condition, break/continue, return, output and indentation in one cohesive annotated code scene. No extra code fragments, no second program, no panels or borders dividing the scene. No lists/dicts, files, classes, decorators or later-lecture subjects. Keep all 12 labels and the complete program readable. Keep all background walls, cups, book spines and desk notebooks free of decorative writing.

## Правка: убрать фоновые надписи и добавить значение по умолчанию

Use case: precise-object-edit.
Edit the supplied single-frame illustrated Python teaching poster. Apply the changes below carefully. Preserve its main composition as ONE scene, main title, warm illustration style, student in blue hoodie, green python with spectacles, large central board, all important educational callouts and clear typeset code.

1. REMOVE ALL DECORATIVE TEXT in the room. Completely remove the small motivational posters on the background wall (upper right and middle left); replace them with the natural wall texture. Remove the writing from BOTH cups/mugs on the desk; make them plain ceramic. Also leave background book spines and the small desk notebook unlettered to keep the scene visually quiet. Do not add any new background posters, slogans, words or decorative symbols. KEEP the main poster title, subtitle, educational labels, central Python program and laptop output — these are teaching content, not decorative posters.

2. ADD a second function parameter with a default value. The complete code on the large board must now be EXACTLY:
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

The second parameter is precisely goal=60, with no spaces around the equals sign in this unannotated default parameter. Change the stopping comparison from total >= 60 to total >= goal. Do not change the call: read_pages(daily_pages) supplies only the first argument, so the second parameter takes its default 60. Laptop output stays exactly «Вывод: 60».

3. Replace educational callout number 2 with:
Heading: «2. Параметры»
Body line 1: «portion — обязательный»
Body line 2: «goal=60 — по умолчанию»
Body line 3: «int — аннотация типа»
Use two short accurate leader pointers from this label to portion and goal=60 in the definition, respectively; the pointers must not cover any code character. Reposition or widen the label if needed.

4. Keep callout number 10 as «10. Вызов функции» with «Здесь выполняется её тело» and add a short clearly legible line «goal не передан: берётся 60». This label points at the call read_pages(daily_pages). Callout 11 still explains the argument: «Значение daily_pages: 20». Keep parameter vs argument clear.

5. ENSURE ALL CODE INDENTATION AND IDENTIFIERS ARE CORRECT. Align the initial def and the three final top-level lines at exactly the same left x-coordinate. The four-space-indented lines total=0, for, and return must align with one another. The two if lines and total += portion are indented 8 spaces. continue and break are indented 12 spaces. Keep underscores in read_pages and daily_pages visible. Widen or modestly reposition the code area if needed so that the full longer definition line is readable and does not collide with labels. Never omit or abbreviate code.

6. CORRECT the continue flow depiction. In the input image the small curved green arrow below continue points towards the if statement, which is misleading. REMOVE that small curved arrow entirely. KEEP the clear leader arrow from the «6. continue» explanatory label to the continue keyword. The wording «Следующая итерация цикла» is correct and sufficient. Keep the red break flow arrow leading out of the for loop to return total. Keep return visibly OUTSIDE the for loop but INSIDE the function.

All other main headings and educational labels remain. Exactly one continuous poster scene, no panels, no extra code samples, no extra decorative words. Proofread every Russian line, default argument syntax, whitespace alignment and the complete code.

## Финальное уточнение выравнивания

FINAL HIGH-PRIORITY LAYOUT CORRECTION:
The three top-level lines at the bottom are currently horizontally indented relative to def. This is incorrect for this educational code poster. Put their first character at EXACTLY THE SAME horizontal coordinate as the d in def (approximately x=300 on a 1024px-wide poster):
daily_pages = 20
result = read_pages(daily_pages)
print(result)
That means shifting all three bottom code lines approximately 45 pixels LEFT from the supplied image. They must NOT line up with return, which is correctly indented inside the function. Keep def at x≈300, total/for/return at x≈355, both if statements and total += portion at x≈412, continue/break at x≈468. These form a rigorous 4-space indentation grid. Update the lower label pointer lines to follow the shifted text. This horizontal alignment is ESSENTIAL. Do not draw these bottom lines as a separate code block with its own arbitrary origin.
Keep the function-definition line fully legible as def read_pages(portion: int, goal=60) -> int: with true underscores and visible spaces around ->. If needed, use a slightly narrower monospace font for that one longer line rather than compressing characters.
Apply all the cleanup and second-default-parameter changes described above.
