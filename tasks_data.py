# ====================== ДАННЫЕ ЗАДАНИЙ И ШТРАФОВ ======================
# type: "simple" — одна галочка, "choice" — выбор из 2 вариантов (только один)
# limit: максимальное число нажатий (None = бесконечно)

TASKS = [
    # ===== QR-задания =====
    {"name": "Доставка сена Х2 (QR)", "type": "choice", "options": [
        {"label": "Р", "value": 3},
        {"label": "А", "value": 10}
    ], "group": "QR"},
    {"name": "Перенос в пройденную ячейку (QR)", "type": "choice", "options": [
        {"label": "Р", "value": 3},
        {"label": "А", "value": 10}
    ], "group": "QR"},
    {"name": "Баллы за гипнодиск x2 (3 оборота) (QR)", "type": "choice", "options": [
        {"label": "Р", "value": 3},
        {"label": "А", "value": 10}
    ], "group": "QR"},
    {"name": "Второе вмешательство (QR)", "type": "choice", "options": [
        {"label": "Р", "value": 3},
        {"label": "А", "value": 10}
    ], "group": "QR"},
    
    # ===== Маяки: красный =====
    {"name": "Захват красного маяка", "type": "choice", "options": [
        {"label": "Р", "value": 6},
        {"label": "А", "value": 12}
    ], "group": "Красный маяк"},
    {"name": "Захват красного маяка на стойке", "type": "choice", "options": [
        {"label": "Р", "value": 9},
        {"label": "А", "value": 16}
    ], "group": "Красный маяк"},
    {"name": "Доставка красного маяка", "type": "simple", "options": [
        {"label": "✓", "value": 10}
    ], "group": "Красный маяк"},
    
    # ===== Маяки: синий =====
    {"name": "Захват синего маяка", "type": "choice", "options": [
        {"label": "Р", "value": 6},
        {"label": "А", "value": 12}
    ], "group": "Синий маяк"},
    {"name": "Захват синего маяка на стойке", "type": "choice", "options": [
        {"label": "Р", "value": 9},
        {"label": "А", "value": 16}
    ], "group": "Синий маяк"},
    {"name": "Доставка синего маяка", "type": "simple", "options": [
        {"label": "✓", "value": 10}
    ], "group": "Синий маяк"},
    
    # ===== Маяки: зелёный =====
    {"name": "Захват зелёного маяка", "type": "choice", "options": [
        {"label": "Р", "value": 6},
        {"label": "А", "value": 12}
    ], "group": "Зелёный маяк"},
    {"name": "Захват зелёного маяка на стойке", "type": "choice", "options": [
        {"label": "Р", "value": 9},
        {"label": "А", "value": 16}
    ], "group": "Зелёный маяк"},
    {"name": "Доставка зелёного маяка", "type": "simple", "options": [
        {"label": "✓", "value": 10}
    ], "group": "Зелёный маяк"},
    
    # ===== Маяки: жёлтый =====
    {"name": "Захват жёлтого маяка", "type": "choice", "options": [
        {"label": "Р", "value": 6},
        {"label": "А", "value": 12}
    ], "group": "Жёлтый маяк"},
    {"name": "Захват жёлтого маяка на стойке", "type": "choice", "options": [
        {"label": "Р", "value": 9},
        {"label": "А", "value": 16}
    ], "group": "Жёлтый маяк"},
    {"name": "Доставка жёлтого маяка", "type": "simple", "options": [
        {"label": "✓", "value": 10}
    ], "group": "Жёлтый маяк"},
    
    # ===== Спец. маяк =====
    {"name": "Захват спец. маяка", "type": "choice", "options": [
        {"label": "Р", "value": 8},
        {"label": "А", "value": 15}
    ], "group": "Спец. маяк"},
    {"name": "Доставка спец. маяка на поле", "type": "simple", "options": [
        {"label": "✓", "value": 10}
    ], "group": "Спец. маяк"},
    {"name": "Доставка спец. маяка в ящик", "type": "simple", "options": [
        {"label": "✓", "value": 15}
    ], "group": "Спец. маяк"},
    
    # ===== Тяжёлый маяк =====
    {"name": "Захват тяжёлого маяка", "type": "choice", "options": [
        {"label": "Р", "value": 8},
        {"label": "А", "value": 15}
    ], "group": "Тяжёлый маяк"},
    {"name": "Доставка тяжёлого маяка на поле", "type": "simple", "options": [
        {"label": "✓", "value": 15}
    ], "group": "Тяжёлый маяк"},
    {"name": "Доставка тяжёлого маяка в ящик", "type": "simple", "options": [
        {"label": "✓", "value": 18}
    ], "group": "Тяжёлый маяк"},
    
    # ===== Белый маяк =====
    {"name": "Захват белого маяка", "type": "simple", "options": [
        {"label": "✓", "value": 10}
    ], "group": "Белый маяк"},
    {"name": "Доставка белого маяка", "type": "simple", "options": [
        {"label": "✓", "value": 20}
    ], "group": "Белый маяк"},
    
    # ===== Прочее =====
    {"name": "Минибашенка", "type": "simple", "options": [
        {"label": "✓", "value": 20}
    ], "group": "Прочее"},
    {"name": "Обломок", "type": "simple", "options": [
        {"label": "✓", "value": 4}
    ], "limit": None, "group": "Прочее"},
    {"name": "Доставка обломка", "type": "simple", "options": [
        {"label": "✓", "value": 3}
    ], "limit": None, "group": "Прочее"},
    {"name": "Провалы обломок", "type": "simple", "options": [
        {"label": "✓", "value": 13}
    ], "limit": 2, "group": "Прочее"},
    {"name": "Захват мяча (траншея)", "type": "simple", "options": [
        {"label": "✓", "value": 4}
    ], "limit": 5, "group": "Мяч"},
    {"name": "Доставка мяча", "type": "simple", "options": [
        {"label": "✓", "value": 3}
    ], "limit": 5, "group": "Мяч"},
    {"name": "Кнопка", "type": "simple", "options": [
        {"label": "✓", "value": 3}
    ], "limit": 3, "group": "Прочее"},
    {"name": "Захват флага", "type": "simple", "options": [
        {"label": "✓", "value": 15}
    ], "group": "Прочее"},
    {"name": "Извлечь (трубы)", "type": "simple", "options": [
        {"label": "✓", "value": 8}
    ], "limit": 5, "group": "Трубы"},
    {"name": "Изучить (трубы)", "type": "simple", "options": [
        {"label": "✓", "value": 5}
    ], "group": "Трубы"},
    {"name": "180 (трубы)", "type": "simple", "options": [
        {"label": "✓", "value": 9}
    ], "limit": 5, "group": "Трубы"},
    {"name": "360 (трубы)", "type": "simple", "options": [
        {"label": "✓", "value": 12}
    ], "limit": 5, "group": "Трубы"},
    {"name": "Мишень", "type": "simple", "options": [
        {"label": "1", "value": 4},
        {"label": "2", "value": 8},
        {"label": "3", "value": 12},
        {"label": "4", "value": 16},
        {"label": "5", "value": 20}
    ], "group": "Прочее"},
    {"name": "Рычаг (вентили)", "type": "simple", "options": [
        {"label": "1", "value": 8},
        {"label": "2", "value": 8}
    ], "group": "Вентили"},
    {"name": "Баб. кр (вентили)", "type": "simple", "options": [
        {"label": "✓", "value": 15}
    ], "group": "Вентили"},
    {"name": "Вент (Вентили)", "type": "simple", "options": [
        {"label": "✓", "value": 20}
    ], "group": "Вентили"},
    {"name": "Баб. жел", "type": "simple", "options": [
        {"label": "✓", "value": 10}
    ], "group": "Прочее"},
    {"name": "Дверь на себя", "type": "simple", "options": [
        {"label": "✓", "value": 9}
    ], "group": "Прочее"},
    {"name": "Дверь от себя", "type": "simple", "options": [
        {"label": "✓", "value": 1}
    ], "group": "Прочее"},
    {"name": "Управляемый переворот", "type": "simple", "options": [
        {"label": "✓", "value": 15}
    ], "group": "Прочее"},
    {"name": "Знак опасности", "type": "simple", "options": [
        {"label": "1", "value": 15},
        {"label": "2", "value": 15},
        {"label": "3", "value": 15},
        {"label": "4", "value": 15}
    ], "group": "Прочее"},
    {"name": "Захват сена", "type": "simple", "options": [
        {"label": "✓", "value": 5}
    ], "limit": 4, "group": "Сено"},
    {"name": "Доставка сена", "type": "simple", "options": [
        {"label": "✓", "value": 5}
    ], "limit": 4, "group": "Сено"},
    {"name": "Захват мусора", "type": "simple", "options": [
        {"label": "✓", "value": 4}
    ], "limit": 8, "group": "Мусор"},
    {"name": "Доставка мусора", "type": "simple", "options": [
        {"label": "✓", "value": 4}
    ], "limit": 8, "group": "Мусор"},
]

PENALTIES = [
    {"name": "Падение в люк", "type": "simple", "options": [
        {"label": "1", "value": -6},
        {"label": "2", "value": -6}
    ], "group": "Штрафы"},
    {"name": "Отваливающиеся детали", "type": "simple", "options": [
        {"label": "✓", "value": -2}
    ], "limit": None, "group": "Штрафы"},
    {"name": "Отвалив. группа деталей (>4)", "type": "simple", "options": [
        {"label": "✓", "value": -5}
    ], "limit": None, "group": "Штрафы"},
    {"name": "Доставка не в тот бак", "type": "simple", "options": [
        {"label": "✓", "value": -2}
    ], "limit": 2, "group": "Штрафы"},
    {"name": "Переход в автомат (2 раза)", "type": "simple", "options": [
        {"label": "✓", "value": -1}
    ], "limit": None, "group": "Штрафы"},
    {"name": "Перенос попытки", "type": "simple", "options": [
        {"label": "✓", "value": -15}
    ], "group": "Штрафы"},
    {"name": "Подрыв на мине", "type": "simple", "options": [
        {"label": "1", "value": -8},
        {"label": "2", "value": -8},
        {"label": "3", "value": -8}
    ], "group": "Штрафы"},
    {"name": "Повреждение полигона", "type": "simple", "options": [
        {"label": "✓", "value": -5}
    ], "limit": None, "group": "Штрафы"},
    {"name": "Вмешательство", "type": "simple", "options": [
        {"label": "✓", "value": -7}
    ], "limit": 2, "group": "Штрафы"},
    {"name": "За сбитую корову/разм. коровой", "type": "simple", "options": [
        {"label": "✓", "value": -5}
    ], "limit": 10, "group": "Штрафы"},
    {"name": "За упавший опасный объект", "type": "simple", "options": [
        {"label": "✓", "value": -5}
    ], "group": "Штрафы"},
    {"name": "Подсказки/Неспорт. поведение", "type": "simple", "options": [
        {"label": "1", "value": -5},
        {"label": "2", "value": -5},
        {"label": "3", "value": -10}
    ], "group": "Штрафы"},
]
