"""
PDF Report Generator for Scheduling Results
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


def generate_pdf_report(results, output_path, processes_input, time_quantum=2):
    """Generate a comprehensive PDF report comparing all algorithms."""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        alignment=TA_CENTER,
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#7f8c8d'),
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2980b9'),
        spaceAfter=10,
        spaceBefore=15,
    )

    # Title page
    story.append(Paragraph("CPU Scheduling Algorithms", title_style))
    story.append(Paragraph("Performance Analysis Report", subtitle_style))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        ParagraphStyle('Date', parent=styles['Normal'], alignment=TA_CENTER,
                      textColor=colors.grey, fontSize=10)
    ))
    story.append(Spacer(1, 0.5*inch))

    # Input processes table
    story.append(Paragraph("Input Processes", heading_style))

    input_data = [['Process ID', 'Arrival Time', 'Burst Time', 'Priority']]
    for p in processes_input:
        input_data.append([p.pid, str(p.arrival_time), str(p.burst_time), str(p.priority)])

    input_table = Table(input_data, colWidths=[3*cm, 3*cm, 3*cm, 3*cm])
    input_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ecf0f1')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.HexColor('#ecf0f1'), colors.white]),
    ]))
    story.append(input_table)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph(
        f"<b>Time Quantum (Round Robin):</b> {time_quantum} time units",
        styles['Normal']
    ))

    story.append(PageBreak())

    # Results for each algorithm
    for result in results:
        story.append(Paragraph(result.algorithm_name, heading_style))

        # Process details table
        proc_data = [['PID', 'AT', 'BT', 'CT', 'TAT', 'WT', 'RT']]
        for p in result.processes:
            proc_data.append([
                p.pid,
                str(p.arrival_time),
                str(p.burst_time),
                str(p.completion_time),
                str(p.turnaround_time),
                str(p.waiting_time),
                str(p.response_time),
            ])

        proc_table = Table(proc_data, colWidths=[2*cm]*7)
        proc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1),
             [colors.HexColor('#ecf0f1'), colors.white]),
        ]))
        story.append(proc_table)
        story.append(Spacer(1, 0.2*inch))

        # Gantt chart text representation
        story.append(Paragraph("<b>Gantt Chart:</b>", styles['Normal']))
        gantt_text = " | ".join(
            f"{b.pid}({b.start}-{b.end})" for b in result.gantt_chart
        )
        story.append(Paragraph(gantt_text, ParagraphStyle(
            'Gantt', parent=styles['Code'], fontSize=9,
            textColor=colors.HexColor('#2c3e50'),
            backColor=colors.HexColor('#ecf0f1'),
            borderPadding=8, leftIndent=5, rightIndent=5,
        )))
        story.append(Spacer(1, 0.2*inch))

        # Performance metrics
        metrics_data = [
            ['Metric', 'Value'],
            ['Average Waiting Time', f"{result.avg_waiting_time:.2f} units"],
            ['Average Turnaround Time', f"{result.avg_turnaround_time:.2f} units"],
            ['Average Response Time', f"{result.avg_response_time:.2f} units"],
            ['CPU Utilization', f"{result.cpu_utilization:.2f}%"],
            ['Throughput', f"{result.throughput:.4f} processes/unit"],
            ['Total Execution Time', f"{result.total_time} units"],
        ]

        metrics_table = Table(metrics_data, colWidths=[6*cm, 6*cm])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 0.4*inch))

    # Comparison summary
    story.append(PageBreak())
    story.append(Paragraph("Algorithms Comparison Summary", heading_style))

    comparison_data = [
        ['Algorithm', 'Avg WT', 'Avg TAT', 'Avg RT', 'CPU%']
    ]
    for r in results:
        comparison_data.append([
            r.algorithm_name,
            f"{r.avg_waiting_time:.2f}",
            f"{r.avg_turnaround_time:.2f}",
            f"{r.avg_response_time:.2f}",
            f"{r.cpu_utilization:.1f}%",
        ])

    comp_table = Table(comparison_data, colWidths=[5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8e44ad')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#bdc3c7')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1),
         [colors.HexColor('#ecf0f1'), colors.white]),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 0.3*inch))

    # Best algorithm analysis
    best_wt = min(results, key=lambda r: r.avg_waiting_time)
    best_tat = min(results, key=lambda r: r.avg_turnaround_time)
    best_rt = min(results, key=lambda r: r.avg_response_time)

    story.append(Paragraph("Analysis", heading_style))
    analysis_text = f"""
    <b>Best Average Waiting Time:</b> {best_wt.algorithm_name} ({best_wt.avg_waiting_time:.2f} units)<br/>
    <b>Best Average Turnaround Time:</b> {best_tat.algorithm_name} ({best_tat.avg_turnaround_time:.2f} units)<br/>
    <b>Best Average Response Time:</b> {best_rt.algorithm_name} ({best_rt.avg_response_time:.2f} units)<br/><br/>

    <b>Recommendation:</b> The choice of algorithm depends on system requirements.
    SJF generally minimizes waiting time but can cause starvation. Round Robin provides
    fair CPU allocation and is ideal for time-sharing systems. FCFS is simple but can
    lead to the convoy effect. Priority scheduling is useful when tasks have different
    importance levels.
    """
    story.append(Paragraph(analysis_text, styles['Normal']))

    # Build PDF
    doc.build(story)
    return output_path
