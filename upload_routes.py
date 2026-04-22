import csv
from io import StringIO
from fastapi.responses import StreamingResponse
from fastapi import UploadFile, File

@app.get("/functions/download_template")
async def download_function_template():
    """Download CSV template for bulk upload"""
    csv_data = [
        ["function_name", "category", "priority", "estimated_hours", "description"],
        ["User Login", "Function", "high", "5.0", "Allow users to login via email and password"],
        ["Export Report", "Requirement", "medium", "8.0", "Export data to Excel"],
    ]
    
    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(csv_data)
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=function_template.csv"}
    )

@app.post("/functions/upload")
async def upload_functions(
    project_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Bulk upload functions from CSV"""
    content = await file.read()
    decoded = content.decode("utf-8")
    csv_reader = csv.DictReader(StringIO(decoded))
    
    import random
    
    for row in csv_reader:
        function_name = row.get("function_name", "").strip()
        if not function_name:
            continue
            
        category = row.get("category", "Function").strip()
        priority = row.get("priority", "medium").strip()
        
        try:
            estimated_hours = float(row.get("estimated_hours", 0))
        except ValueError:
            estimated_hours = 0.0
            
        description = row.get("description", "").strip()
        
        function_code = generate_function_code(project_id, db)
        
        func = models.ProjectFunction(
            project_id=project_id,
            function_code=function_code,
            function_name=function_name,
            category=category,
            priority=priority,
            estimated_hours=estimated_hours,
            description=description,
            status="not_started"
        )
        db.add(func)
        
    db.commit()
    return RedirectResponse(url=f"/functions?project_id={project_id}", status_code=303)
