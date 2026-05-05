"""
CPU Scheduling Simulator - Main GUI Application
A professional, animated CPU scheduling simulator with comparison features.
"""

import sys
import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QComboBox, QGroupBox, QGridLayout, QMessageBox,
    QFileDialog, QTabWidget, QFrame, QScrollArea, QSplitter,
    QStackedWidget, QSlider, QTextEdit
)

from algorithms import (
    Process, fcfs, sjf_non_preemptive, round_robin,
    priority_scheduling, run_all_algorithms, SchedulingResult
)
from gantt_widget import GanttChartWidget, PROCESS_COLORS


# ============ STYLES ============
DARK_STYLESHEET = """
QMainWindow {
    background-color: #2c3e50;
}

QWidget {
    color: #ecf0f1;
    font-family: 'Segoe UI', Arial, sans-serif;
}

QGroupBox {
    background-color: #34495e;
    border: 2px solid #2c3e50;
    border-radius: 8px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: bold;
    font-size: 13px;
    color: #ecf0f1;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
    color: #3498db;
}

QPushButton {
    background-color: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-weight: bold;
    font-size: 12px;
    min-height: 18px;
}

QPushButton:hover {
    background-color: #2980b9;
}

QPushButton:pressed {
    background-color: #21618c;
}

QPushButton:disabled {
    background-color: #7f8c8d;
    color: #bdc3c7;
}

QPushButton#successBtn {
    background-color: #27ae60;
}
QPushButton#successBtn:hover {
    background-color: #229954;
}

QPushButton#dangerBtn {
    background-color: #e74c3c;
}
QPushButton#dangerBtn:hover {
    background-color: #c0392b;
}

QPushButton#warningBtn {
    background-color: #f39c12;
}
QPushButton#warningBtn:hover {
    background-color: #e67e22;
}

QPushButton#purpleBtn {
    background-color: #9b59b6;
}
QPushButton#purpleBtn:hover {
    background-color: #8e44ad;
}

QTableWidget {
    background-color: #ecf0f1;
    color: #2c3e50;
    border: 1px solid #34495e;
    border-radius: 6px;
    gridline-color: #bdc3c7;
    font-size: 11px;
    selection-background-color: #3498db;
    selection-color: white;
}

QTableWidget::item {
    padding: 6px;
}

QHeaderView::section {
    background-color: #2c3e50;
    color: white;
    padding: 8px;
    border: none;
    font-weight: bold;
    font-size: 11px;
}

QSpinBox, QComboBox {
    background-color: #ecf0f1;
    color: #2c3e50;
    border: 1px solid #34495e;
    border-radius: 4px;
    padding: 5px 8px;
    min-height: 20px;
    font-size: 11px;
}

QSpinBox:focus, QComboBox:focus {
    border: 2px solid #3498db;
}

QComboBox::drop-down {
    border: none;
    width: 25px;
}

QComboBox QAbstractItemView {
    background-color: #ecf0f1;
    color: #2c3e50;
    selection-background-color: #3498db;
    selection-color: white;
}

QLabel {
    color: #ecf0f1;
    font-size: 12px;
}

QLabel#titleLabel {
    color: #3498db;
    font-size: 24px;
    font-weight: bold;
}

QLabel#subtitleLabel {
    color: #bdc3c7;
    font-size: 12px;
    font-style: italic;
}

QLabel#metricLabel {
    color: #f39c12;
    font-size: 14px;
    font-weight: bold;
}

QLabel#metricValue {
    color: #2ecc71;
    font-size: 18px;
    font-weight: bold;
}

QTabWidget::pane {
    background-color: #34495e;
    border: 1px solid #2c3e50;
    border-radius: 6px;
}

QTabBar::tab {
    background-color: #2c3e50;
    color: #bdc3c7;
    padding: 10px 20px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    font-weight: bold;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #3498db;
    color: white;
}

QTabBar::tab:hover:!selected {
    background-color: #34495e;
    color: #ecf0f1;
}

QSlider::groove:horizontal {
    height: 6px;
    background: #34495e;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #3498db;
    width: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background: #2980b9;
}

QScrollArea {
    border: none;
    background-color: transparent;
}

QFrame#metricCard {
    background-color: #34495e;
    border: 2px solid #3498db;
    border-radius: 8px;
}
"""


class MetricCard(QFrame):
    """A card widget displaying a single metric."""

    def __init__(self, title, value="--", color="#3498db"):
        super().__init__()
        self.setObjectName("metricCard")
        self.setStyleSheet(f"""
            QFrame#metricCard {{
                background-color: #34495e;
                border-left: 4px solid {color};
                border-radius: 6px;
                padding: 8px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(4)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("color: #bdc3c7; font-size: 11px; font-weight: normal;")

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"color: {color}; font-size: 20px; font-weight: bold;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value):
        self.value_label.setText(str(value))


class CPUSchedulerApp(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.results = []  # All algorithm results
        self.current_result = None
        self.processes_input = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CPU Scheduling Simulator - Operating Systems Project")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet(DARK_STYLESHEET)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Header
        self.create_header(main_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_simulator_tab(), "🎯  Simulator")
        self.tabs.addTab(self.create_comparison_tab(), "📊  Algorithm Comparison")
        self.tabs.addTab(self.create_about_tab(), "ℹ️  About")

        main_layout.addWidget(self.tabs)

        # Status bar
        self.statusBar().setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")
        self.statusBar().showMessage("Ready - Add processes and run simulation")

        # Load sample data
        self.load_sample_data()

    def create_header(self, layout):
        """Create the header section."""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 8px;
                padding: 12px;
            }
        """)
        header_layout = QHBoxLayout(header)

        # Title section
        title_section = QVBoxLayout()
        title = QLabel("⚙️  CPU Scheduling Simulator")
        title.setObjectName("titleLabel")

        subtitle = QLabel("FCFS  •  SJF  •  Round Robin  •  Priority Scheduling")
        subtitle.setObjectName("subtitleLabel")

        title_section.addWidget(title)
        title_section.addWidget(subtitle)

        header_layout.addLayout(title_section)
        header_layout.addStretch()

        # Stats summary in header
        self.processes_count_label = QLabel("Processes: 0")
        self.processes_count_label.setStyleSheet(
            "color: #3498db; font-size: 14px; font-weight: bold; padding: 8px;"
        )
        header_layout.addWidget(self.processes_count_label)

        layout.addWidget(header)

    def create_simulator_tab(self):
        """Create the main simulator tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)

        # Top section: Process input and controls
        top_splitter = QSplitter(Qt.Horizontal)

        # Left: Process table
        process_group = QGroupBox("📋  Process Input")
        process_layout = QVBoxLayout(process_group)

        self.process_table = QTableWidget(0, 4)
        self.process_table.setHorizontalHeaderLabels(
            ["Process ID", "Arrival Time", "Burst Time", "Priority"]
        )
        self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.process_table.verticalHeader().setVisible(False)
        process_layout.addWidget(self.process_table)

        # Process control buttons
        process_btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Process")
        add_btn.setObjectName("successBtn")
        add_btn.clicked.connect(self.add_process_row)

        remove_btn = QPushButton("➖ Remove Selected")
        remove_btn.setObjectName("dangerBtn")
        remove_btn.clicked.connect(self.remove_selected_row)

        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.setObjectName("warningBtn")
        clear_btn.clicked.connect(self.clear_all_processes)

        sample_btn = QPushButton("📝 Load Sample")
        sample_btn.clicked.connect(self.load_sample_data)

        process_btn_layout.addWidget(add_btn)
        process_btn_layout.addWidget(remove_btn)
        process_btn_layout.addWidget(clear_btn)
        process_btn_layout.addWidget(sample_btn)
        process_layout.addLayout(process_btn_layout)

        top_splitter.addWidget(process_group)

        # Right: Algorithm selection and controls
        control_group = QGroupBox("⚙️  Algorithm & Controls")
        control_layout = QGridLayout(control_group)
        control_layout.setSpacing(12)

        # Algorithm selector
        algo_label = QLabel("Algorithm:")
        algo_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.algo_combo = QComboBox()
        self.algo_combo.addItems([
            "FCFS - First Come First Served",
            "SJF - Shortest Job First",
            "Round Robin",
            "Priority Scheduling (Non-Preemptive)",
            "Priority Scheduling (Preemptive)",
        ])
        self.algo_combo.currentIndexChanged.connect(self.on_algorithm_changed)
        control_layout.addWidget(algo_label, 0, 0)
        control_layout.addWidget(self.algo_combo, 0, 1)

        # Time quantum (for Round Robin)
        self.quantum_label = QLabel("Time Quantum:")
        self.quantum_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.quantum_spin = QSpinBox()
        self.quantum_spin.setRange(1, 20)
        self.quantum_spin.setValue(2)
        control_layout.addWidget(self.quantum_label, 1, 0)
        control_layout.addWidget(self.quantum_spin, 1, 1)
        self.quantum_label.setVisible(False)
        self.quantum_spin.setVisible(False)

        # Animation speed
        speed_label = QLabel("Animation Speed:")
        speed_label.setStyleSheet("font-weight: bold; font-size: 13px;")
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setRange(50, 500)
        self.speed_slider.setValue(150)
        self.speed_slider.setInvertedAppearance(True)
        self.speed_value_label = QLabel("Normal")
        self.speed_slider.valueChanged.connect(self.update_speed_label)
        speed_layout = QHBoxLayout()
        speed_layout.addWidget(self.speed_slider)
        speed_layout.addWidget(self.speed_value_label)
        control_layout.addWidget(speed_label, 2, 0)
        control_layout.addLayout(speed_layout, 2, 1)

        # Run buttons
        run_btn = QPushButton("▶️  Run Simulation")
        run_btn.setObjectName("successBtn")
        run_btn.setStyleSheet(run_btn.styleSheet() + "font-size: 14px; padding: 12px;")
        run_btn.clicked.connect(self.run_simulation)
        control_layout.addWidget(run_btn, 3, 0, 1, 2)

        run_all_btn = QPushButton("🔄  Run All Algorithms (Compare)")
        run_all_btn.setObjectName("purpleBtn")
        run_all_btn.setStyleSheet(run_all_btn.styleSheet() + "font-size: 13px; padding: 10px;")
        run_all_btn.clicked.connect(self.run_all_algorithms)
        control_layout.addWidget(run_all_btn, 4, 0, 1, 2)

        # Animation controls
        anim_layout = QHBoxLayout()
        self.replay_btn = QPushButton("⏪ Replay Animation")
        self.replay_btn.clicked.connect(self.replay_animation)
        self.replay_btn.setEnabled(False)

        self.skip_btn = QPushButton("⏭️ Show Final")
        self.skip_btn.clicked.connect(self.skip_animation)
        self.skip_btn.setEnabled(False)

        anim_layout.addWidget(self.replay_btn)
        anim_layout.addWidget(self.skip_btn)
        control_layout.addLayout(anim_layout, 5, 0, 1, 2)

        # Export button
        export_btn = QPushButton("📄  Export PDF Report")
        export_btn.setObjectName("warningBtn")
        export_btn.clicked.connect(self.export_pdf)
        control_layout.addWidget(export_btn, 6, 0, 1, 2)

        control_layout.setRowStretch(7, 1)

        top_splitter.addWidget(control_group)
        top_splitter.setSizes([800, 500])
        layout.addWidget(top_splitter)

        # Gantt chart section
        gantt_group = QGroupBox("📊  Gantt Chart Visualization")
        gantt_layout = QVBoxLayout(gantt_group)

        self.gantt_widget = GanttChartWidget()
        self.gantt_widget.animation_finished.connect(self.on_animation_finished)
        gantt_layout.addWidget(self.gantt_widget)

        # Process color legend
        self.legend_layout = QHBoxLayout()
        self.legend_layout.setAlignment(Qt.AlignCenter)
        self.legend_layout.setSpacing(15)
        legend_widget = QWidget()
        legend_widget.setLayout(self.legend_layout)
        gantt_layout.addWidget(legend_widget)

        layout.addWidget(gantt_group)

        # Metrics section
        metrics_group = QGroupBox("📈  Performance Metrics")
        metrics_outer = QVBoxLayout(metrics_group)
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(10)

        self.metric_wt = MetricCard("Avg Waiting Time", "--", "#3498db")
        self.metric_tat = MetricCard("Avg Turnaround Time", "--", "#e74c3c")
        self.metric_rt = MetricCard("Avg Response Time", "--", "#f39c12")
        self.metric_cpu = MetricCard("CPU Utilization", "--", "#2ecc71")
        self.metric_throughput = MetricCard("Throughput", "--", "#9b59b6")

        metrics_layout.addWidget(self.metric_wt)
        metrics_layout.addWidget(self.metric_tat)
        metrics_layout.addWidget(self.metric_rt)
        metrics_layout.addWidget(self.metric_cpu)
        metrics_layout.addWidget(self.metric_throughput)

        metrics_outer.addLayout(metrics_layout)

        # Results table
        self.results_table = QTableWidget(0, 7)
        self.results_table.setHorizontalHeaderLabels([
            "PID", "Arrival", "Burst", "Completion", "Turnaround", "Waiting", "Response"
        ])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.verticalHeader().setVisible(False)
        self.results_table.setMaximumHeight(200)
        metrics_outer.addWidget(self.results_table)

        layout.addWidget(metrics_group)

        return widget

    def create_comparison_tab(self):
        """Create the algorithm comparison tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        info_label = QLabel(
            "📊 Compare all algorithms side-by-side. Click 'Run All Algorithms' on the Simulator tab."
        )
        info_label.setStyleSheet(
            "background-color: #34495e; padding: 12px; border-radius: 6px; "
            "color: #3498db; font-size: 13px; font-weight: bold;"
        )
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        # Comparison table
        comparison_group = QGroupBox("🏆  Algorithm Performance Comparison")
        comp_layout = QVBoxLayout(comparison_group)

        self.comparison_table = QTableWidget(0, 6)
        self.comparison_table.setHorizontalHeaderLabels([
            "Algorithm", "Avg WT", "Avg TAT", "Avg RT", "CPU %", "Throughput"
        ])
        self.comparison_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.comparison_table.verticalHeader().setVisible(False)
        comp_layout.addWidget(self.comparison_table)

        layout.addWidget(comparison_group)

        # Best algorithm highlights
        winners_group = QGroupBox("🥇  Winners by Metric")
        winners_layout = QHBoxLayout(winners_group)
        winners_layout.setSpacing(10)

        self.winner_wt = MetricCard("Best Waiting Time", "--", "#3498db")
        self.winner_tat = MetricCard("Best Turnaround", "--", "#e74c3c")
        self.winner_rt = MetricCard("Best Response", "--", "#f39c12")

        winners_layout.addWidget(self.winner_wt)
        winners_layout.addWidget(self.winner_tat)
        winners_layout.addWidget(self.winner_rt)

        layout.addWidget(winners_group)

        # All Gantt charts comparison
        gantt_compare_group = QGroupBox("📊  All Algorithms Gantt Charts")
        gantt_compare_layout = QVBoxLayout(gantt_compare_group)

        self.comparison_gantt_area = QScrollArea()
        self.comparison_gantt_area.setWidgetResizable(True)
        self.comparison_gantt_widget = QWidget()
        self.comparison_gantt_layout = QVBoxLayout(self.comparison_gantt_widget)
        self.comparison_gantt_area.setWidget(self.comparison_gantt_widget)

        gantt_compare_layout.addWidget(self.comparison_gantt_area)
        layout.addWidget(gantt_compare_group)

        return widget

    def create_about_tab(self):
        """Create the about/info tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)

        about_text = QTextEdit()
        about_text.setReadOnly(True)
        about_text.setStyleSheet("""
            QTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #2c3e50;
                border-radius: 8px;
                padding: 20px;
                font-size: 13px;
            }
        """)

        about_html = """
        <h1 style="color: #3498db;">⚙️ CPU Scheduling Simulator</h1>
        <p style="color: #bdc3c7; font-style: italic;">
            A comprehensive operating systems project demonstrating CPU scheduling algorithms
        </p>

        <h2 style="color: #2ecc71;">🎯 Implemented Algorithms</h2>
        <ul>
            <li><b style="color: #3498db;">FCFS (First Come First Served):</b>
                Non-preemptive algorithm that schedules processes in order of arrival.
                Simple but suffers from the convoy effect.</li>
            <li><b style="color: #e74c3c;">SJF (Shortest Job First):</b>
                Selects the process with shortest burst time. Provides optimal average
                waiting time but can cause starvation.</li>
            <li><b style="color: #f39c12;">Round Robin:</b>
                Time-sharing algorithm with configurable time quantum. Fair allocation
                ideal for interactive systems.</li>
            <li><b style="color: #9b59b6;">Priority Scheduling:</b>
                Schedules based on priority (lower number = higher priority). Available
                in both preemptive and non-preemptive variants.</li>
        </ul>

        <h2 style="color: #2ecc71;">📊 Performance Metrics</h2>
        <ul>
            <li><b>Waiting Time (WT):</b> Time spent in ready queue</li>
            <li><b>Turnaround Time (TAT):</b> Total time from arrival to completion</li>
            <li><b>Response Time (RT):</b> Time from arrival to first execution</li>
            <li><b>CPU Utilization:</b> Percentage of time CPU was busy</li>
            <li><b>Throughput:</b> Number of processes completed per time unit</li>
        </ul>

        <h2 style="color: #2ecc71;">✨ Features</h2>
        <ul>
            <li>🎬 <b>Animated Gantt Chart</b> - Visualizes process execution in real-time</li>
            <li>🔄 <b>Algorithm Comparison</b> - Run all algorithms simultaneously to compare</li>
            <li>📄 <b>PDF Report Export</b> - Generate professional reports with all results</li>
            <li>🎨 <b>Modern Dark UI</b> - Clean, professional interface</li>
            <li>⚙️ <b>Configurable Parameters</b> - Adjust time quantum and animation speed</li>
        </ul>

        <h2 style="color: #2ecc71;">📚 How to Use</h2>
        <ol>
            <li>Add processes to the input table (PID, Arrival Time, Burst Time, Priority)</li>
            <li>Select an algorithm from the dropdown</li>
            <li>Configure time quantum (for Round Robin)</li>
            <li>Click "Run Simulation" to see the animated execution</li>
            <li>View detailed metrics and process completion data</li>
            <li>Click "Run All Algorithms" to compare all algorithms</li>
            <li>Export results as a professional PDF report</li>
        </ol>

        <p style="color: #95a5a6; margin-top: 30px; text-align: center;">
            <i>Built with Python + PyQt5 — Operating Systems Course Project</i>
        </p>
        """

        about_text.setHtml(about_html)
        layout.addWidget(about_text)

        return widget

    # ============ EVENT HANDLERS ============

    def on_algorithm_changed(self, index):
        """Show/hide quantum input based on algorithm."""
        is_round_robin = self.algo_combo.currentText().startswith("Round Robin")
        self.quantum_label.setVisible(is_round_robin)
        self.quantum_spin.setVisible(is_round_robin)

    def update_speed_label(self, value):
        """Update speed display label."""
        if value < 100:
            self.speed_value_label.setText("Fast")
        elif value < 200:
            self.speed_value_label.setText("Normal")
        elif value < 350:
            self.speed_value_label.setText("Slow")
        else:
            self.speed_value_label.setText("Very Slow")

    def add_process_row(self):
        """Add a new empty row to the process table."""
        row = self.process_table.rowCount()
        self.process_table.insertRow(row)

        # Default values
        self.process_table.setItem(row, 0, QTableWidgetItem(f"P{row + 1}"))
        self.process_table.setItem(row, 1, QTableWidgetItem("0"))
        self.process_table.setItem(row, 2, QTableWidgetItem("5"))
        self.process_table.setItem(row, 3, QTableWidgetItem("1"))

        for col in range(4):
            item = self.process_table.item(row, col)
            if col != 0:
                item.setTextAlignment(Qt.AlignCenter)

        self.update_process_count()

    def remove_selected_row(self):
        """Remove the selected row."""
        rows = sorted(set(item.row() for item in self.process_table.selectedItems()), reverse=True)
        for row in rows:
            self.process_table.removeRow(row)
        self.update_process_count()

    def clear_all_processes(self):
        """Clear all processes."""
        reply = QMessageBox.question(
            self, "Confirm Clear",
            "Are you sure you want to clear all processes?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.process_table.setRowCount(0)
            self.update_process_count()

    def load_sample_data(self):
        """Load sample process data."""
        self.process_table.setRowCount(0)
        sample = [
            ("P1", "0", "8", "3"),
            ("P2", "1", "4", "1"),
            ("P3", "2", "9", "4"),
            ("P4", "3", "5", "2"),
            ("P5", "4", "2", "3"),
        ]
        for pid, at, bt, pri in sample:
            row = self.process_table.rowCount()
            self.process_table.insertRow(row)
            for col, val in enumerate([pid, at, bt, pri]):
                item = QTableWidgetItem(val)
                if col != 0:
                    item.setTextAlignment(Qt.AlignCenter)
                self.process_table.setItem(row, col, item)
        self.update_process_count()
        self.statusBar().showMessage("Sample data loaded")

    def update_process_count(self):
        """Update process count display."""
        count = self.process_table.rowCount()
        self.processes_count_label.setText(f"Processes: {count}")

    def get_processes_from_table(self):
        """Read processes from the input table."""
        processes = []
        for row in range(self.process_table.rowCount()):
            try:
                pid = self.process_table.item(row, 0).text().strip()
                at = int(self.process_table.item(row, 1).text())
                bt = int(self.process_table.item(row, 2).text())
                pri = int(self.process_table.item(row, 3).text())

                if not pid:
                    raise ValueError(f"Row {row + 1}: Process ID is empty")
                if at < 0:
                    raise ValueError(f"Row {row + 1}: Arrival time must be >= 0")
                if bt <= 0:
                    raise ValueError(f"Row {row + 1}: Burst time must be > 0")

                processes.append(Process(pid=pid, arrival_time=at, burst_time=bt, priority=pri))
            except (ValueError, AttributeError) as e:
                raise ValueError(f"Invalid data in row {row + 1}: {str(e)}")

        if not processes:
            raise ValueError("No processes defined. Please add at least one process.")

        return processes

    def run_simulation(self):
        """Run the selected algorithm."""
        try:
            processes = self.get_processes_from_table()
            self.processes_input = processes
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return

        algo_name = self.algo_combo.currentText()
        quantum = self.quantum_spin.value()

        try:
            if algo_name.startswith("FCFS"):
                result = fcfs(processes)
            elif algo_name.startswith("SJF"):
                result = sjf_non_preemptive(processes)
            elif algo_name.startswith("Round Robin"):
                result = round_robin(processes, quantum)
            elif algo_name.startswith("Priority Scheduling (Non-Preemptive)"):
                result = priority_scheduling(processes, preemptive=False)
            elif algo_name.startswith("Priority Scheduling (Preemptive)"):
                result = priority_scheduling(processes, preemptive=True)
            else:
                return

            self.current_result = result
            self.display_result(result)
            self.statusBar().showMessage(f"Simulation completed: {result.algorithm_name}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Simulation failed: {str(e)}")

    def display_result(self, result: SchedulingResult):
        """Display the result in the UI with animation."""
        # Set Gantt data
        self.gantt_widget.set_data(result.gantt_chart, result.processes)

        # Update legend
        self.update_legend(result)

        # Update metrics
        self.metric_wt.set_value(f"{result.avg_waiting_time:.2f}")
        self.metric_tat.set_value(f"{result.avg_turnaround_time:.2f}")
        self.metric_rt.set_value(f"{result.avg_response_time:.2f}")
        self.metric_cpu.set_value(f"{result.cpu_utilization:.1f}%")
        self.metric_throughput.set_value(f"{result.throughput:.4f}")

        # Update results table
        self.results_table.setRowCount(len(result.processes))
        for row, p in enumerate(result.processes):
            values = [
                p.pid, str(p.arrival_time), str(p.burst_time),
                str(p.completion_time), str(p.turnaround_time),
                str(p.waiting_time), str(p.response_time)
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                self.results_table.setItem(row, col, item)

        # Start animation
        speed = self.speed_slider.value()
        self.gantt_widget.start_animation(speed)
        self.replay_btn.setEnabled(True)
        self.skip_btn.setEnabled(True)

    def update_legend(self, result):
        """Update the process color legend."""
        # Clear existing legend
        while self.legend_layout.count():
            item = self.legend_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Add legend items
        unique_pids = []
        for block in result.gantt_chart:
            if block.pid not in unique_pids and not block.is_idle:
                unique_pids.append(block.pid)

        for i, pid in enumerate(unique_pids):
            color = PROCESS_COLORS[i % len(PROCESS_COLORS)]
            legend_item = QLabel(f"  ●  {pid}  ")
            legend_item.setStyleSheet(
                f"color: {color}; font-size: 14px; font-weight: bold;"
            )
            self.legend_layout.addWidget(legend_item)

    def replay_animation(self):
        """Replay the current animation."""
        if self.current_result:
            speed = self.speed_slider.value()
            self.gantt_widget.start_animation(speed)

    def skip_animation(self):
        """Skip animation and show final state."""
        self.gantt_widget.show_complete()

    def on_animation_finished(self):
        """Called when animation completes."""
        self.statusBar().showMessage("Animation completed")

    def run_all_algorithms(self):
        """Run all algorithms for comparison."""
        try:
            processes = self.get_processes_from_table()
            self.processes_input = processes
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))
            return

        quantum = self.quantum_spin.value()
        self.results = run_all_algorithms(processes, quantum)
        self.update_comparison_tab()
        self.tabs.setCurrentIndex(1)
        self.statusBar().showMessage("All algorithms executed - check Comparison tab")

    def update_comparison_tab(self):
        """Update the comparison tab with all results."""
        # Clear comparison table
        self.comparison_table.setRowCount(len(self.results))

        for row, r in enumerate(self.results):
            values = [
                r.algorithm_name,
                f"{r.avg_waiting_time:.2f}",
                f"{r.avg_turnaround_time:.2f}",
                f"{r.avg_response_time:.2f}",
                f"{r.cpu_utilization:.1f}%",
                f"{r.throughput:.4f}",
            ]
            for col, val in enumerate(values):
                item = QTableWidgetItem(val)
                if col == 0:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignCenter)
                self.comparison_table.setItem(row, col, item)

        # Highlight best in each metric
        best_wt = min(self.results, key=lambda r: r.avg_waiting_time)
        best_tat = min(self.results, key=lambda r: r.avg_turnaround_time)
        best_rt = min(self.results, key=lambda r: r.avg_response_time)

        for row, r in enumerate(self.results):
            if r is best_wt:
                self.comparison_table.item(row, 1).setBackground(QColor("#27ae60"))
                self.comparison_table.item(row, 1).setForeground(QColor("white"))
            if r is best_tat:
                self.comparison_table.item(row, 2).setBackground(QColor("#27ae60"))
                self.comparison_table.item(row, 2).setForeground(QColor("white"))
            if r is best_rt:
                self.comparison_table.item(row, 3).setBackground(QColor("#27ae60"))
                self.comparison_table.item(row, 3).setForeground(QColor("white"))

        # Update winner cards
        self.winner_wt.set_value(f"{best_wt.algorithm_name.split('(')[0].strip()}\n{best_wt.avg_waiting_time:.2f}")
        self.winner_tat.set_value(f"{best_tat.algorithm_name.split('(')[0].strip()}\n{best_tat.avg_turnaround_time:.2f}")
        self.winner_rt.set_value(f"{best_rt.algorithm_name.split('(')[0].strip()}\n{best_rt.avg_response_time:.2f}")

        # Clear and rebuild Gantt comparisons
        while self.comparison_gantt_layout.count():
            item = self.comparison_gantt_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for r in self.results:
            label = QLabel(f"<b>{r.algorithm_name}</b>")
            label.setStyleSheet("color: #3498db; font-size: 14px; padding: 8px;")
            self.comparison_gantt_layout.addWidget(label)

            gantt = GanttChartWidget()
            gantt.set_data(r.gantt_chart, r.processes)
            gantt.show_complete()
            gantt.setMinimumHeight(150)
            self.comparison_gantt_layout.addWidget(gantt)

    def export_pdf(self):
        """Export results to PDF."""
        if not self.results and not self.current_result:
            QMessageBox.information(
                self, "No Data",
                "Please run a simulation first before exporting."
            )
            return

        # If no full comparison was run, run all now
        if not self.results:
            try:
                processes = self.get_processes_from_table()
                self.results = run_all_algorithms(processes, self.quantum_spin.value())
                self.processes_input = processes
            except ValueError as e:
                QMessageBox.warning(self, "Invalid Input", str(e))
                return

        # Choose save location
        path, _ = QFileDialog.getSaveFileName(
            self, "Save PDF Report",
            "scheduling_report.pdf",
            "PDF Files (*.pdf)"
        )

        if not path:
            return

        try:
            from pdf_report import generate_pdf_report
            generate_pdf_report(
                self.results, path, self.processes_input,
                self.quantum_spin.value()
            )
            QMessageBox.information(
                self, "Success",
                f"PDF report saved successfully to:\n{path}"
            )
            self.statusBar().showMessage(f"Report exported: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export PDF:\n{str(e)}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Set application font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    window = CPUSchedulerApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
