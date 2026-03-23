from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QComboBox, QScrollArea, QGroupBox
)
from PyQt6.QtCore import Qt
from core.laplace_ops import laplace_transform, inverse_laplace_transform
from utils.latex_render import render_latex_label, sympy_to_latex


class LaplaceTab(QWidget):
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
            "正轉換 f(t) → F(s)",
            "逆轉換 F(s) → f(t)",
        ])
        self.op_combo.currentIndexChanged.connect(self._on_op_changed)
        op_layout.addWidget(QLabel("轉換類型:"))
        op_layout.addWidget(self.op_combo, 1)
        layout.addWidget(op_group)

        # Input area
        input_group = QGroupBox("輸入")
        input_layout = QVBoxLayout(input_group)

        self.input_label = QLabel("f(t) =")
        row = QHBoxLayout()
        row.addWidget(self.input_label)
        self.expr_input = QLineEdit()
        self.expr_input.setPlaceholderText("例: exp(-t)*sin(t) 或 t**2")
        row.addWidget(self.expr_input, 1)
        input_layout.addLayout(row)

        input_layout.addWidget(QLabel(
            "提示: 使用 t 和 s 作為變數\n"
            "常用函數: sin(t), cos(t), exp(t), t**n, Heaviside(t), DiracDelta(t)"
        ))
        layout.addWidget(input_group)

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
        if index == 0:
            self.input_label.setText("f(t) =")
            self.expr_input.setPlaceholderText("例: exp(-t)*sin(t) 或 t**2")
        else:
            self.input_label.setText("F(s) =")
            self.expr_input.setPlaceholderText("例: 1/(s**2 + 1) 或 s/(s**2 + 4)")

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

        if not expr_str:
            self._show_error("請輸入表達式")
            return

        try:
            if op == 0:  # Forward Laplace
                result = laplace_transform(expr_str)
                self._show_result(
                    f"\\mathcal{{L}}\\{{{expr_str}\\}} = {sympy_to_latex(result)}",
                    "Laplace 正轉換:"
                )
            else:  # Inverse Laplace
                result = inverse_laplace_transform(expr_str)
                self._show_result(
                    f"\\mathcal{{L}}^{{-1}}\\{{{expr_str}\\}} = {sympy_to_latex(result)}",
                    "Laplace 逆轉換:"
                )
        except Exception as e:
            self._show_error(str(e))

        self.result_layout.addStretch()
