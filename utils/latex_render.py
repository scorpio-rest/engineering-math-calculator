import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import Qt
import sympy as sp


def render_latex_to_pixmap(latex_str, font_size=16, dpi=150):
    """Render a LaTeX string to a QPixmap using matplotlib."""
    fig = Figure(figsize=(0.1, 0.1))
    fig.patch.set_facecolor('#1e1e2e')
    fig.text(
        0.5, 0.5,
        f"${latex_str}$",
        fontsize=font_size,
        color='#cdd6f4',
        ha='center', va='center',
    )

    fig.savefig(buf := io.BytesIO(), format='png', dpi=dpi,
                bbox_inches='tight', pad_inches=0.15,
                facecolor='#1e1e2e', edgecolor='none')
    plt.close(fig)

    buf.seek(0)
    image = QImage.fromData(buf.read())
    return QPixmap.fromImage(image)


def render_latex_label(latex_str, font_size=16, max_width=700):
    """Create a QLabel displaying rendered LaTeX."""
    label = QLabel()
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    try:
        pixmap = render_latex_to_pixmap(latex_str, font_size)
        if pixmap.width() > max_width:
            pixmap = pixmap.scaledToWidth(max_width, Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(pixmap)
    except Exception as e:
        label.setText(f"Render error: {e}")
        label.setStyleSheet("color: #f38ba8;")
    return label


def sympy_to_latex(expr):
    """Convert a SymPy expression to LaTeX string."""
    return sp.latex(expr)
