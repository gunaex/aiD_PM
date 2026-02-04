from fpdf import FPDF
import datetime
import os

class ProjectReport(FPDF):
    def __init__(self, project_name=""):
        super().__init__()
        self.project_name = project_name

    def header(self):
        # Title
        self.set_font('helvetica', 'B', 16)
        self.set_text_color(30, 41, 59) # Slate 800
        self.cell(0, 10, 'Executive Project Performance Report', 0, 1, 'C')
        
        # Project Name (Requested by user to be below the title line)
        if self.project_name:
            self.set_font('helvetica', 'B', 14)
            self.set_text_color(51, 65, 85) # Slate 700
            self.cell(0, 8, self.project_name, 0, 1, 'C')
            
        self.set_font('helvetica', 'I', 10)
        self.set_text_color(100)
        self.cell(0, 5, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(100)
        self.cell(0, 10, f'Page {self.page_no()} | aiD_PM Smart Control Tower', 0, 0, 'C')

def generate_project_pdf(project_data: dict, output_path: str):
    # Initialize with project name for the header
    pdf = ProjectReport(project_name=project_data.get('name', ''))
    pdf.add_page()
    
    # --- 1. Project Info Summary ---
    pdf.set_fill_color(241, 245, 249) # Slate 100
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, " Project Overview", 0, 1, 'L', True)
    
    pdf.set_font('helvetica', '', 9)
    pdf.cell(50, 6, f"Customer: {project_data.get('customer', 'N/A')}", 0, 0)
    pdf.cell(50, 6, f"Methodology: {project_data.get('methodology', 'Waterfall')}", 0, 0)
    status_text = "RECOVERY MODE" if project_data.get('is_recovery_mode') else "ACTIVE"
    pdf.set_text_color(220, 38, 38) if project_data.get('is_recovery_mode') else pdf.set_text_color(22, 163, 74)
    pdf.cell(0, 6, f"Status: {status_text}", 0, 1, 'R')
    pdf.set_text_color(30, 41, 59)
    pdf.ln(3)

    # --- 2. Executive Summary ---
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, "Executive Summary", 'B', 1)
    pdf.ln(2)
    pdf.set_font('helvetica', '', 10)
    pdf.multi_cell(0, 5, project_data.get('ai_summary', "Analysis suggests nominal performance."))
    pdf.ln(4)

    # --- 3. Key Metrics (Side-by-Side) ---
    start_y = pdf.get_y()
    col_w = pdf.epw / 2 - 5
    
    # Left: Progress
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(col_w, 7, "Execution Progress", 'B', 1)
    pdf.set_font('helvetica', '', 9)
    pdf.cell(col_w, 6, f"Overall Completion: {project_data.get('progress', 0):.1f}%", 0, 1)
    pdf.cell(col_w, 6, f"Tasks: {project_data.get('tasks_completed', 0)} / {project_data.get('tasks_total', 0)} Done", 0, 1)
    
    # Right: Issues
    pdf.set_xy(pdf.epw/2 + 5, start_y)
    pdf.set_font('helvetica', 'B', 10)
    pdf.cell(col_w, 7, "Risk & Issue Inventory", 'B', 1)
    pdf.set_font('helvetica', '', 9)
    pdf.set_x(pdf.epw/2 + 5)
    pdf.cell(col_w, 6, f"Total Open Issues: {project_data.get('issues_open', 0)}", 0, 1)
    pdf.set_x(pdf.epw/2 + 5)
    pdf.set_text_color(220, 38, 38)
    pdf.cell(col_w, 6, f"Critical/High Severity: {project_data.get('issues_critical', 0)}", 0, 1)
    pdf.set_text_color(30, 41, 59)
    pdf.ln(8)

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

    # --- 5. Team Capacity & Assignment ---
    pdf.set_font('helvetica', 'B', 11)
    pdf.cell(0, 8, "Team Capacity & Assignment", 'B', 1)
    pdf.ln(2)
    
    resources = project_data.get('resources', [])
    if resources:
        pdf.set_fill_color(226, 232, 240)
        pdf.set_font('helvetica', 'B', 9)
        pdf.cell(80, 7, " Resource Name", 1, 0, 'L', True)
        pdf.cell(60, 7, " Role", 1, 0, 'L', True)
        pdf.cell(50, 7, " Active Tasks", 1, 1, 'L', True)
        pdf.set_font('helvetica', '', 9)
        for r in resources:
            pdf.cell(80, 7, f" {r['name']}", 1, 0)
            pdf.cell(60, 7, f" {r['role']}", 1, 0)
            pdf.cell(50, 7, f" {r['task_count']}", 1, 1)
    else:
        pdf.cell(0, 7, "No team members assigned.", 0, 1)

    # Save to disk
    pdf.output(output_path)
    return output_path
