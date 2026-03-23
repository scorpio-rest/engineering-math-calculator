from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QGroupBox, QTextEdit, QCheckBox
)
from PyQt6.QtCore import Qt
from core.ode_ops import solve_ode
from utils.latex_render import render_latex_label, sympy_to_latex


class ODETab(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Input area
        input_group = QGroupBox("ODE 輸入")
        input_layout = QVBoxLayout(input_group)

        input_layout.addWidget(QLabel(
            "輸入 ODE 方程式 (設 = 0 的形式)\n"
            "例: y'' + 3*y' + 2*y - sin(x)\n"
            "    表示 y'' + 3y' + 2y - sin(x) = 0\n"
            "使用 ' 表示微分: y' = dy/dx, y'' = d²y/dx²"
        ))

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("方程式:"))
        self.ode_input = QLineEdit()
        self.ode_input.setPlaceholderText("y'' + 3*y' + 2*y")
        row1.addWidget(self.ode_input, 1)
        row1.addWidget(QLabel("= 0"))
        input_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("函數名:"))
        self.func_input = QLineEdit("y")
        self.func_input.setMaximumWidth(60)
        row2.addWidget(self.func_input)
        row2.addWidget(QLabel("自變數:"))
        self.var_input = QLineEdit("x")
        self.var_input.setMaximumWidth(60)
        row2.addWidget(self.var_input)
        row2.addStretch()
        input_layout.addLayout(row2)

        # Initial conditions
        self.ic_check = QCheckBox("加入初始條件")
        self.ic_check.toggled.connect(self._toggle_ic)
        input_layout.addWidget(self.ic_check)

        self.ic_widget = QWidget()
        ic_layout = QVBoxLayout(self.ic_widget)
        ic_layout.setContentsMargins(0, 0, 0, 0)
        ic_layout.addWidget(QLabel("格式: 每行一個條件，如 y(0)=1 或 y'(0)=0"))
        self.ic_input = QTextEdit()
        self.ic_input.setPlaceholderText("y(0)=1\ny'(0)=0")
        self.ic_input.setMaximumHeight(80)
        ic_layout.addWidget(self.ic_input)
        self.ic_widget.setVisible(False)
        input_layout.addWidget(self.ic_widget)

        layout.addWidget(input_group)

        # Calculate button
        self.calc_btn = QPushButton("求解")
        self.calc_btn.setMinimumHeight(40)
        self.calc_btn.clicked.connect(self._calculate)
        layout.addWidget(self.calc_btn)

        # Result area
        result_group = QGroupBox("解")
        result_layout_outer = QVBoxLayout(result_group)
        self.result_scroll = QScrollArea()
        self.result_scroll.setWidgetResizable(True)
        self.result_scroll.setMinimumHeight(200)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_scroll.setWidget(self.result_widget)
        result_layout_outer.addWidget(self.result_scroll)
        layout.addWidget(result_group, 1)

    def _toggle_ic(self, checked):
        self.ic_widget.setVisible(checked)

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
        ode_str = self.ode_input.text().strip()
        func_str = self.func_input.text().strip() or 'y'
        var_str = self.var_input.text().strip() or 'x'

        if not ode_str:
            self._show_error("請輸入 ODE 方程式")
            return

        # Parse initial conditions
        ics = None
        if self.ic_check.isChecked():
            ic_text = self.ic_input.toPlainText().strip()
            if ic_text:
                ics = {}
                for line in ic_text.split('\n'):
                    line = line.strip()
                    if '=' in line:
                        key, val = line.split('=', 1)
                        ics[key.strip()] = val.strip()

        try:
            solution = solve_ode(ode_str, func_str, var_str, ics)
            if isinstance(solution, list):
                for i, sol in enumerate(solution):
                    self._show_result(sympy_to_latex(sol), f"解 {i+1}:")
            else:
                self._show_result(sympy_to_latex(solution), "解:")
        except Exception as e:
            self._show_error(str(e))

        self.result_layout.addStretch()
