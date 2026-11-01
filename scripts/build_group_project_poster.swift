import CoreGraphics
import CoreText
import Foundation

// One-page A4 handout for reference/group-project.md.
let pageWidth: CGFloat = 595.28
let pageHeight: CGFloat = 841.89
let margin: CGFloat = 34
let output = URL(fileURLWithPath: "output/pdf/group_project_poster_a4.pdf")
try FileManager.default.createDirectory(
    at: output.deletingLastPathComponent(),
    withIntermediateDirectories: true
)

guard let consumer = CGDataConsumer(url: output as CFURL) else {
    fatalError("Cannot create PDF output")
}
var mediaBox = CGRect(x: 0, y: 0, width: pageWidth, height: pageHeight)
guard let context = CGContext(consumer: consumer, mediaBox: &mediaBox, nil) else {
    fatalError("Cannot create PDF context")
}

func rgb(_ hex: UInt32) -> CGColor {
    CGColor(
        red: CGFloat((hex >> 16) & 0xff) / 255,
        green: CGFloat((hex >> 8) & 0xff) / 255,
        blue: CGFloat(hex & 0xff) / 255,
        alpha: 1
    )
}

let navy = rgb(0x14263D)
let ink = rgb(0x192A3D)
let muted = rgb(0x526477)
let teal = rgb(0x087C77)
let pale = rgb(0xEAF5F2)
let line = rgb(0xD9E4E9)
let white = rgb(0xFFFFFF)
let paper = rgb(0xFAFCFC)

func font(_ size: CGFloat, bold: Bool = false) -> CTFont {
    CTFontCreateWithName(
        (bold ? "HelveticaNeue-Bold" : "HelveticaNeue") as CFString,
        size,
        nil
    )
}

func textLine(_ value: String, x: CGFloat, top: CGFloat, size: CGFloat,
              color: CGColor = ink, bold: Bool = false) {
    let face = font(size, bold: bold)
    let attrs: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): face,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): color,
    ]
    let attributed = NSAttributedString(string: value, attributes: attrs)
    let ctLine = CTLineCreateWithAttributedString(attributed)
    context.textPosition = CGPoint(
        x: x,
        y: pageHeight - top - CTFontGetAscent(face)
    )
    CTLineDraw(ctLine, context)
}

func textWidth(_ value: String, size: CGFloat, bold: Bool = false) -> CGFloat {
    let attrs: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): font(size, bold: bold)
    ]
    let ctLine = CTLineCreateWithAttributedString(
        NSAttributedString(string: value, attributes: attrs)
    )
    return CGFloat(CTLineGetTypographicBounds(ctLine, nil, nil, nil))
}

@discardableResult
func wrapped(_ value: String, x: CGFloat, top: CGFloat, width: CGFloat,
             size: CGFloat, leading: CGFloat, color: CGColor = ink,
             bold: Bool = false) -> CGFloat {
    var cursor = top
    for paragraph in value.components(separatedBy: "\n") {
        var current = ""
        for word in paragraph.split(separator: " ") {
            let candidate = current.isEmpty ? String(word) : current + " " + word
            if !current.isEmpty && textWidth(candidate, size: size, bold: bold) > width {
                textLine(current, x: x, top: cursor, size: size, color: color, bold: bold)
                cursor += leading
                current = String(word)
            } else {
                current = candidate
            }
        }
        if !current.isEmpty {
            textLine(current, x: x, top: cursor, size: size, color: color, bold: bold)
            cursor += leading
        }
    }
    return cursor
}

func box(x: CGFloat, top: CGFloat, width: CGFloat, height: CGFloat,
         radius: CGFloat, fill: CGColor, stroke: CGColor? = nil) {
    let rect = CGRect(x: x, y: pageHeight - top - height, width: width, height: height)
    let path = CGPath(
        roundedRect: rect,
        cornerWidth: radius,
        cornerHeight: radius,
        transform: nil
    )
    context.addPath(path)
    context.setFillColor(fill)
    if let stroke {
        context.setStrokeColor(stroke)
        context.setLineWidth(0.8)
        context.drawPath(using: .fillStroke)
    } else {
        context.fillPath()
    }
}

func section(_ number: String, _ title: String, top: CGFloat) {
    textLine(number, x: margin, top: top + 1, size: 11, color: teal, bold: true)
    textLine(title, x: margin + 36, top: top, size: 17, color: navy, bold: true)
}

context.beginPDFPage(nil)
context.setFillColor(paper)
context.fill(CGRect(x: 0, y: 0, width: pageWidth, height: pageHeight))

// Header
context.setFillColor(navy)
context.fill(CGRect(x: 0, y: pageHeight - 200, width: pageWidth, height: 200))
textLine("ИТОГОВЫЙ ПРОЕКТ · PYTHON", x: margin, top: 24, size: 10.5,
         color: rgb(0x7BE0CF), bold: true)
textLine("От идеи до работающего", x: margin, top: 52, size: 27,
         color: white, bold: true)
textLine("продукта", x: margin, top: 84, size: 27, color: white, bold: true)
textLine("Один полезный сценарий для реального пользователя", x: margin,
         top: 126, size: 13, color: rgb(0xD9E8EF))

let chips: [(String, CGFloat, CGFloat)] = [
    ("1–3 человека", 34, 132),
    ("до 7 ноября", 174, 122),
    ("защита · семинар 14", 304, 222),
]
for (label, x, width) in chips {
    box(x: x, top: 160, width: width, height: 26, radius: 6, fill: rgb(0x29465B))
    textLine(label, x: x + 10, top: 166, size: 10.5, color: white, bold: true)
}

// Start
section("01", "Старт", top: 218)
let cardTop: CGFloat = 247
let gap: CGFloat = 12
let cardWidth = (pageWidth - 2 * margin - gap) / 2
box(x: margin, top: cardTop, width: cardWidth, height: 113, radius: 10,
    fill: white, stroke: line)
box(x: margin + cardWidth + gap, top: cardTop, width: cardWidth, height: 113,
    radius: 10, fill: white, stroke: line)
textLine("Выберите задачу", x: margin + 15, top: cardTop + 14, size: 13,
         color: ink, bold: true)
wrapped("Тема из списка или своя. В пределах семинарской группы темы не повторяются.",
        x: margin + 15, top: cardTop + 38, width: cardWidth - 30,
        size: 10.7, leading: 14.5, color: muted)
textLine("Зарегистрируйте", x: margin + cardWidth + gap + 15,
         top: cardTop + 14, size: 13, color: ink, bold: true)
wrapped("До 7 ноября у семинариста: имена, что делает программа и какие технологии нужны. Канал он сообщит.",
        x: margin + cardWidth + gap + 15, top: cardTop + 38,
        width: cardWidth - 30, size: 10.7, leading: 14.5, color: muted)

// Product
section("02", "Продукт", top: 378)
box(x: margin, top: 407, width: pageWidth - 2 * margin, height: 147,
    radius: 10, fill: white, stroke: line)
let flowLabels = ["ЧЕЛОВЕК", "ИНТЕРФЕЙС", "ЛОГИКА PYTHON", "РЕЗУЛЬТАТ"]
let flowNotes = [
    "вводит или выбирает данные",
    "страница, окно, бот, игра, меню",
    "расчёты, правила, алгоритм",
    "понятный вывод и рисунки",
]
let innerX = margin + 15
let flowGap: CGFloat = 7
let flowWidth = (pageWidth - 2 * margin - 30 - 3 * flowGap) / 4
for index in 0..<4 {
    let x = innerX + CGFloat(index) * (flowWidth + flowGap)
    box(x: x, top: 422, width: flowWidth, height: 75, radius: 7,
        fill: pale)
    textLine(flowLabels[index], x: x + 8, top: 433, size: 9.3,
             color: teal, bold: true)
    wrapped(flowNotes[index], x: x + 8, top: 451, width: flowWidth - 16,
            size: 9.3, leading: 11.5, color: ink)
}
wrapped("Пользователь не работает с JSON и длинными файлами. Графики и диаграммы — изображениями. В коде: аннотации типов и обработка ошибок.",
        x: margin + 16, top: 508, width: pageWidth - 2 * margin - 32,
        size: 10.2, leading: 14, color: muted)

// Defense
section("03", "Защита", top: 571)
box(x: margin, top: 601, width: pageWidth - 2 * margin, height: 112,
    radius: 10, fill: navy)
textLine("ГЛАВНОЕ — ЖИВАЯ ДЕМОНСТРАЦИЯ", x: margin + 17,
         top: 616, size: 15.5, color: white, bold: true)
wrapped("Через интерфейс: данные → действие → результат. Каждый автор объясняет техническое решение, ограничения и отвечает на вопросы.",
        x: margin + 17, top: 644, width: pageWidth - 2 * margin - 34,
        size: 10.8, leading: 14.5, color: rgb(0xE5F0F4))
textLine("Слайды и презентация необязательны: они могут быть планом рассказа.",
         x: margin + 17, top: 686, size: 9.8, color: rgb(0x99E3D5))

// Submission and footer
section("04", "Сдача", top: 730)
wrapped("Код и данные для показа — архивом или ссылкой на репозиторий. Короткий README: установка, запуск, пример результата и вклад авторов.",
        x: margin + 36, top: 756, width: pageWidth - 2 * margin - 36,
        size: 10.4, leading: 13.5, color: ink)
context.setStrokeColor(line)
context.setLineWidth(0.8)
context.move(to: CGPoint(x: margin, y: pageHeight - 802))
context.addLine(to: CGPoint(x: pageWidth - margin, y: pageHeight - 802))
context.strokePath()
textLine("Git и автотесты — по желанию  ·  Без промежуточных сдач",
         x: margin, top: 810, size: 9.6, color: muted)
textLine("40% оценки за практику", x: pageWidth - margin - 148,
         top: 810, size: 9.6, color: teal, bold: true)

context.endPDFPage()
context.closePDF()
print(output.path)
