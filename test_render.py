from fastapi.templating import Jinja2Templates
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

engine = create_engine('sqlite:///pm_system.db')
Session = sessionmaker(bind=engine)
db = Session()

templates = Jinja2Templates(directory="templates")

projects = db.query(models.Project).all()
phases = db.query(models.ProjectPhase).all()

starts = [p.planned_start for p in phases if p.planned_start]
ends   = [p.planned_end   for p in phases if p.planned_end]
timeline_start = (min(starts) - datetime.timedelta(days=7)) if starts else datetime.date.today()
timeline_end   = (max(ends)   + datetime.timedelta(days=7)) if ends   else timeline_start + datetime.timedelta(days=180)

def get_timeline_months(start_date, end_date):
    months = []
    total_days = (end_date - start_date).days
    if total_days <= 0: return []
    curr = start_date
    while curr < end_date:
        m_name = curr.strftime("%b")
        m_year = curr.year
        if curr.month == 12:
            next_m_start = datetime.date(curr.year + 1, 1, 1)
        else:
            next_m_start = datetime.date(curr.year, curr.month + 1, 1)
        segment_end = min(next_m_start, end_date)
        days_in_segment = (segment_end - curr).days
        if days_in_segment > 0:
            months.append({
                "name": m_name,
                "year": m_year,
                "width_pct": (days_in_segment / total_days) * 100,
                "days": days_in_segment
            })
        curr = segment_end
    return months

months_data = get_timeline_months(timeline_start, timeline_end)

try:
    res = templates.get_template("phases.html").render({
        "request": {},
        "projects": projects,
        "phases": phases,
        "selected_project_id": None,
        "timeline_start": timeline_start,
        "timeline_end": timeline_end,
        "months_data": months_data,
    })
    print("SUCCESS")
except Exception as e:
    import traceback
    traceback.print_exc()

