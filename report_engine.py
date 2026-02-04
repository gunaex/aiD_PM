from fpdf import FPDF
import datetime
import os

class ProjectReport(FPDF):
    def header(self):
        # Logo placeholder or Title
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(30, 41, 59) # Slate 800
        self.cell(0, 10, 'Executive Project Performance Report', 0, 1, 'C')
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 5, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100)
        self.cell(0, 10, f'Page {self.page_no()} | aiD_PM Smart Control Tower', 0, 0, 'C')

def generate_project_pdf(project_data: dict, output_path: str):
    pdf = ProjectReport()
    pdf.add_page()
    
    # --- 1. Project Header Section ---
    pdf.set_fill_color(241, 245, 249) # Slate 100
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 10, f" Project: {project_data['name']}", 0, 1, 'L', True)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(50, 8, f"Customer: {project_data['customer']}", 0, 0)
    pdf.cell(50, 8, f"Methodology: {project_data['methodology']}", 0, 0)
    status_text = "RECOVERY MODE" if project_data['is_recovery_mode'] else "NOMINAL"
    pdf.set_text_color(220, 38, 38) if project_data['is_recovery_mode'] else pdf.set_text_color(22, 163, 74)
    pdf.cell(0, 8, f"Status: {status_text}", 0, 1, 'R')
    pdf.set_text_color(30, 41, 59)
    pdf.ln(5)

    # --- 2. Executive Summary (AI Insights) ---
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, "Executive Summary", 'B', 1)
    pdf.ln(2)
    pdf.set_font('helvetica', '', 10)
    summary = project_data.get('ai_summary', "The project is currently active. Performance analysis suggests maintaining focus on upcoming milestones.")
    pdf.multi_cell(0, 6, summary)
    pdf.ln(5)

    # --- 3. Key Performance Metrics ---
    # Draw two columns
    col_width = pdf.epw / 2
    
    # Left: Progress Stats
    start_y = pdf.get_y()
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(col_width, 8, "Progress Metrics", 'B', 1)
    pdf.set_font('helvetica', '', 10)
    pdf.cell(col_width, 7, f"Overall Completion: {project_data['progress']:.1f}%", 0, 1)
    pdf.cell(col_width, 7, f"Tasks Completed: {project_data['tasks_completed']} / {project_data['tasks_total']}", 0, 1)
    pdf.cell(col_width, 7, f"Remaining Hours: {project_data['remaining_hours']:.1f} hrs", 0, 1)
    
    # Right: Issue Stats
    pdf.set_xy(col_width + 15, start_y)
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(col_width - 5, 8, "Issue Tracking", 'B', 1)
    pdf.set_font('helvetica', '', 10)
    pdf.set_x(col_width + 15)
    pdf.cell(col_width - 5, 7, f"Open Issues: {project_data['issues_open']}", 0, 1)
    pdf.set_x(col_width + 15)
    pdf.set_text_color(220, 38, 38) # Red for critical
    pdf.cell(col_width - 5, 7, f"Critical Severity: {project_data['issues_critical']}", 0, 1)
    pdf.set_text_color(30, 41, 59)
    pdf.set_x(col_width + 15)
    pdf.cell(col_width - 5, 7, f"Resolved This Week: {project_data['issues_resolved_week']}", 0, 1)
    pdf.ln(10)

    # --- 4. Upcoming Milestones ---
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, "Key Upcoming Milestones", 'B', 1)
    pdf.ln(2)
    
    # Table Header
    pdf.set_fill_color(226, 232, 240) # Slate 200
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(100, 7, " Milestone / Task Name", 1, 0, 'L', True)
    pdf.cell(40, 7, " Due Date", 1, 0, 'L', True)
    pdf.cell(50, 7, " Status", 1, 1, 'L', True)
    
    pdf.set_font('helvetica', '', 9)
    milestones = project_data.get('milestones', [])
    if not milestones:
        pdf.cell(0, 7, "No upcoming milestones found.", 1, 1, 'C')
    else:
        for m in milestones:
            pdf.cell(100, 7, f" {m['name']}", 1, 0)
            pdf.cell(40, 7, f" {m['due_date']}", 1, 0)
            pdf.cell(50, 7, f" {m['status']}", 1, 1)
    pdf.ln(10)

    # --- 5. Resource Allocation ---
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, "Team Capacity & Assignment", 'B', 1)
    pdf.ln(2)
    
    # Simple list of resources and their load
    resources = project_data.get('resources', [])
    if not resources:
        pdf.set_font('helvetica', 'I', 10)
        pdf.cell(0, 7, "No resources assigned to this project.", 0, 1)
    else:
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(80, 7, " Resource Name", 1, 0, 'L', True)
        pdf.cell(60, 7, " Primary Role", 1, 0, 'L', True)
        pdf.cell(50, 7, " Active Tasks", 1, 1, 'L', True)
        
        pdf.set_font('helvetica', '', 9)
        for r in resources:
            pdf.cell(80, 7, f" {r['name']}", 1, 0)
            pdf.cell(60, 7, f" {r['role']}", 1, 0)
            pdf.cell(50, 7, f" {r['task_count']}", 1, 1)

    # Save to disk
    pdf.output(output_path)
    return output_path
