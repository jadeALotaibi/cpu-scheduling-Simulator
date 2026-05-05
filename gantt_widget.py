"""
Animated Gantt Chart Widget for CPU Scheduling Visualization
"""

from PyQt5.QtCore import Qt, QTimer, QRectF, pyqtSignal
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QBrush, QLinearGradient
from PyQt5.QtWidgets import QWidget, QSizePolicy


# Beautiful color palette for processes
PROCESS_COLORS = [
    "#3498db",  # Blue
    "#e74c3c",  # Red
    "#2ecc71",  # Green
    "#f39c12",  # Orange
    "#9b59b6",  # Purple
    "#1abc9c",  # Turquoise
    "#e67e22",  # Carrot
    "#34495e",  # Wet Asphalt
    "#16a085",  # Green Sea
    "#d35400",  # Pumpkin
    "#c0392b",  # Pomegranate
    "#8e44ad",  # Wisteria
]

IDLE_COLOR = "#7f8c8d"


class GanttChartWidget(QWidget):
    """Animated Gantt chart with smooth process visualization."""

    animation_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gantt_blocks = []
        self.process_colors = {}
        self.current_time = 0
        self.max_time = 0
        self.is_animating = False
        self.animation_speed = 100  # ms per time unit

        self.timer = QTimer()
        self.timer.timeout.connect(self._advance_animation)

        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("background-color: #1e272e; border-radius: 8px;")

    def set_data(self, gantt_blocks, processes):
        """Set the Gantt chart data."""
        self.gantt_blocks = gantt_blocks
        self.max_time = max((b.end for b in gantt_blocks), default=0)
        self.current_time = 0

        # Assign colors to processes
        self.process_colors = {}
        unique_pids = []
        for block in gantt_blocks:
            if block.pid not in unique_pids and not block.is_idle:
                unique_pids.append(block.pid)

        for i, pid in enumerate(unique_pids):
            self.process_colors[pid] = PROCESS_COLORS[i % len(PROCESS_COLORS)]
        self.process_colors["IDLE"] = IDLE_COLOR

        self.update()

    def start_animation(self, speed_ms=100):
        """Start the animated playback."""
        if not self.gantt_blocks:
            return
        self.animation_speed = speed_ms
        self.current_time = 0
        self.is_animating = True
        self.timer.start(self.animation_speed)
        self.update()

    def stop_animation(self):
        """Stop the animation."""
        self.timer.stop()
        self.is_animating = False

    def show_complete(self):
        """Show the entire chart at once (no animation)."""
        self.stop_animation()
        self.current_time = self.max_time
        self.update()

    def _advance_animation(self):
        """Advance animation by one time unit."""
        self.current_time += 1
        if self.current_time >= self.max_time:
            self.current_time = self.max_time
            self.timer.stop()
            self.is_animating = False
            self.animation_finished.emit()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self.gantt_blocks or self.max_time == 0:
            self._draw_empty_state(painter)
            return

        # Layout
        margin_left = 20
        margin_right = 20
        margin_top = 30
        bar_height = 70
        time_axis_y = margin_top + bar_height + 25

        width = self.width() - margin_left - margin_right
        unit_width = width / self.max_time

        # Draw title
        painter.setPen(QColor("#ecf0f1"))
        painter.setFont(QFont("Arial", 11, QFont.Bold))
        painter.drawText(margin_left, 20, "Gantt Chart - Process Execution Timeline")

        # Draw blocks
        for block in self.gantt_blocks:
            if block.start >= self.current_time:
                continue

            # Calculate visible portion
            visible_end = min(block.end, self.current_time)
            x = margin_left + block.start * unit_width
            w = (visible_end - block.start) * unit_width

            if w <= 0:
                continue

            # Draw block with gradient
            color = QColor(self.process_colors.get(block.pid, "#95a5a6"))

            gradient = QLinearGradient(x, margin_top, x, margin_top + bar_height)
            gradient.setColorAt(0, color.lighter(120))
            gradient.setColorAt(1, color.darker(110))

            painter.setBrush(QBrush(gradient))
            painter.setPen(QPen(color.darker(150), 2))

            rect = QRectF(x, margin_top, w, bar_height)
            painter.drawRoundedRect(rect, 4, 4)

            # Draw process ID in the block
            if w > 30:
                painter.setPen(QColor("white"))
                painter.setFont(QFont("Arial", 11, QFont.Bold))
                painter.drawText(rect, Qt.AlignCenter, block.pid)

        # Draw time axis
        painter.setPen(QPen(QColor("#bdc3c7"), 2))
        painter.drawLine(margin_left, margin_top + bar_height + 5,
                        margin_left + width, margin_top + bar_height + 5)

        # Draw time markers
        painter.setFont(QFont("Arial", 9))
        painter.setPen(QColor("#ecf0f1"))

        # Determine step size for clean display
        step = max(1, self.max_time // 20)

        for t in range(0, self.max_time + 1, step):
            x = margin_left + t * unit_width
            # Tick mark
            painter.setPen(QPen(QColor("#bdc3c7"), 1))
            painter.drawLine(int(x), margin_top + bar_height + 5,
                           int(x), margin_top + bar_height + 12)
            # Label
            painter.setPen(QColor("#ecf0f1"))
            painter.drawText(int(x - 15), time_axis_y + 5, 30, 15,
                           Qt.AlignCenter, str(t))

        # Always draw last tick
        if self.max_time % step != 0:
            x = margin_left + self.max_time * unit_width
            painter.setPen(QPen(QColor("#bdc3c7"), 1))
            painter.drawLine(int(x), margin_top + bar_height + 5,
                           int(x), margin_top + bar_height + 12)
            painter.setPen(QColor("#ecf0f1"))
            painter.drawText(int(x - 15), time_axis_y + 5, 30, 15,
                           Qt.AlignCenter, str(self.max_time))

        # Draw current time indicator (animated cursor)
        if self.is_animating and self.current_time < self.max_time:
            cursor_x = margin_left + self.current_time * unit_width
            painter.setPen(QPen(QColor("#f1c40f"), 2, Qt.DashLine))
            painter.drawLine(int(cursor_x), margin_top - 5,
                           int(cursor_x), margin_top + bar_height + 10)

            # Pulsing dot at top
            painter.setBrush(QColor("#f1c40f"))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QRectF(cursor_x - 5, margin_top - 12, 10, 10))

    def _draw_empty_state(self, painter):
        """Draw empty state message."""
        painter.setPen(QColor("#7f8c8d"))
        painter.setFont(QFont("Arial", 12))
        painter.drawText(self.rect(), Qt.AlignCenter,
                        "Add processes and click 'Run Simulation' to see Gantt chart")
