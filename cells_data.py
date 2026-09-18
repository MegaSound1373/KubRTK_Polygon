# ====================== ДАННЫЕ ВСЕХ КЛЕТОК ======================
# shape: (кол-во клеток в ряд, кол-во клеток в столбец) или "L" для L-образной
# parts: список частей клетки, каждая часть = одно нажатие
# limit: максимальное число нажатий (None = бесконечно)

CELL_DEFINITIONS = [
    # ===== Обычные клетки =====
    {"name": "Брёвна", "shape": (1,1), "parts": [{"label": "12", "value": 12, "group": None}]},
    {"name": "Буераки", "shape": (1,1), "parts": [{"label": "17", "value": 17, "group": None}]},
    {"name": "Гипнодиск", "shape": (1,1), "parts": [{"label": "13", "value": 13, "group": None}]},
    {"name": "Горка с трубами", "shape": (1,1), "parts": [
        {"label": "17", "value": 17, "group": None},
        {"label": "30A", "value": 30, "group": None}
    ]},
    {"name": "Дверь", "shape": (1,1), "parts": [
        {"label": "1", "value": 1, "group": None},
        {"label": "9", "value": 9, "group": None}
    ]},
    {"name": "Завал", "shape": (1,1), "parts": [{"label": "12", "value": 12, "group": None}]},
    {"name": "Звёздочки", "shape": (1,1), "parts": [{"label": "9", "value": 9, "group": None}]},
    {"name": "Изгородь", "shape": (1,1), "parts": [{"label": "5", "value": 5, "group": None}]},
    {"name": "Камни, камни с травой", "shape": (1,1), "parts": [{"label": "2", "value": 2, "group": None}]},
    {"name": "Качели", "shape": (1,1), "parts": [
        {"label": "12", "value": 12, "group": None},
        {"label": "4", "value": 4, "group": None}
    ]},
    {"name": "Керамзит", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Копыто", "shape": (1,1), "parts": [
        {"label": "15", "value": 15, "group": None},
        {"label": "40A", "value": 40, "group": None}
    ]},
    {"name": "Крыша", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Лёд", "shape": (1,1), "parts": [{"label": "1", "value": 1, "group": None}]},
    {"name": "Лес", "shape": (1,1), "parts": [{"label": "5", "value": 5, "group": None}]},
    {"name": "Люк", "shape": (1,1), "parts": [
        {"label": "9", "value": 9, "group": None},
        {"label": "2", "value": 2, "group": None}
    ]},
    {"name": "Мины", "shape": (1,1), "parts": [
        {"label": "4", "value": 4, "group": None},
        {"label": "4", "value": 4, "group": None},
        {"label": "4", "value": 4, "group": None},
        {"label": "1", "value": 1, "group": None}
    ]},
    {"name": "Мосты", "shape": (1,1), "parts": [
        {"label": "1", "value": 1, "group": None},
        {"label": "3", "value": 3, "group": None}
    ]},
    {"name": "Овраг", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Песок", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Провалы", "shape": (1,1), "parts": [
        {"label": "6", "value": 6, "group": None},
        {"label": "10A", "value": 10, "group": None}
    ]},
    {"name": "Провода", "shape": (1,1), "parts": [{"label": "5", "value": 5, "group": None}]},
    {"name": "Разбитая дорога", "shape": (1,1), "parts": [{"label": "5", "value": 5, "group": None}]},
    {"name": "Рампы «Волны»", "shape": (1,1), "parts": [{"label": "4", "value": 4, "group": None}]},
    {"name": "Рампы «Прямые»", "shape": (1,1), "parts": [{"label": "7", "value": 7, "group": None}]},
    {"name": "Рампы «Скаты»", "shape": (1,1), "parts": [{"label": "4", "value": 4, "group": None}]},
    {"name": "Рёбра", "shape": (1,1), "parts": [{"label": "4", "value": 4, "group": None}]},
    {"name": "Рельсы", "shape": (1,1), "parts": [
        {"label": "6", "value": 6, "group": None},
        {"label": "4", "value": 4, "group": None}
    ]},
    {"name": "Решето", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Ролики", "shape": (1,1), "parts": [{"label": "6", "value": 6, "group": None}]},
    {"name": "Сетка", "shape": (1,1), "parts": [{"label": "2", "value": 2, "group": None}]},
    {"name": "Сломанные весы", "shape": (1,1), "parts": [{"label": "4", "value": 4, "group": None}]},
    {"name": "Сталкер", "shape": (1,1), "parts": [
        {"label": "6", "value": 6, "group": None},
        {"label": "20A", "value": 20, "group": None}
    ]},
    {"name": "Тир", "shape": (1,1), "parts": [{"label": "0", "value": 0, "group": None}]},
    {"name": "Трава", "shape": (1,1), "parts": [{"label": "1", "value": 1, "group": None}]},
    {"name": "Траншея", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Трясина", "shape": (1,1), "parts": [{"label": "8", "value": 8, "group": None}]},
    {"name": "Туман", "shape": (3,1), "parts": [
        {"label": "5", "value": 5, "group": None},
        {"label": "5", "value": 5, "group": None},
        {"label": "5", "value": 5, "group": None}
    ]},
    {"name": "Ухабы", "shape": (1,1), "parts": [{"label": "6", "value": 6, "group": None}]},
    {"name": "Шарики", "shape": (1,1), "parts": [{"label": "7", "value": 7, "group": None}]},
    {"name": "Шипы", "shape": (1,1), "parts": [{"label": "5", "value": 5, "group": None}]},
    {"name": "Шишки", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Эстакада", "shape": "L", "parts": [
        {"label": "13", "value": 13, "group": None},
        {"label": "40A", "value": 40, "group": None}
    ]},
    {"name": "Яма", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    
    # ===== Составные клетки =====
    {"name": "Большая лестница", "shape": (2,2), "parts": [
        {"label": "40", "value": 40, "group": "green"},
        {"label": "80A", "value": 80, "group": "green"},
        {"label": "10", "value": 10, "group": "red"},
        {"label": "30A", "value": 30, "group": "red"}
    ]},
    {"name": "Двухскатная дорога", "shape": (1,1), "parts": [{"label": "2", "value": 2, "group": None}]},
    {"name": "Мини лестница", "shape": (2,2), "parts": [
        {"label": "13", "value": 13, "group": "green"},
        {"label": "26A", "value": 26, "group": "green"},
        {"label": "10", "value": 10, "group": "red"}
    ]},
    {"name": "Наклонная ледяная", "shape": (1,1), "parts": [{"label": "2", "value": 2, "group": None}]},
    {"name": "Наклонная каменная", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Наклонная Травяная", "shape": (1,1), "parts": [{"label": "2", "value": 2, "group": None}]},
    {"name": "Наклонная 20°", "shape": (3,1), "parts": [
        {"label": "3", "value": 3, "group": "green"},
        {"label": "6A", "value": 6, "group": "green"},
        {"label": "3", "value": 3, "group": "red"}
    ]},
    {"name": "Наклонная 30°", "shape": (2,1), "parts": [
        {"label": "5", "value": 5, "group": "green"},
        {"label": "10A", "value": 10, "group": "green"},
        {"label": "3", "value": 3, "group": "red"}
    ]},
    {"name": "Наклонная с рампами", "shape": (1,1), "parts": [{"label": "5", "value": 5, "group": None}]},
    {"name": "Подвесной мост", "shape": (1,1), "parts": [
        {"label": "6", "value": 6, "group": None},
        {"label": "20A", "value": 20, "group": None}
    ]},
    {"name": "Невод", "shape": (1,1), "parts": [{"label": "7", "value": 7, "group": None}]},
    {"name": "Доска", "shape": (2,2), "parts": [
        {"label": "15", "value": 15, "group": "green"},
        {"label": "40A", "value": 40, "group": "green"},
        {"label": "7", "value": 7, "group": "red"}
    ]},
    {"name": "Карьер", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    {"name": "Высокие косые рампы", "shape": (1,1), "parts": [{"label": "9", "value": 9, "group": None}]},
    {"name": "Ёлочка", "shape": (1,1), "parts": [{"label": "4", "value": 4, "group": None}]},
    {"name": "Откидной мост", "shape": (1,1), "parts": [
        {"label": "2", "value": 2, "group": None},
        {"label": "6", "value": 6, "group": None}
    ]},
    {"name": "Двухполосный мост", "shape": (3,1), "parts": [{"label": "6", "value": 6, "group": None}]},
    {"name": "Ковролин", "shape": (1,1), "parts": [{"label": "1", "value": 1, "group": None}]},
    {"name": "Щётки", "shape": (1,1), "parts": [{"label": "3", "value": 3, "group": None}]},
    
    # ===== Новая клетка =====
    {"name": "Авто линия", "shape": (5,1), "parts": [
        {"label": "10", "value": 10, "group": None},
        {"label": "10", "value": 10, "group": None},
        {"label": "10", "value": 10, "group": None},
        {"label": "10", "value": 10, "group": None},
        {"label": "10", "value": 10, "group": None}
    ]},
    
    # ===== Стартовые клетки =====
    {"name": "Зелёный старт", "shape": (1,1), "parts": [], "group": "green", "is_start": True},
    {"name": "Красный старт", "shape": (1,1), "parts": [], "group": "red", "is_start": True},
]
