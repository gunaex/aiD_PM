# Export Directory Fix - Summary

## Issue
When trying to export reports (Weekly or Daily), the application threw an error:
```
{"detail":"Error generating report: [Errno 2] No such file or directory: 'exports/WeeklyReport_Project_1_20260204_105815.xlsx'"}
```

## Root Cause
The `exports/` directory didn't exist, and the code attempted to write files directly without creating the directory first. This is a common cross-platform issue that can occur on fresh installations.

## Solution Applied

### 1. Fixed `main.py` Export Functions
Added automatic directory creation in both export endpoints:

**Lines 1869-1882** (Weekly Report):
```python
@app.get("/export/weekly/{project_id}")
def export_weekly_report_endpoint(project_id: int, db: Session = Depends(get_db)):
    """ส่งออก Weekly Report เป็น Excel"""
    template_path = "templates_excel/WeeklyReport_PH(PU).xlsx"
    output_path = f"exports/WeeklyReport_Project_{project_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)  # ← NEW LINE
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    try:
        result_path = excel_engine.export_weekly_report(db, project_id, template_path, output_path)
        return FileResponse(result_path, filename=os.path.basename(result_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
```

**Lines 1884-1897** (Daily Progress):
```python
@app.get("/export/daily/{project_id}")
def export_daily_progress_endpoint(project_id: int, db: Session = Depends(get_db)):
    """ส่งออก Daily Progress Report เป็น Excel"""
    template_path = "templates_excel/Daily_Progress_PH(PU).xls"
    output_path = f"exports/DailyProgress_Project_{project_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.xls"
    
    # Create exports directory if it doesn't exist
    os.makedirs("exports", exist_ok=True)  # ← NEW LINE
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template file not found")
    
    try:
        result_path = excel_engine.export_daily_progress(db, project_id, template_path, output_path)
        return FileResponse(result_path, filename=os.path.basename(result_path))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")
```

### 2. Updated `.gitignore`
Added `exports/` to the output files section to prevent generated reports from being committed to version control:

```gitignore
# Output files
output/
exports/  # ← NEW LINE
*.xls
*.xlsx
!templates_excel/*.xls
!templates_excel/*.xlsx
```

## How to Apply the Fix

Since your server is currently running, you need to restart it:

1. **Stop the current server**: Press `Ctrl+C` in the terminal running `./run.sh`
2. **Restart the server**: Run `./run.sh` again
3. **Test the export**: Try exporting a report again

The `exports/` directory will now be created automatically when you export your first report.

## Why This Happened

This is a **cross-platform compatibility issue**:
- On Windows, some applications might create directories automatically
- On macOS/Linux, Python's file operations are more strict and require explicit directory creation
- The `os.makedirs(path, exist_ok=True)` function is the cross-platform solution that:
  - Creates the directory if it doesn't exist
  - Doesn't throw an error if it already exists (`exist_ok=True`)

## Files Modified
- ✅ `/Users/macbook/Documents/git_macbook/aiD_PM/aiD_PM/main.py` (2 functions updated)
- ✅ `/Users/macbook/Documents/git_macbook/aiD_PM/aiD_PM/.gitignore` (1 line added)
