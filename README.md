# ⚙️ CPU Scheduling Simulator

A professional, animated CPU scheduling algorithms simulator built with Python and PyQt5.

محاكي خوارزميات جدولة المعالج - مشروع مادة أنظمة التشغيل

---

## 📋 Implemented Algorithms | الخوارزميات المنفذة

1. **FCFS** - First Come First Served
2. **SJF** - Shortest Job First (Non-Preemptive)
3. **Round Robin** - With configurable time quantum
4. **Priority Scheduling** - Both Preemptive & Non-Preemptive

---

## ✨ Features | المميزات

- 🎬 **Animated Gantt Chart** - Real-time visualization of process execution
- 🔄 **Algorithm Comparison** - Run all algorithms simultaneously and compare
- 📊 **Performance Metrics** - WT, TAT, RT, CPU Utilization, Throughput
- 📄 **PDF Report Export** - Professional reports with full analysis
- 🎨 **Modern Dark UI** - Clean, professional interface
- ⚙️ **Configurable** - Adjustable time quantum and animation speed
- 🏆 **Winner Highlighting** - Automatically identifies best algorithm per metric

---

## 🚀 Installation & Running | التثبيت والتشغيل

### Step 1: Install Python 3.8 or higher

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

Or install directly:
```bash
pip install PyQt5 reportlab
```

### Step 3: Run the application
```bash
python main.py
```

---

## 📁 Project Structure | هيكلة المشروع

```
cpu_scheduler/
├── main.py              # Main GUI application
├── algorithms.py        # Scheduling algorithms implementation
├── gantt_widget.py      # Custom animated Gantt chart widget
├── pdf_report.py        # PDF report generator
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

## 🎯 How to Use | طريقة الاستخدام

1. **Add Processes** - Enter PID, Arrival Time, Burst Time, and Priority
2. **Select Algorithm** - Choose from the dropdown menu
3. **Configure Parameters** - Set time quantum for Round Robin
4. **Run Simulation** - Click "Run Simulation" to see animation
5. **Compare Algorithms** - Click "Run All Algorithms" for comparison
6. **Export Report** - Generate professional PDF report

---

## 📊 Performance Metrics Explained

| Metric | Description |
|--------|-------------|
| **Waiting Time (WT)** | Time spent in ready queue |
| **Turnaround Time (TAT)** | Total time from arrival to completion |
| **Response Time (RT)** | Time from arrival to first execution |
| **CPU Utilization** | Percentage of time CPU was busy |
| **Throughput** | Processes completed per time unit |

---

## 🎓 Educational Use

This project is designed for Operating Systems courses to demonstrate:
- Different scheduling strategies
- Performance comparison between algorithms
- Visual understanding of process execution
- Trade-offs between different metrics

---

## 🛠️ Technical Stack

- **Language:** Python 3.8+
- **GUI Framework:** PyQt5
- **PDF Generation:** ReportLab
- **Architecture:** Modular MVC pattern
