from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QScrollArea, QGroupBox, QSpinBox
)
from PyQt6.QtCore import Qt
from core.calculus_ops import (
    differentiate, integrate_indefinite, integrate_definite,
    limit, taylor_expand
)
from utils.latex_render import render_latex_label, sympy_to_latex


class CalculusTab(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Operation selector
        op_group = QGroupBox("操作選擇")
        op_layout = QHBoxLayout(op_group)
        self.op_combo = QComboBox()
        self.op_combo.addItems([
            "微分 (Differentiation)",
            "不定積分 (Indefinite Integral)",
            "定積分 (Definite Integral)",
            "極限 (Limit)",
            "Taylor 展開 (Taylor Expansion)",
        ])
        self.op_combo.currentIndexChanged.connect(self._on_op_changed)
        op_layout.addWidget(QLabel("運算:"))
        op_layout.addWidget(self.op_combo, 1)
        layout.addWidget(op_group)

        # Input area
        input_group = QGroupBox("輸入")
        input_layout = QVBoxLayout(input_group)

        # Expression
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("函數 f(x):"))
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText("例: sin(x)*exp(x) 或 x**3 + 2*x")
        row1.addWidget(self.expr_input, 1)
        input_layout.addLayout(row1)

        # Variable
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("變數:"))
        self.var_input = QLineEdit("x")
        self.var_input.setMaximumWidth(60)
        row2.addWidget(self.var_input)

        # Order (for differentiation)
        self.order_label = QLabel("階數:")
        row2.addWidget(self.order_label)
        self.order_spin = QSpinBox()
        self.order_spin.setRange(1, 10)
        self.order_spin.setValue(1)
        row2.addWidget(self.order_spin)

        # Bounds (for definite integral)
        self.lower_label = QLabel("下界:")
        row2.addWidget(self.lower_label)
        self.lower_input = QLineEdit("0")
        self.lower_input.setMaximumWidth(80)
        row2.addWidget(self.lower_input)
        self.upper_label = QLabel("上界:")
        row2.addWidget(self.upper_label)
        self.upper_input = QLineEdit("1")
        self.upper_input.setMaximumWidth(80)
        row2.addWidget(self.upper_input)

        # Limit point
        self.point_label = QLabel("趨近點:")
        row2.addWidget(self.point_label)
        self.point_input = QLineEdit("0")
        self.point_input.setMaximumWidth(80)
        row2.addWidget(self.point_input)

        # Direction for limit
        self.dir_label = QLabel("方向:")
        row2.addWidget(self.dir_label)
        self.dir_combo = QComboBox()
        self.dir_combo.addItems(["雙側", "右側 (+)", "左側 (-)"])
        self.dir_combo.setMaximumWidth(100)
        row2.addWidget(self.dir_combo)

        row2.addStretch()
        input_layout.addLayout(row2)
        layout.addWidget(input_group)

        self._on_op_changed(0)

        # Calculate button
        self.calc_btn = QPushButton("計算")
        self.calc_btn.setMinimumHeight(40)
        self.calc_btn.clicked.connect(self._calculate)
        layout.addWidget(self.calc_btn)

        # Result area
        result_group = QGroupBox("結果")
        result_layout_outer = QVBoxLayout(result_group)
        self.result_scroll = QScrollArea()
        self.result_scroll.setWidgetResizable(True)
        self.result_scroll.setMinimumHeight(200)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_scroll.setWidget(self.result_widget)
        result_layout_outer.addWidget(self.result_scroll)
        layout.addWidget(result_group, 1)

    def _on_op_changed(self, index):
        # Show/hide fields based on operation
        self.order_label.setVisible(index in (0, 4))  # diff, taylor
        self.order_spin.setVisible(index in (0, 4))
        self.lower_label.setVisible(index == 2)
        self.lower_input.setVisible(index == 2)
        self.upper_label.setVisible(index == 2)
        self.upper_input.setVisible(index == 2)
        self.point_label.setVisible(index in (3, 4))
        self.point_input.setVisible(index in (3, 4))
        self.dir_label.setVisible(index == 3)
        self.dir_combo.setVisible(index == 3)

        if index == 4:
            self.order_label.setText("展開階數:")
            self.order_spin.setRange(1, 20)
            self.order_spin.setValue(5)
        else:
            self.order_label.setText("階數:")
            self.order_spin.setRange(1, 10)
            self.order_spin.setValue(1)

    def _clear_results(self):
        while self.result_layout.count():
            child = self.result_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _show_result(self, latex_str, label_text=""):
        if label_text:
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color: #a6adc8; font-weight: bold;")
            self.result_layout.addWidget(lbl)
        widget = render_latex_label(latex_str)
        self.result_layout.addWidget(widget)

    def _show_error(self, msg):
        lbl = QLabel(f"錯誤: {msg}")
        lbl.setStyleSheet("color: #f38ba8;")
        lbl.setWordWrap(True)
        self.result_layout.addWidget(lbl)

    def _calculate(self):
        self._clear_results()
        op = self.op_combo.currentIndex()
        expr_str = self.expr_input.text().strip()
        var_str = self.var_input.text().strip() or 'x'

        if not expr_str:
            self._show_error("請輸入函數表達式")
            return

        try:
            if op == 0:  # Differentiation
                order = self.order_spin.value()
                result = differentiate(expr_str, var_str, order)
                self._show_result(
                    f"\\frac{{d^{{{order}}}}}{{d{var_str}^{{{order}}}}}\\left({expr_str}\\right) = {sympy_to_latex(result)}",
                    f"第 {order} 階微分:"
                )
            elif op == 1:  # Indefinite integral
                result = integrate_indefinite(expr_str, var_str)
                self._show_result(
                    f"\\int {expr_str} \\, d{var_str} = {sympy_to_latex(result)} + C",
                    "不定積分:"
                )
            elif op == 2:  # Definite integral
                lower = self.lower_input.text().strip()
                upper = self.upper_input.text().strip()
                result = integrate_definite(expr_str, var_str, lower, upper)
                self._show_result(
                    f"\\int_{{{lower}}}^{{{upper}}} {expr_str} \\, d{var_str} = {sympy_to_latex(result)}",
                    "定積分:"
                )
            elif op == 3:  # Limit
                point = self.point_input.text().strip()
                dir_map = {0: '', 1: '+', 2: '-'}
                direction = dir_map[self.dir_combo.currentIndex()]
                result = limit(expr_str, var_str, point, direction)
                dir_text = f"^{direction}" if direction else ""
                self._show_result(
                    f"\\lim_{{{var_str} \\to {point}{dir_text}}} {expr_str} = {sympy_to_latex(result)}",
                    "極限:"
                )
            elif op == 4:  # Taylor expansion
                point = self.point_input.text().strip()
                order = self.order_spin.value()
                result = taylor_expand(expr_str, var_str, point, order)
                self._show_result(
                    sympy_to_latex(result),
                    f"在 {var_str}={point} 的 Taylor 展開 (至 {order} 階):"
                )

        except Exception as e:
            self._show_error(str(e))

        self.result_layout.addStretch()
