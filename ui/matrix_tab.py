from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QComboBox, QScrollArea, QFrame, QGroupBox
)
from PyQt6.QtCore import Qt
from core.matrix_ops import (
    parse_matrix, determinant, inverse, transpose,
    eigenvalues, eigenvectors, matrix_multiply, matrix_add,
    matrix_subtract, rank, rref
)
from utils.latex_render import render_latex_label, sympy_to_latex


class MatrixTab(QWidget):
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
            "行列式 (Determinant)",
            "反矩陣 (Inverse)",
            "轉置 (Transpose)",
            "特徵值 (Eigenvalues)",
            "特徵向量 (Eigenvectors)",
            "秩 (Rank)",
            "RREF (列簡化梯形式)",
            "矩陣加法 (A + B)",
            "矩陣減法 (A - B)",
            "矩陣乘法 (A × B)",
        ])
        self.op_combo.currentIndexChanged.connect(self._on_op_changed)
        op_layout.addWidget(QLabel("運算:"))
        op_layout.addWidget(self.op_combo, 1)
        layout.addWidget(op_group)

        # Matrix input area
        input_layout = QHBoxLayout()

        # Matrix A
        a_group = QGroupBox("矩陣 A")
        a_layout = QVBoxLayout(a_group)
        a_layout.addWidget(QLabel("每行以空格或逗號分隔，換行或分號分隔列"))
        self.matrix_a_input = QTextEdit()
        self.matrix_a_input.setPlaceholderText("1 2 3\n4 5 6\n7 8 9")
        self.matrix_a_input.setMaximumHeight(120)
        a_layout.addWidget(self.matrix_a_input)
        input_layout.addWidget(a_group)

        # Matrix B (hidden by default)
        self.b_group = QGroupBox("矩陣 B")
        b_layout = QVBoxLayout(self.b_group)
        self.matrix_b_input = QTextEdit()
        self.matrix_b_input.setPlaceholderText("1 0 0\n0 1 0\n0 0 1")
        self.matrix_b_input.setMaximumHeight(120)
        b_layout.addWidget(self.matrix_b_input)
        self.b_group.setVisible(False)
        input_layout.addWidget(self.b_group)

        layout.addLayout(input_layout)

        # Calculate button
        self.calc_btn = QPushButton("計算")
        self.calc_btn.setMinimumHeight(40)
        self.calc_btn.clicked.connect(self._calculate)
        layout.addWidget(self.calc_btn)

        # Result area
        result_group = QGroupBox("結果")
        result_layout = QVBoxLayout(result_group)
        self.result_scroll = QScrollArea()
        self.result_scroll.setWidgetResizable(True)
        self.result_scroll.setMinimumHeight(200)
        self.result_widget = QWidget()
        self.result_layout = QVBoxLayout(self.result_widget)
        self.result_scroll.setWidget(self.result_widget)
        result_layout.addWidget(self.result_scroll)
        layout.addWidget(result_group, 1)

    def _on_op_changed(self, index):
        needs_b = index >= 7  # Add, Subtract, Multiply
        self.b_group.setVisible(needs_b)

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
        try:
            mat_a = parse_matrix(self.matrix_a_input.toPlainText())
            self._show_result(sympy_to_latex(mat_a), "矩陣 A:")

            if op == 0:  # Determinant
                res = determinant(mat_a)
                self._show_result(sympy_to_latex(res), "行列式 det(A):")
            elif op == 1:  # Inverse
                res = inverse(mat_a)
                self._show_result(sympy_to_latex(res), "反矩陣 A⁻¹:")
            elif op == 2:  # Transpose
                res = transpose(mat_a)
                self._show_result(sympy_to_latex(res), "轉置 Aᵀ:")
            elif op == 3:  # Eigenvalues
                res = eigenvalues(mat_a)
                for val, mult in res.items():
                    self._show_result(
                        f"\\lambda = {sympy_to_latex(val)}, \\quad \\text{{重數}} = {mult}",
                        "特徵值:"
                    )
            elif op == 4:  # Eigenvectors
                res = eigenvectors(mat_a)
                for val, mult, vecs in res:
                    self._show_result(
                        f"\\lambda = {sympy_to_latex(val)}",
                        f"特徵值 (重數 {mult}):"
                    )
                    for v in vecs:
                        self._show_result(sympy_to_latex(v), "特徵向量:")
            elif op == 5:  # Rank
                res = rank(mat_a)
                self._show_result(f"\\text{{rank}}(A) = {res}", "秩:")
            elif op == 6:  # RREF
                res, pivots = rref(mat_a)
                self._show_result(sympy_to_latex(res), "RREF:")
                lbl = QLabel(f"主元列: {list(pivots)}")
                lbl.setStyleSheet("color: #a6e3a1;")
                self.result_layout.addWidget(lbl)
            elif op >= 7:  # Two-matrix operations
                mat_b = parse_matrix(self.matrix_b_input.toPlainText())
                self._show_result(sympy_to_latex(mat_b), "矩陣 B:")
                if op == 7:
                    res = matrix_add(mat_a, mat_b)
                    self._show_result(sympy_to_latex(res), "A + B:")
                elif op == 8:
                    res = matrix_subtract(mat_a, mat_b)
                    self._show_result(sympy_to_latex(res), "A - B:")
                elif op == 9:
                    res = matrix_multiply(mat_a, mat_b)
                    self._show_result(sympy_to_latex(res), "A × B:")

        except Exception as e:
            self._show_error(str(e))

        self.result_layout.addStretch()
