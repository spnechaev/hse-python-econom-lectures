import CoreGraphics
import CoreText
import Foundation

// Standalone one-page A4 poster based on reference/group-project.md.
let pageWidth: CGFloat = 595.28
let pageHeight: CGFloat = 841.89
let margin: CGFloat = 34
let output = URL(fileURLWithPath: "output/pdf/group_project_topics_poster_a4.pdf")
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

func makeLine(_ value: String, size: CGFloat, bold: Bool,
              color: CGColor? = nil) -> CTLine {
    var attrs: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): font(size, bold: bold)
    ]
    if let color {
        attrs[NSAttributedString.Key(kCTForegroundColorAttributeName as String)] = color
    }
    return CTLineCreateWithAttributedString(
        NSAttributedString(string: value, attributes: attrs)
    )
}

func textWidth(_ value: String, size: CGFloat, bold: Bool = false) -> CGFloat {
    CGFloat(CTLineGetTypographicBounds(
        makeLine(value, size: size, bold: bold), nil, nil, nil
    ))
}

func textLine(_ value: String, x: CGFloat, top: CGFloat, size: CGFloat,
              color: CGColor = ink, bold: Bool = false) {
    let face = font(size, bold: bold)
    let ctLine = makeLine(value, size: size, bold: bold, color: color)
    context.textPosition = CGPoint(x: x, y: pageHeight - top - CTFontGetAscent(face))
    CTLineDraw(ctLine, context)
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
    context.addPath(CGPath(
        roundedRect: rect, cornerWidth: radius, cornerHeight: radius, transform: nil
    ))
    context.setFillColor(fill)
    if let stroke {
        context.setStrokeColor(stroke)
        context.setLineWidth(0.8)
        context.drawPath(using: .fillStroke)
    } else {
        context.fillPath()
    }
}

let topics: [(title: String, detail: String)] = [
    (
        "Куда уходят деньги?",
        "Студент записывает покупки; видит траты по категориям и сравнение с месячными лимитами."
    ),
    (
        "Насколько подорожала привычная корзина?",
        "Покупатель выбирает продукты и два месяца; видит изменение стоимости и вклад каждого товара."
    ),
    (
        "Какие товары приносят магазину деньги?",
        "Владелец загружает продажи, закупочные цены и возвраты; видит прибыль по товарам."
    ),
    (
        "Сколько нужно продать, чтобы не работать в убыток?",
        "Владелец кофейни вводит цену и затраты; видит порог безубыточности и график прибыли."
    ),
    (
        "Хватит ли денег на ближайшие платежи?",
        "Владелец бизнеса вводит остаток, поступления и платежи; видит график денег и дату дефицита."
    ),
    (
        "Какой тариф связи выбрать для курьеров?",
        "Менеджер доставки вводит расход связи курьеров и тарифы; видит месячную стоимость с доплатой сверх пакета."
    ),
    (
        "Что пора заказать в магазин?",
        "Управляющий указывает остатки, продажи и срок поставки; видит товары, которые скоро закончатся."
    ),
    (
        "У кого закупиться дешевле?",
        "Кафе задаёт список товаров, цены, доставку и наличие; получает самый дешёвый допустимый вариант."
    ),
    (
        "В каких регионах цены росли быстрее?",
        "Редакция выбирает годы; видит диаграмму роста цен по регионам и пропуски в данных."
    ),
    (
        "Телеграм-бот для учёта расходов",
        "Студент пишет боту сумму и категорию; получает траты за месяц и остаток лимита."
    ),
    (
        "Игра про небольшой магазин",
        "Игрок выбирает закупку и цену; после ходов видит выручку, расходы, остатки и прибыль."
    ),
    (
        "Распознавание лиц на фотографиях мероприятия",
        "Организатор выбирает портреты добровольцев; видит знакомые лица и неуверенные совпадения."
    ),
]

context.beginPDFPage(nil)
context.setFillColor(paper)
context.fill(CGRect(x: 0, y: 0, width: pageWidth, height: pageHeight))

context.setFillColor(navy)
context.fill(CGRect(x: 0, y: pageHeight - 143, width: pageWidth, height: 143))
textLine("ИТОГОВЫЙ ПРОЕКТ · PYTHON", x: margin, top: 24, size: 10.5,
         color: rgb(0x7BE0CF), bold: true)
textLine("12 тем для проекта", x: margin, top: 51, size: 29,
         color: white, bold: true)
textLine("Кто пользуется → что делает → что получает", x: margin,
         top: 101, size: 13, color: rgb(0xD9E8EF))

let cardTop: CGFloat = 159
let cardHeight: CGFloat = 100
let rowGap: CGFloat = 7
let columnGap: CGFloat = 13
let cardWidth = (pageWidth - 2 * margin - columnGap) / 2

for index in topics.indices {
    let column = index / 6
    let row = index % 6
    let x = margin + CGFloat(column) * (cardWidth + columnGap)
    let top = cardTop + CGFloat(row) * (cardHeight + rowGap)
    box(x: x, top: top, width: cardWidth, height: cardHeight,
        radius: 9, fill: white, stroke: line)
    textLine(String(format: "%02d", index + 1), x: x + 12, top: top + 11,
             size: 10, color: teal, bold: true)
    let titleEnd = wrapped(
        topics[index].title,
        x: x + 38, top: top + 10, width: cardWidth - 50,
        size: 11.1, leading: 13.3, color: ink, bold: true
    )
    let detailTop = max(top + 34, titleEnd + 4)
    let detailEnd = wrapped(
        topics[index].detail,
        x: x + 12, top: detailTop, width: cardWidth - 24,
        size: 9.4, leading: 11.5, color: muted
    )
    precondition(
        detailEnd <= top + cardHeight - 5,
        "Topic \(index + 1) does not fit its card"
    )
}

textLine("Можно предложить свою тему. Уникальность нужна только внутри семинарской группы.",
         x: margin, top: 810, size: 9.8, color: teal)

context.endPDFPage()
context.closePDF()
print(output.path)
