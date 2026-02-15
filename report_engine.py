from fpdf import FPDF
import datetime
import os

class ProjectReport(FPDF):
    def __init__(self, project_name=""):
        super().__init__()
        self.project_name = project_name
        
        # Register Unicode Font (Sarabun supports both Latin and Thai)
        font_path = os.path.join(os.getcwd(), "static/fonts/Sarabun-Regular.ttf")
        bold_font_path = os.path.join(os.getcwd(), "static/fonts/Sarabun-Bold.ttf")
        
        if os.path.exists(font_path):
            self.add_font("Sarabun", "", font_path)
            if os.path.exists(bold_font_path):
                self.add_font("Sarabun", "B", bold_font_path)
            self.font_family_main = "Sarabun"
        else:
            self.font_family_main = "helvetica" # Fallback

    def header(self):
        # Title
        self.set_font(self.font_family_main, 'B', 16)
        self.set_text_color(30, 41, 59) # Slate 800
        self.cell(0, 10, 'Executive Project Performance Report', 0, 1, 'C')
        
        # Project Name (Requested by user to be below the title line)
        if self.project_name:
            self.set_font(self.font_family_main, 'B', 14)
            self.set_text_color(51, 65, 85) # Slate 700
            self.cell(0, 8, self.project_name, 0, 1, 'C')
            
        self.set_font(self.font_family_main, 'I' if self.font_family_main == "helvetica" else "", 10)
        self.set_text_color(100)
        self.cell(0, 5, f'Generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.font_family_main, 'I' if self.font_family_main == "helvetica" else "", 8)
        self.set_text_color(100)
        self.cell(0, 10, f'Page {self.page_no()} | aiD_PM Smart Control Tower', 0, 0, 'C')

def generate_project_pdf(project_data: dict, output_path: str):
    # Initialize with project name for the header
    pdf = ProjectReport(project_name=project_data.get('name', ''))
    pdf.add_page()
    
    # --- 1. Project Info Summary ---
    pdf.set_fill_color(241, 245, 249) # Slate 100
    pdf.set_font(pdf.font_family_main, 'B', 11)
    pdf.cell(0, 8, " Project Overview", 0, 1, 'L', True)
    
    pdf.set_font(pdf.font_family_main, '', 9)
    pdf.cell(50, 6, f"Customer: {project_data.get('customer', 'N/A')}", 0, 0)
    pdf.cell(50, 6, f"Methodology: {project_data.get('methodology', 'Waterfall')}", 0, 0)
    status_text = "RECOVERY MODE" if project_data.get('is_recovery_mode') else "ACTIVE"
    pdf.set_text_color(220, 38, 38) if project_data.get('is_recovery_mode') else pdf.set_text_color(22, 163, 74)
    pdf.cell(0, 6, f"Status: {status_text}", 0, 1, 'R')
    pdf.set_text_color(30, 41, 59)
    pdf.ln(3)

    # --- 2. Executive Summary ---
    pdf.set_font(pdf.font_family_main, 'B', 11)
    pdf.cell(0, 8, "Executive Summary", 'B', 1)
    pdf.ln(2)
    pdf.set_font(pdf.font_family_main, '', 10)
    pdf.multi_cell(0, 5, project_data.get('ai_summary', "Analysis suggests nominal performance."))
    pdf.ln(4)

    # --- 3. Key Metrics (Side-by-Side) ---
    start_y = pdf.get_y()
    col_w = pdf.epw / 2 - 5
    
    # Left: Progress
    pdf.set_font(pdf.font_family_main, 'B', 10)
    pdf.cell(col_w, 7, "Execution Progress", 'B', 1)
    pdf.set_font(pdf.font_family_main, '', 9)
    pdf.cell(col_w, 6, f"Overall Completion: {project_data.get('progress', 0):.1f}%", 0, 1)
    pdf.cell(col_w, 6, f"Tasks: {project_data.get('tasks_completed', 0)} / {project_data.get('tasks_total', 0)} Done", 0, 1)
    
    # Right: Issues
    pdf.set_xy(pdf.epw/2 + 5, start_y)
    pdf.set_font(pdf.font_family_main, 'B', 10)
    pdf.cell(col_w, 7, "Risk & Issue Inventory", 'B', 1)
    pdf.set_font(pdf.font_family_main, '', 9)
    pdf.set_x(pdf.epw/2 + 5)
    pdf.cell(col_w, 6, f"Total Open Issues: {project_data.get('issues_open', 0)}", 0, 1)
    pdf.set_x(pdf.epw/2 + 5)
    pdf.set_text_color(220, 38, 38)
    pdf.cell(col_w, 6, f"Critical/High Severity: {project_data.get('issues_critical', 0)}", 0, 1)
    pdf.set_text_color(30, 41, 59)
    pdf.ln(8)

    # --- 4. Upcoming Milestones ---
    pdf.set_font(pdf.font_family_main, 'B', 11)
    pdf.cell(0, 8, "Key Upcoming Milestones", 'B', 1)
    pdf.ln(2)
    
    # Table Header
    pdf.set_fill_color(226, 232, 240) # Slate 200
    pdf.set_font(pdf.font_family_main, 'B', 9)
    pdf.cell(100, 7, " Milestone / Task Name", 1, 0, 'L', True)
    pdf.cell(40, 7, " Due Date", 1, 0, 'L', True)
    pdf.cell(50, 7, " Status", 1, 1, 'L', True)
    
    pdf.set_font(pdf.font_family_main, '', 9)
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
    pdf.set_font(pdf.font_family_main, 'B', 11)
    pdf.cell(0, 8, "Team Capacity & Assignment", 'B', 1)
    pdf.ln(2)
    
    resources = project_data.get('resources', [])
    if resources:
        pdf.set_fill_color(226, 232, 240)
        pdf.set_font(pdf.font_family_main, 'B', 9)
        pdf.cell(80, 7, " Resource Name", 1, 0, 'L', True)
        pdf.cell(60, 7, " Role", 1, 0, 'L', True)
        pdf.cell(50, 7, " Active Tasks", 1, 1, 'L', True)
        pdf.set_font(pdf.font_family_main, '', 9)
        for r in resources:
            pdf.cell(80, 7, f" {r['name']}", 1, 0)
            pdf.cell(60, 7, f" {r['role']}", 1, 0)
            pdf.cell(50, 7, f" {r['task_count']}", 1, 1)
    else:
        pdf.cell(0, 7, "No team members assigned.", 0, 1)

    # Save to disk
    pdf.output(output_path)
    return output_path

def generate_onsite_consensus_pdf(report_data: dict, output_path: str):
    """Generate Onsite Consensus Report PDF matching the exact design provided"""
    pdf = FPDF()
    
    # Register Unicode Font (Sarabun supports both Latin and Thai)
    font_path = os.path.join(os.getcwd(), "static/fonts/Sarabun-Regular.ttf")
    bold_font_path = os.path.join(os.getcwd(), "static/fonts/Sarabun-Bold.ttf")
    
    if os.path.exists(font_path):
        pdf.add_font("Sarabun", "", font_path)
        if os.path.exists(bold_font_path):
            pdf.add_font("Sarabun", "B", bold_font_path)
        font_family = "Sarabun"
    else:
        font_family = "helvetica"

    pdf.add_page()
    
    # --- Header (exactly as in image) ---
    pdf.set_y(25)
    pdf.set_font(font_family, 'B', 26)
    pdf.set_text_color(44, 62, 80)  # Dark blue-gray
    pdf.cell(0, 12, 'Onsite Consensus Report', 0, 1, 'C')
    
    # Project name subtitle
    pdf.set_font(font_family, '', 13)
    pdf.set_text_color(127, 140, 141)  # Medium gray
    pdf.cell(0, 7, report_data.get('project_name', 'N/A'), 0, 1, 'C')
    
    # Date
    pdf.set_font(font_family, '', 11)
    report_date = report_data.get('report_date', datetime.date.today())
    pdf.cell(0, 6, report_date.strftime('%B %d, %Y'), 0, 1, 'C')
    
    pdf.ln(3)
    # Blue horizontal line
    pdf.set_draw_color(52, 152, 219)
    pdf.set_line_width(1.0)
    pdf.line(46, pdf.get_y(), pdf.epw - 36, pdf.get_y())
    pdf.ln(15)
    
    # --- Customer & Responder (side by side, NO background boxes) ---
    start_y = pdf.get_y()
    col_width = pdf.epw / 2 - 5
    
    customer_profile = report_data.get('customer_profile')
    responder_profile = report_data.get('responder_profile')
    
    # Left side - Customer
    pdf.set_xy(10, start_y)
    pdf.set_font(font_family, 'B', 11)
    pdf.set_text_color(85, 85, 85)
    pdf.cell(col_width, 7, "Customer", 0, 1)
    
    if customer_profile:
        pdf.set_x(10)
        pdf.set_font(font_family, 'B', 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(col_width, 7, customer_profile.company_name or "N/A", 0, 1)
        
        pdf.set_x(10)
        pdf.set_font(font_family, '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(col_width, 5, customer_profile.address or "")
    
    # Right side - Responder
    pdf.set_xy(pdf.epw/2 + 15, start_y)
    pdf.set_font(font_family, 'B', 11)
    pdf.set_text_color(85, 85, 85)
    pdf.cell(col_width, 7, "Responder", 0, 1)
    
    if responder_profile:
        pdf.set_x(pdf.epw/2 + 15)
        pdf.set_font(font_family, 'B', 12)
        pdf.set_text_color(44, 62, 80)
        pdf.cell(col_width, 7, responder_profile.company_name or "N/A", 0, 1)
        
        pdf.set_x(pdf.epw/2 + 15)
        pdf.set_font(font_family, '', 10)
        pdf.set_text_color(100, 100, 100)
        pdf.multi_cell(col_width, 5, responder_profile.address or "")
    
    pdf.ln(20)
    
    # --- Observations ---
    pdf.set_font(font_family, 'B', 16)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, "Observations", 0, 1)
    
    # Thin line below
    pdf.set_draw_color(200, 200, 200)
    pdf.set_line_width(0.3)
    pdf.line(10, pdf.get_y(), pdf.epw + 10, pdf.get_y())
    pdf.ln(8)
    
    # Observation text in light gray box
    pdf.set_fill_color(248, 250, 252)
    obs_text = report_data.get('description', 'TEST')
    
    pdf.set_font(font_family, '', 11)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 7, obs_text, 0, 'L', fill=True)
    
    pdf.ln(25)
    
    # --- Signature Section (in light gray box) ---
    sig_box_y = pdf.get_y()
    sig_box_height = 60
    
    pdf.set_fill_color(248, 250, 252)
    pdf.rect(10, sig_box_y, pdf.epw, sig_box_height, 'F')
    
    col_w = pdf.epw / 2
    
    # Headers
    pdf.set_xy(10, sig_box_y + 12)
    pdf.set_font(font_family, 'B', 12)
    pdf.set_text_color(85, 85, 85)
    pdf.cell(col_w, 7, "Customer Representative", 0, 0, 'C')
    pdf.cell(col_w, 7, "Responder Representative", 0, 1, 'C')
    
    # Signature lines
    pdf.ln(12)
    line_y = pdf.get_y()
    line_w = 90
    
    pdf.set_draw_color(60, 60, 60)
    pdf.set_line_width(0.4)
    pdf.line(10 + (col_w - line_w)/2, line_y, 10 + (col_w + line_w)/2, line_y)
    pdf.line(10 + col_w + (col_w - line_w)/2, line_y, 10 + col_w + (col_w + line_w)/2, line_y)
    
    # "Signature" label
    pdf.set_y(line_y + 3)
    pdf.set_font(font_family, '', 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(col_w, 6, "Signature", 0, 0, 'C')
    pdf.cell(col_w, 6, "Signature", 0, 1, 'C')
    
    # Names (bold)
    pdf.ln(1)
    pdf.set_font(font_family, 'B', 11)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(col_w, 6, report_data.get('customer_signature_name', ''), 0, 0, 'C')
    pdf.cell(col_w, 6, report_data.get('responder_signature_name', ''), 0, 1, 'C')
    
    # Save to disk
    pdf.output(output_path)
    return output_path

