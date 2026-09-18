import json
import os

# ✅ Настройка шрифта с кириллицей ДО импорта App
from kivy.core.text import LabelBase
from kivy.resources import resource_add_path

resource_add_path(os.path.dirname(__file__))

_roboto_path = os.path.join(os.path.dirname(__file__), "Roboto-Regular.ttf")
if os.path.exists(_roboto_path):
    LabelBase.register(
        name='Roboto',
        fn_regular=_roboto_path
    )
FONT = 'Roboto'

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.clock import Clock

from cells_data import CELL_DEFINITIONS
from tasks_data import TASKS, PENALTIES


# ====================== УТИЛИТЫ ======================

def get_scheme_path():
    """Путь для сохранения схемы (работает на Android/iOS)."""
    return os.path.join(App.get_running_app().user_data_dir, "scheme.json")


def show_popup(title, text):
    """Попап с кнопкой ОК — не зависает на мобильных."""
    content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
    lbl = Label(text=text, halign='center', valign='middle', font_name=FONT)
    lbl.bind(size=lbl.setter('text_size'))
    content.add_widget(lbl)
    btn = Button(text="OK", size_hint_y=None, height=dp(44), font_name=FONT)
    content.add_widget(btn)
    popup = Popup(title=title, content=content,
                  size_hint=(0.85, 0.35), auto_dismiss=True,
                  title_font=FONT)
    btn.bind(on_press=popup.dismiss)
    popup.open()
    return popup


# ====================== ИГРОВОЕ ПОЛЕ ======================

class GameField(FloatLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.cells_on_field = []
        self.grid_cols = 12
        self.grid_rows = 20
        self.cell_size = 40

        self.padding_left = 1
        self.padding_right = 1
        self.padding_top = 1
        self.padding_bottom = 1

        self.offset_x = 0
        self.offset_y = 0

        # ✅ Зум
        self.zoom_level = 1.0
        self.base_cell_size = None

        # ✅ Фиксируем высоту поля под размер сетки
        self.size_hint_y = None
        self.bind(width=self.update_cell_size)

        self.canvas_widget = Widget()
        self.add_widget(self.canvas_widget)

    def update_cell_size(self, *args):
        if self.width <= 0:
            return

        avail_width = self.width / (self.grid_cols + self.padding_left + self.padding_right)
        self.base_cell_size = avail_width

        self.cell_size = self.base_cell_size * self.zoom_level

        total_height = (self.grid_rows + self.padding_top + self.padding_bottom) * self.cell_size
        self.height = total_height

        total_width = self.grid_cols * self.cell_size
        self.offset_x = (self.width - total_width) / 2
        self.offset_y = self.padding_bottom * self.cell_size

        self.redraw()

    def redraw(self):
        self.canvas_widget.canvas.clear()

        for child in self.canvas_widget.children[:]:
            if isinstance(child, Label):
                self.canvas_widget.remove_widget(child)

        with self.canvas_widget.canvas:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)

            Color(0.85, 0.85, 0.85, 1)
            for i in range(self.grid_cols + 1):
                x = self.offset_x + i * self.cell_size
                Line(points=[x, self.offset_y, x,
                             self.offset_y + self.grid_rows * self.cell_size], width=1)
            for j in range(self.grid_rows + 1):
                y = self.offset_y + j * self.cell_size
                Line(points=[self.offset_x, y,
                             self.offset_x + self.grid_cols * self.cell_size, y], width=1)

            Color(0.3, 0.3, 0.3, 1)
            Line(rectangle=(
                self.offset_x,
                self.offset_y,
                self.grid_cols * self.cell_size,
                self.grid_rows * self.cell_size
            ), width=2)

        # ✅ Группируем клетки 1×1 по позиции, остальные — отдельно
        simple_cells = {}
        other_cells = []

        for cell in self.cells_on_field:
            shape = cell["shape"]
            if shape == (1, 1) and not cell.get("is_start"):
                key = (cell["col"], cell["row"])
                simple_cells.setdefault(key, []).append(cell)
            else:
                other_cells.append(cell)

        for cell in other_cells:
            self.draw_cell(cell)

        for (col, row), cells in simple_cells.items():
            self.draw_stacked_cells(col, row, cells)

    # ✅ Раскладка частей внутри клетки (доли от размера клетки)
    def get_part_rects(self, n, gap=0.08):
        if n == 1:
            return [(0.0, 0.0, 1.0, 1.0)]

        if n == 2:
            return [
                (0.0,          0.0, 0.5 - gap / 2, 1.0),
                (0.5 + gap / 2, 0.0, 0.5 - gap / 2, 1.0),
            ]

        if n == 3:
            w = 1.0 / 3.0 - gap / 2
            return [
                (0.0,              0.0, w, 1.0),
                (1.0 / 3.0 + gap / 2, 0.0, w, 1.0),
                (2.0 / 3.0 + gap / 2, 0.0, w, 1.0),
            ]

        if n == 4:
            w = 0.5 - gap / 2
            h = 0.5 - gap / 2
            return [
                (0.0,         0.5 + gap / 2, w, h),
                (0.5 + gap / 2, 0.5 + gap / 2, w, h),
                (0.0,         0.0,          w, h),
                (0.5 + gap / 2, 0.0,          w, h),
            ]

        w = 1.0 / n - gap / 2
        return [(i * (1.0 / n) + gap / 2, 0.0, w, 1.0) for i in range(n)]

    def draw_cell(self, cell):
        """Рисует «прочие» клетки — стартовые, 2×2, L-образные."""
        cs = self.cell_size
        shape = cell["shape"]
        rotation = cell.get("rotation", 0)

        if shape == "L":
            blocks = self.get_l_blocks(cell["col"], cell["row"], rotation)
        else:
            w, h = shape
            blocks = [(cell["col"] + dc, cell["row"] + dr)
                      for dr in range(h) for dc in range(w)]

        parts = cell["parts"]
        pressed = cell["pressed"]
        is_start = cell.get("is_start", False)

        for i, (bc, br) in enumerate(blocks):
            x = self.offset_x + bc * cs
            y = self.offset_y + br * cs

            if is_start:
                with self.canvas_widget.canvas:
                    if cell["group"] == "green":
                        Color(0.8, 1, 0.8, 1)
                    else:
                        Color(1, 0.8, 0.8, 1)
                    Rectangle(pos=(x, y), size=(cs, cs))
                    Color(0.3, 0.3, 0.3, 1)
                    Line(rectangle=(x, y, cs, cs), width=1.5)

                lbl = Label(
                    text=cell["name"],
                    pos=(x, y),
                    size=(cs, cs),
                    font_size=sp(max(8, cs * 0.22)),
                    bold=True,
                    font_name=FONT,
                    color=(0, 0.5, 0, 1) if cell["group"] == "green" else (0.8, 0, 0, 1)
                )
                self.canvas_widget.add_widget(lbl)
                continue

            if len(parts) == 0:
                continue

            # Составные клетки (2×2, L): рисуем поклеточно по частям
            if len(parts) == 1:
                part_idx = 0
            else:
                part_idx = i % len(parts)

            if part_idx >= len(parts):
                continue

            with self.canvas_widget.canvas:
                if pressed[part_idx]:
                    Color(0.6, 0.85, 0.6, 1)
                else:
                    Color(0.9, 0.9, 0.9, 1)
                Rectangle(pos=(x, y), size=(cs, cs))

                Color(0.4, 0.4, 0.4, 1)
                Line(rectangle=(x, y, cs, cs), width=1)

            part = parts[part_idx]
            group = part.get("group")
            if group == "green":
                text_color = (0, 0.5, 0, 1)
            elif group == "red":
                text_color = (0.8, 0, 0, 1)
            else:
                text_color = (0, 0, 0, 1)

            lbl_value = Label(
                text=part["label"],
                pos=(x, y + cs * 0.35),
                size=(cs, cs * 0.4),
                font_size=sp(max(9, cs * 0.30)),
                bold=True,
                font_name=FONT,
                color=text_color
            )
            self.canvas_widget.add_widget(lbl_value)

            if part_idx == 0 and cell["name"]:
                lbl_name = Label(
                    text=cell["name"],
                    pos=(x, y),
                    size=(cs, cs * 0.35),
                    font_size=sp(max(7, cs * 0.13)),
                    font_name=FONT,
                    color=(0.4, 0.4, 0.4, 1)
                )
                self.canvas_widget.add_widget(lbl_name)

    def draw_stacked_cells(self, col, row, cells):
        """
        Рисует N клеток 1×1, занимающих одну ячейку (col, row).
        Ячейка делится по вертикали на N частей (или 2×2 при N=4).
        """
        cs = self.cell_size
        x0 = self.offset_x + col * cs
        y0 = self.offset_y + row * cs

        n = len(cells)
        rects = self.get_part_rects(n, gap=0.06)

        for idx, (rx, ry, rw, rh) in enumerate(rects):
            if idx >= n:
                break
            cell = cells[idx]

            px = x0 + rx * cs
            py = y0 + ry * cs
            pw = rw * cs
            ph = rh * cs

            parts = cell["parts"]
            pressed = cell["pressed"]

            if len(parts) == 0:
                continue

            if len(parts) == 1:
                # Одна часть — рисуем как один прямоугольник
                with self.canvas_widget.canvas:
                    if pressed[0]:
                        Color(0.6, 0.85, 0.6, 1)
                    else:
                        Color(0.9, 0.9, 0.9, 1)
                    Rectangle(pos=(px, py), size=(pw, ph))

                    Color(0.4, 0.4, 0.4, 1)
                    Line(rectangle=(px, py, pw, ph), width=1)

                part = parts[0]
                group = part.get("group")
                if group == "green":
                    text_color = (0, 0.5, 0, 1)
                elif group == "red":
                    text_color = (0.8, 0, 0, 1)
                else:
                    text_color = (0, 0, 0, 1)

                lbl_value = Label(
                    text=part["label"],
                    pos=(px, py + ph * 0.25),
                    size=(pw, ph * 0.5),
                    font_size=sp(max(7, min(pw, ph) * 0.42)),
                    bold=True,
                    font_name=FONT,
                    color=text_color
                )
                self.canvas_widget.add_widget(lbl_value)

                if cell["name"]:
                    lbl_name = Label(
                        text=cell["name"],
                        pos=(px, py),
                        size=(pw, ph * 0.22),
                        font_size=sp(max(6, min(pw, ph) * 0.20)),
                        font_name=FONT,
                        color=(0.5, 0.5, 0.5, 1)
                    )
                    self.canvas_widget.add_widget(lbl_name)
            else:
                # У клетки несколько частей — вложенные мини-прямоугольники
                sub_rects = self.get_part_rects(len(parts), gap=0.10)
                for pidx, (sx, sy, sw, sh) in enumerate(sub_rects):
                    spx = px + sx * pw
                    spy = py + sy * ph
                    spw = sw * pw
                    sph = sh * ph

                    with self.canvas_widget.canvas:
                        if pressed[pidx]:
                            Color(0.6, 0.85, 0.6, 1)
                        else:
                            Color(0.9, 0.9, 0.9, 1)
                        Rectangle(pos=(spx, spy), size=(spw, sph))

                        Color(0.4, 0.4, 0.4, 1)
                        Line(rectangle=(spx, spy, spw, sph), width=1)

                    part = parts[pidx]
                    group = part.get("group")
                    if group == "green":
                        text_color = (0, 0.5, 0, 1)
                    elif group == "red":
                        text_color = (0.8, 0, 0, 1)
                    else:
                        text_color = (0, 0, 0, 1)

                    lbl_value = Label(
                        text=part["label"],
                        pos=(spx, spy + sph * 0.2),
                        size=(spw, sph * 0.6),
                        font_size=sp(max(6, min(spw, sph) * 0.45)),
                        bold=True,
                        font_name=FONT,
                        color=text_color
                    )
                    self.canvas_widget.add_widget(lbl_value)

    def get_l_blocks(self, col, row, rotation):
        if rotation == 0:
            return [(col, row), (col + 1, row), (col + 1, row + 1)]
        elif rotation == 90:
            return [(col, row), (col, row + 1), (col + 1, row + 1)]
        elif rotation == 180:
            return [(col, row), (col + 1, row), (col, row + 1)]
        else:
            return [(col, row), (col + 1, row), (col + 1, row - 1)]

    def get_cells_at_grid(self, col, row):
        """Все клетки, занимающие ячейку (col, row), в порядке добавления."""
        result = []
        for cell in self.cells_on_field:
            shape = cell["shape"]
            rotation = cell.get("rotation", 0)
            if shape == "L":
                blocks = self.get_l_blocks(cell["col"], cell["row"], rotation)
            else:
                w, h = shape
                blocks = [(cell["col"] + dc, cell["row"] + dr)
                          for dr in range(h) for dc in range(w)]
            if (col, row) in blocks:
                result.append(cell)
        return result

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.ud['gf_start'] = touch.pos
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if 'gf_start' in touch.ud and self.collide_point(*touch.pos):
            dx = abs(touch.x - touch.ud['gf_start'][0])
            dy = abs(touch.y - touch.ud['gf_start'][1])
            if dx < dp(10) and dy < dp(10):
                if self.app.mode == "constructor":
                    if self.app.selected_tool:
                        self.place_cell(touch)
                    else:
                        self.remove_cell_at_touch(touch)
                else:
                    self.click_cell(touch)
                return True
        return super().on_touch_up(touch)

    def remove_cell_at_touch(self, touch):
        """Удаляет ВЕРХНЮЮ (последнюю добавленную) клетку на позиции."""
        cs = self.cell_size
        col = int((touch.x - self.offset_x) / cs)
        row = int((touch.y - self.offset_y) / cs)

        cells_here = self.get_cells_at_grid(col, row)
        if cells_here:
            top_cell = cells_here[-1]
            self.cells_on_field.remove(top_cell)
            self.app.update_tools_list()
            self.redraw()
            return True
        return False

    def place_cell(self, touch):
        if not self.app.selected_tool:
            return

        # ✅ Запрет дубликата по имени клетки
        existing_names = [c["name"] for c in self.cells_on_field]
        if self.app.selected_tool["name"] in existing_names:
            show_popup("Ограничение",
                       f"Клетка «{self.app.selected_tool['name']}» уже размещена!")
            return

        cs = self.cell_size
        col = int((touch.x - self.offset_x) / cs)
        row = int((touch.y - self.offset_y) / cs)

        cell = self.app.selected_tool
        shape = cell["shape"]
        if shape == "L":
            w, h = 2, 2
        else:
            w, h = shape

        col = max(0, min(col, self.grid_cols - w))
        row = max(0, min(row, self.grid_rows - h))

        new_cell = {
            "name": cell["name"],
            "shape": cell["shape"],
            "parts": [dict(p) for p in cell["parts"]],
            "group": cell.get("group"),
            "is_start": cell.get("is_start", False),
            "col": col,
            "row": row,
            "rotation": self.app.rotation,
            "pressed": [False] * len(cell["parts"]),
            "press_count": [0] * len(cell["parts"])
        }
        self.cells_on_field.append(new_cell)
        self.app.update_tools_list()
        self.redraw()

    def click_cell(self, touch):
        cs = self.cell_size
        col = int((touch.x - self.offset_x) / cs)
        row = int((touch.y - self.offset_y) / cs)

        # ✅ Если на позиции есть простые 1×1 — берём нужную из стека
        simple_cells = []
        for c in self.cells_on_field:
            if c["shape"] == (1, 1) and not c.get("is_start"):
                if c["col"] == col and c["row"] == row:
                    simple_cells.append(c)

        if simple_cells:
            cell = self._pick_stacked_cell(touch, col, row, simple_cells)
            if cell is not None:
                self._toggle_part(cell, touch, col, row, cs)
            return

        # Иначе — ищем среди «прочих» клеток
        for cell in self.cells_on_field:
            if cell.get("is_start"):
                continue
            shape = cell["shape"]
            if shape == (1, 1):
                continue
            rotation = cell.get("rotation", 0)
            if shape == "L":
                blocks = self.get_l_blocks(cell["col"], cell["row"], rotation)
            else:
                w, h = shape
                blocks = [(cell["col"] + dc, cell["row"] + dr)
                          for dr in range(h) for dc in range(w)]
            if (col, row) in blocks:
                self._toggle_part(cell, touch, col, row, cs)
                return

    def _pick_stacked_cell(self, touch, col, row, cells):
        """Возвращает клетку из стека, на которую попал тап."""
        cs = self.cell_size
        x0 = self.offset_x + col * cs
        y0 = self.offset_y + row * cs

        rects = self.get_part_rects(len(cells), gap=0.06)
        tx = (touch.x - x0) / cs
        ty = (touch.y - y0) / cs

        for idx, (rx, ry, rw, rh) in enumerate(rects):
            if idx >= len(cells):
                break
            if rx <= tx <= rx + rw and ry <= ty <= ry + rh:
                return cells[idx]
        return None

    def _toggle_part(self, cell, touch, col, row, cs):
        """Переключает нажатую часть клетки."""
        shape = cell["shape"]
        parts = cell["parts"]
        if len(parts) == 0:
            return

        if shape != (1, 1):
            rotation = cell.get("rotation", 0)
            if shape == "L":
                blocks = self.get_l_blocks(cell["col"], cell["row"], rotation)
            else:
                w, h = shape
                blocks = [(cell["col"] + dc, cell["row"] + dr)
                          for dr in range(h) for dc in range(w)]
            block_index = blocks.index((col, row))
            part_idx = block_index % len(parts) if len(parts) > 1 else 0
        else:
            if len(parts) == 1:
                part_idx = 0
            elif len(parts) == 2:
                x_center = self.offset_x + cell["col"] * cs + cs / 2
                part_idx = 0 if touch.x < x_center else 1
            elif len(parts) == 3:
                third = cs / 3
                x1 = self.offset_x + cell["col"] * cs
                if touch.x < x1 + third:
                    part_idx = 0
                elif touch.x < x1 + 2 * third:
                    part_idx = 1
                else:
                    part_idx = 2
            elif len(parts) == 4:
                x1 = self.offset_x + cell["col"] * cs
                y1 = self.offset_y + cell["row"] * cs
                x_mid = x1 + cs / 2
                y_mid = y1 + cs / 2
                if touch.x < x_mid and touch.y < y_mid:
                    part_idx = 2
                elif touch.x >= x_mid and touch.y < y_mid:
                    part_idx = 3
                elif touch.x < x_mid and touch.y >= y_mid:
                    part_idx = 0
                else:
                    part_idx = 1
            else:
                part_idx = 0

        if part_idx >= len(parts):
            return

        value = parts[part_idx]["value"]
        if cell["pressed"][part_idx]:
            cell["pressed"][part_idx] = False
            cell["press_count"][part_idx] -= 1
            self.app.score_received -= value
        else:
            cell["pressed"][part_idx] = True
            cell["press_count"][part_idx] += 1
            self.app.score_received += value

        self.app.update_score_display()
        self.redraw()


# ====================== ЗАДАНИЯ ======================

class TasksPage(ScrollView):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

        self.layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=None, padding=dp(10))
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        self.build_tasks()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def build_tasks(self):
        self.layout.clear_widgets()

        self.layout.add_widget(Label(
            text="ЗАДАНИЯ",
            size_hint_y=None,
            height=dp(40),
            bold=True,
            font_size=sp(18),
            font_name=FONT,
            color=(0, 0, 0, 1)
        ))

        for task in TASKS:
            self.layout.add_widget(self.create_task_widget(task))

        self.layout.add_widget(Label(
            text="— ШТРАФЫ —",
            size_hint_y=None,
            height=dp(40),
            bold=True,
            font_size=sp(18),
            font_name=FONT,
            color=(0.8, 0, 0, 1)
        ))

        for penalty in PENALTIES:
            self.layout.add_widget(self.create_task_widget(penalty, is_penalty=True))

    def create_task_widget(self, task, is_penalty=False):
        limit = task.get("limit", None)

        box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(90), padding=dp(10))

        name_label = Label(
            text=task["name"],
            size_hint_y=None,
            height=dp(30),
            bold=True,
            font_size=sp(13),
            font_name=FONT,
            color=(0.8, 0, 0, 1) if is_penalty else (0, 0, 0, 1),
            halign='left',
            valign='middle'
        )
        name_label.bind(size=name_label.setter('text_size'))
        box.add_widget(name_label)

        options_box = BoxLayout(orientation='horizontal', size_hint_y=None,
                                height=dp(45), spacing=dp(10))

        if limit is not None and limit > 1:
            for i, opt in enumerate(task["options"]):
                value = opt["value"]
                label_text = opt["label"]

                variant_box = BoxLayout(orientation='horizontal',
                                        size_hint_x=None, width=dp(160), spacing=dp(5))

                btn_minus = Button(text="−", size_hint_x=None, width=dp(40),
                                   font_size=sp(18), font_name=FONT)
                btn_minus.task = task
                btn_minus.opt_index = i
                btn_minus.delta = -1
                btn_minus.value = value
                btn_minus.is_penalty = is_penalty
                btn_minus.bind(on_press=self.on_counter_press)

                counter_label = Label(
                    text=f"{label_text}\n0/{limit if limit is not None else '∞'}",
                    size_hint_x=None,
                    width=dp(70),
                    font_size=sp(11),
                    font_name=FONT,
                    color=(0.8, 0, 0, 1) if is_penalty else (0, 0, 0, 1)
                )
                counter_label.task = task
                counter_label.opt_index = i
                counter_label.count = 0
                counter_label.limit = limit
                counter_label.value = value

                btn_plus = Button(text="+", size_hint_x=None, width=dp(40),
                                  font_size=sp(18), font_name=FONT)
                btn_plus.task = task
                btn_plus.opt_index = i
                btn_plus.delta = 1
                btn_plus.value = value
                btn_plus.is_penalty = is_penalty
                btn_plus.bind(on_press=self.on_counter_press)

                variant_box.add_widget(btn_minus)
                variant_box.add_widget(counter_label)
                variant_box.add_widget(btn_plus)

                options_box.add_widget(variant_box)
        else:
            for i, opt in enumerate(task["options"]):
                value = opt["value"]
                label_text = opt["label"]

                if label_text in ["✓", "✔", "☑"]:
                    btn_text = f"OK ({value:+d})"
                else:
                    btn_text = f"{label_text} ({value:+d})"

                btn = ToggleButton(
                    text=btn_text,
                    size_hint_x=None,
                    width=dp(110),
                    font_size=sp(13),
                    font_name=FONT
                )
                btn.task = task
                btn.opt_index = i
                btn.is_penalty = is_penalty
                btn.bind(on_press=self.on_option_press)
                options_box.add_widget(btn)

        box.add_widget(options_box)
        return box

    def on_counter_press(self, btn):
        task = btn.task
        opt_index = btn.opt_index
        value = btn.value
        limit = task.get("limit", None)

        parent_box = btn.parent
        counter_label = None
        for child in parent_box.children:
            if isinstance(child, Label) and hasattr(child, 'count'):
                counter_label = child
                break

        if counter_label is None:
            return

        new_count = counter_label.count + btn.delta

        if limit is not None:
            if new_count < 0:
                new_count = 0
            if new_count > limit:
                return
        else:
            if new_count < 0:
                new_count = 0

        old_count = counter_label.count
        counter_label.count = new_count

        label_text = task["options"][opt_index]["label"]
        limit_text = f"{limit}" if limit is not None else "∞"
        counter_label.text = f"{label_text}\n{new_count}/{limit_text}"

        delta_count = new_count - old_count
        self.app.score_received += value * delta_count

        self.app.update_score_display()

    def on_option_press(self, btn):
        task = btn.task
        opt_index = btn.opt_index
        opt = task["options"][opt_index]
        value = opt["value"]

        if btn.state == 'down':
            if task["type"] == "choice":
                for child in btn.parent.children:
                    if isinstance(child, ToggleButton) and child is not btn \
                            and child.state == 'down':
                        child.state = 'normal'
                        self.app.score_received -= task["options"][child.opt_index]["value"]
            self.app.score_received += value
        else:
            self.app.score_received -= value

        self.app.update_score_display()


# ====================== ГЛАВНЫЙ ЭКРАН ======================

class MainScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app

        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None,
                            height=dp(50), padding=dp(5), spacing=dp(5))

        self.btn_page1 = Button(text="Поле", font_name=FONT,
                                on_press=lambda x: self.switch_page(1))
        self.btn_page2 = Button(text="Задания", font_name=FONT,
                                on_press=lambda x: self.switch_page(2))
        self.btn_constructor = Button(text="Конструктор", font_name=FONT,
                                      on_press=self.toggle_constructor)
        self.score_label = Label(text="Баллы: 0", bold=True,
                                 size_hint_x=0.3, font_name=FONT)

        top_bar.add_widget(self.btn_page1)
        top_bar.add_widget(self.btn_page2)
        top_bar.add_widget(self.btn_constructor)
        top_bar.add_widget(self.score_label)
        self.add_widget(top_bar)

        zoom_bar = BoxLayout(orientation='horizontal', size_hint_y=None,
                             height=dp(44), padding=dp(5), spacing=dp(5))

        self.zoom_label = Label(text="100%", size_hint_x=None, width=dp(70),
                                bold=True, font_name=FONT, font_size=sp(14),
                                color=(0, 0, 0, 1))

        btn_zoom_out = Button(text="−", font_name=FONT, font_size=sp(22),
                              on_press=lambda x: self.change_zoom(-0.1))
        btn_zoom_in = Button(text="+", font_name=FONT, font_size=sp(22),
                             on_press=lambda x: self.change_zoom(0.1))
        btn_zoom_reset = Button(text="Сброс", font_name=FONT,
                                on_press=lambda x: self.reset_zoom())

        zoom_bar.add_widget(Label(text="Зум:", font_name=FONT,
                                  size_hint_x=None, width=dp(50),
                                  color=(0, 0, 0, 1)))
        zoom_bar.add_widget(btn_zoom_out)
        zoom_bar.add_widget(self.zoom_label)
        zoom_bar.add_widget(btn_zoom_in)
        zoom_bar.add_widget(btn_zoom_reset)

        self.add_widget(zoom_bar)

        self.pages_container = BoxLayout(orientation='vertical')

        self.field_page = BoxLayout(orientation='vertical')

        self.field_scroll = ScrollView(
            do_scroll_x=True,
            do_scroll_y=True,
            bar_width=dp(6),
            scroll_type=['bars'],
            scroll_distance=dp(20),
        )

        self.game_field = GameField(app)
        self.field_scroll.add_widget(self.game_field)

        self.field_page.add_widget(self.field_scroll)

        self.constructor_panel = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(300)
        )

        with self.constructor_panel.canvas.before:
            Color(0, 0, 0, 1)
            self.constructor_rect = Rectangle(pos=self.constructor_panel.pos,
                                              size=self.constructor_panel.size)
        self.constructor_panel.bind(pos=self.update_constructor_rect,
                                    size=self.update_constructor_rect)

        lbl = Label(text="Конструктор:", size_hint_y=None, height=dp(30),
                    bold=True, color=(1, 1, 1, 1), font_name=FONT)
        self.constructor_panel.add_widget(lbl)

        size_row = BoxLayout(orientation='horizontal', size_hint_y=None,
                             height=dp(40), spacing=dp(5), padding=dp(5))

        self.lbl_cols = Label(
            text=f"Столбцы: {self.game_field.grid_cols}",
            size_hint_x=None, width=dp(110),
            color=(1, 1, 1, 1), bold=True, font_size=sp(14), font_name=FONT
        )
        btn_col_minus = Button(text="−", size_hint_x=None, width=dp(40),
                               font_name=FONT,
                               on_press=lambda x: self.change_grid("cols", -1))
        btn_col_plus = Button(text="+", size_hint_x=None, width=dp(40),
                              font_name=FONT,
                              on_press=lambda x: self.change_grid("cols", 1))

        self.lbl_rows = Label(
            text=f"Строки: {self.game_field.grid_rows}",
            size_hint_x=None, width=dp(110),
            color=(1, 1, 1, 1), bold=True, font_size=sp(14), font_name=FONT
        )
        btn_row_minus = Button(text="−", size_hint_x=None, width=dp(40),
                               font_name=FONT,
                               on_press=lambda x: self.change_grid("rows", -1))
        btn_row_plus = Button(text="+", size_hint_x=None, width=dp(40),
                              font_name=FONT,
                              on_press=lambda x: self.change_grid("rows", 1))

        size_row.add_widget(self.lbl_cols)
        size_row.add_widget(btn_col_minus)
        size_row.add_widget(btn_col_plus)
        size_row.add_widget(self.lbl_rows)
        size_row.add_widget(btn_row_minus)
        size_row.add_widget(btn_row_plus)

        self.constructor_panel.add_widget(size_row)

        self.tools_list = ScrollView()
        self.tools_grid = GridLayout(cols=2, spacing=dp(2), size_hint_y=None, padding=dp(5))
        self.tools_grid.bind(minimum_height=self.tools_grid.setter('height'))
        self.tools_list.add_widget(self.tools_grid)
        self.constructor_panel.add_widget(self.tools_list)

        btn_row = BoxLayout(orientation='horizontal', size_hint_y=None,
                            height=dp(40), spacing=dp(2))
        btn_rotate = Button(text="Повернуть", font_name=FONT, on_press=self.rotate_tool)
        btn_save = Button(text="Сохранить", font_name=FONT, on_press=self.save_scheme)
        btn_load = Button(text="Загрузить", font_name=FONT, on_press=self.load_scheme)
        btn_clear = Button(text="Очистить", font_name=FONT, on_press=self.clear_field)
        btn_row.add_widget(btn_rotate)
        btn_row.add_widget(btn_save)
        btn_row.add_widget(btn_load)
        btn_row.add_widget(btn_clear)
        self.constructor_panel.add_widget(btn_row)

        self.field_page.add_widget(self.constructor_panel)
        self.constructor_panel.height = 0

        self.tasks_page = TasksPage(app)

        self.pages_container.add_widget(self.field_page)
        self.add_widget(self.pages_container)

        self.switch_page(1)
        self.build_tools_list()

    def update_constructor_rect(self, *args):
        self.constructor_rect.pos = self.constructor_panel.pos
        self.constructor_rect.size = self.constructor_panel.size

    def toggle_constructor(self, instance=None):
        if self.app.mode == "game":
            self.app.mode = "constructor"
            self.constructor_panel.height = dp(300)
            self.btn_constructor.text = "Выйти"

            self.game_field.padding_top = 0
            self.game_field.padding_bottom = 0
        else:
            self.app.mode = "game"
            self.constructor_panel.height = 0
            self.btn_constructor.text = "Конструктор"
            self.app.selected_tool = None

            self.game_field.padding_top = 1
            self.game_field.padding_bottom = 1

        self.game_field.update_cell_size()

        if self.app.mode == "constructor":
            Clock.schedule_once(self._scroll_to_bottom, 0.05)

        self.game_field.redraw()
        self._update_tools_highlight()

    def _scroll_to_bottom(self, *args):
        self.field_scroll.scroll_y = 0

    def _center_scroll(self, *args):
        self.field_scroll.scroll_x = 0.5
        self.field_scroll.scroll_y = 0.0 if self.app.mode == "constructor" else 0.5

    def change_zoom(self, delta):
        new_zoom = self.game_field.zoom_level + delta
        new_zoom = max(0.1, min(3.0, new_zoom))
        self.game_field.zoom_level = round(new_zoom, 2)
        self.game_field.update_cell_size()
        self._update_zoom_label()
        Clock.schedule_once(lambda dt: self._center_scroll(), 0.05)

    def reset_zoom(self, *args):
        self.game_field.zoom_level = 1.0
        self.game_field.update_cell_size()
        self._update_zoom_label()
        Clock.schedule_once(lambda dt: self._center_scroll(), 0.05)

    def _update_zoom_label(self):
        if hasattr(self, 'zoom_label'):
            self.zoom_label.text = f"{int(round(self.game_field.zoom_level * 100))}%"

    def change_grid(self, dimension, delta):
        if dimension == "cols":
            new_val = self.game_field.grid_cols + delta
            if 3 <= new_val <= 50:
                self.game_field.grid_cols = new_val
                self.lbl_cols.text = f"Столбцы: {self.game_field.grid_cols}"
        else:
            new_val = self.game_field.grid_rows + delta
            if 3 <= new_val <= 50:
                self.game_field.grid_rows = new_val
                self.lbl_rows.text = f"Строки: {self.game_field.grid_rows}"

        self.game_field.update_cell_size()
        self.game_field.redraw()

    def switch_page(self, page):
        if page == 1:
            self.pages_container.clear_widgets()
            self.pages_container.add_widget(self.field_page)
        else:
            self.pages_container.clear_widgets()
            self.pages_container.add_widget(self.tasks_page)

    def rotate_tool(self, instance=None):
        if self.app.selected_tool and self.app.selected_tool["shape"] == "L":
            self.app.rotation = (self.app.rotation + 90) % 360

    def build_tools_list(self):
        self.tools_grid.clear_widgets()
        existing_names = [c["name"] for c in self.game_field.cells_on_field]
        for cell_def in CELL_DEFINITIONS:
            btn = Button(text=cell_def["name"], size_hint_y=None,
                         height=dp(44), font_name=FONT)
            if cell_def["name"] in existing_names:
                btn.background_color = (0.7, 0.7, 0.7, 1)
                btn.color = (0.5, 0.5, 0.5, 1)
            else:
                btn.background_color = (1, 1, 1, 1)
                btn.color = (0, 0, 0, 1)
            btn.cell_def = cell_def
            btn.bind(on_press=self.on_tool_select)
            self.tools_grid.add_widget(btn)

        self._update_tools_highlight()

    def _update_tools_highlight(self):
        selected_name = self.app.selected_tool["name"] if self.app.selected_tool else None
        existing_names = [c["name"] for c in self.game_field.cells_on_field]

        for btn in self.tools_grid.children:
            if not hasattr(btn, 'cell_def'):
                continue
            name = btn.cell_def["name"]
            if name == selected_name:
                btn.background_color = (0.4, 0.7, 1, 1)
                btn.color = (1, 1, 1, 1)
            elif name in existing_names:
                btn.background_color = (0.7, 0.7, 0.7, 1)
                btn.color = (0.5, 0.5, 0.5, 1)
            else:
                btn.background_color = (1, 1, 1, 1)
                btn.color = (0, 0, 0, 1)

    def on_tool_select(self, btn):
        cell_def = btn.cell_def

        if self.app.selected_tool and self.app.selected_tool["name"] == cell_def["name"]:
            self.app.selected_tool = None
            self.app.rotation = 0
            self._update_tools_highlight()
            return

        existing_names = [c["name"] for c in self.game_field.cells_on_field]
        if cell_def["name"] in existing_names:
            show_popup("Занято", f"Клетка «{cell_def['name']}» уже на поле!")
            return

        self.app.selected_tool = cell_def
        self.app.rotation = 0
        self._update_tools_highlight()

    def save_scheme(self, instance=None):
        """Сохраняет ВСЕ клетки (включая стеки на одной позиции)."""
        data = []
        for cell in self.game_field.cells_on_field:
            data.append({
                "name": cell["name"],
                "col": cell["col"],
                "row": cell["row"],
                "rotation": cell.get("rotation", 0),
                "pressed": list(cell.get("pressed", [])),
                "press_count": list(cell.get("press_count", []))
            })
        try:
            with open(get_scheme_path(), "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            show_popup("Сохранено", "Схема сохранена!")
        except Exception as e:
            show_popup("Ошибка", f"Не удалось сохранить:\n{e}")

    def load_scheme(self, instance=None):
        path = get_scheme_path()
        if not os.path.exists(path):
            show_popup("Ошибка", "Файл схемы не найден")
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            show_popup("Ошибка", f"Не удалось прочитать:\n{e}")
            return

        self.game_field.cells_on_field = []
        for item in data:
            template = next((c for c in CELL_DEFINITIONS if c["name"] == item["name"]), None)
            if template:
                parts_len = len(template["parts"])
                pressed = item.get("pressed", [False] * parts_len)
                # На случай несовпадения длины — выравниваем
                if len(pressed) != parts_len:
                    pressed = [False] * parts_len
                self.game_field.cells_on_field.append({
                    "name": template["name"],
                    "shape": template["shape"],
                    "parts": [dict(p) for p in template["parts"]],
                    "group": template.get("group"),
                    "is_start": template.get("is_start", False),
                    "col": item["col"],
                    "row": item["row"],
                    "rotation": item.get("rotation", 0),
                    "pressed": list(pressed),
                    "press_count": [0] * parts_len
                })
        self.app.selected_tool = None
        self.app.score_received = 0
        self.app.update_score_display()
        self.build_tools_list()
        self.game_field.redraw()

    def clear_field(self, instance=None):
        self.game_field.cells_on_field = []
        self.app.score_received = 0
        self.app.selected_tool = None
        self.app.update_score_display()
        self.build_tools_list()
        self.game_field.redraw()


# ====================== ПРИЛОЖЕНИЕ ======================

class GameApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mode = "game"
        self.selected_tool = None
        self.rotation = 0
        self.score_received = 0

    def build(self):
        self.title = "Полигон"
        return MainScreen(self)

    def update_score_display(self):
        if hasattr(self, 'root') and hasattr(self.root, 'score_label'):
            self.root.score_label.text = f"Баллы: {self.score_received}"

    def update_tools_list(self):
        if hasattr(self, 'root') and hasattr(self.root, 'tools_grid'):
            self.root.build_tools_list()


if __name__ == "__main__":
    # Window.size нужен только при запуске на ПК, на Android он не работает
    try:
        from kivy.utils import platform
        if platform in ('win', 'linux', 'macosx'):
            Window.size = (400, 800)
    except Exception:
        pass
    GameApp().run()
