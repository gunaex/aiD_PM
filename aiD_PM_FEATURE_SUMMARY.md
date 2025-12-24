# 🚀 aiD_PM - Smart PM Control Tower

## **Overview**

**aiD_PM** (AI-powered Project Management) is an **intelligent, enterprise-grade project management system** designed for modern teams. Built with **FastAPI, SQLite, and AI-powered features**, it combines traditional PM tools with cutting-edge artificial intelligence to make project management **smarter, faster, and more efficient**.

---

## 🎯 **Core Philosophy**

```
Traditional PM Tools → Reactive (you manage the data)
aiD_PM → Proactive (AI helps you make decisions)
```

**Key Differentiators:**
- ✅ **AI-First Design**: Built-in AI assistant for smart recommendations
- ✅ **Local-First**: Your data stays on your machine (privacy-first)
- ✅ **Zero Learning Curve**: Intuitive UI that feels natural
- ✅ **Enterprise Features**: Issue tracking, phases, multi-resource assignment
- ✅ **Cross-Platform Ready**: Web → Mobile (Android/iOS) → Desktop

---

## 📊 **Complete Feature List** (18+ Major Features)

### **1. 🏠 Smart Dashboard**
**The Command Center for Your Projects**

- **Real-time Project Health Metrics**
  - Overall progress across all projects
  - Average completion rate
  - Active tasks vs completed tasks
  
- **At-a-Glance Insights**
  - Project cards with visual progress bars
  - Color-coded status indicators
  - Quick access to all major features

- **Emergency Recovery Mode**
  - One-click toggle for high-risk projects
  - Visual alerts for critical tasks
  - Automatic risk scoring

**Use Case:** *Start your day with a complete overview of all projects in 5 seconds*

---

### **2. 👥 Resource DNA Profiles**
**Know Your Team's Superpowers**

- **Comprehensive Team Member Profiles**
  - Full name, nickname, position
  - Custom skill matrix (JSON-based)
  - Speed score (1-10): How fast they work
  - Quality score (1-10): How good the output is
  
- **Smart Skill Tracking**
  - Multi-skill support (e.g., Python: 9, SQL: 7, React: 8)
  - Visual skill representations
  - Active/Inactive status management

- **AI-Ready Data**
  - Powers the AI resource recommendation engine
  - Historical performance tracking
  - Workload balancing

**Use Case:** *"Who's the best person for a Python API task?" → AI knows instantly*

---

### **3. 📋 Project Management**
**Full Project Lifecycle Control**

- **Project Creation & Configuration**
  - Project name, customer, methodology (Waterfall/Scrum/Kanban)
  - Budget tracking (masked for privacy)
  - Recovery mode toggle
  - Creation timestamp

- **Project Phases**
  - Industry-standard phases (UR, DR, PU/PT, IFT, SIT, BCT, IP, UAT)
  - Custom phase creation
  - Order management
  - Phase-based issue tracking

- **Project Details View**
  - Comprehensive project overview
  - Task list with progress
  - Weekly snapshot history
  - Quick actions (Edit, Add Task, View Gantt, Take Snapshot)

**Use Case:** *Manage entire project from inception to delivery*

---

### **4. ✅ Advanced Task Management**
**Tasks That Know Themselves**

- **Rich Task Properties**
  - Task name, type (Dev/Admin/Procurement/Fix)
  - Weight score (for value-based tracking)
  - Planned start & end dates
  - Actual progress (0-100%)
  - AI risk score (hidden intelligence)

- **Multi-Resource Assignment** ⭐
  - Assign multiple team members to a single task
  - Checkbox-based selection
  - Workload tracking across assignments
  
- **Smart Task Operations**
  - Create, Edit, Delete
  - Progress slider with auto-save
  - Activity logging (who changed what, when)
  - Comment system

- **Value-Based Progress Tracking**
  - Calculate project progress based on task weights
  - More important tasks = more weight = better accuracy

**Use Case:** *Complex tasks require multiple people → No problem!*

---

### **5. 🤖 AI Assistant** ⭐ **NEW!**
**Your Intelligent PM Copilot**

#### **Feature 5a: Smart Task Breakdown**
- **Automatic Task Decomposition**
  - Input: 1 complex task (e.g., "Build REST API")
  - Output: 5-7 actionable subtasks with timelines
  
- **Context-Aware Breakdown**
  - Different templates for Dev, Fix, Admin, Procurement
  - Keyword detection (API → 6 API-specific subtasks)
  - UI/Frontend → UI-specific subtasks
  - Database → DB-specific subtasks

- **Smart Scheduling**
  - Auto-assign dates to subtasks
  - Skip weekends option
  - Dependency-aware sequencing
  - Realistic duration estimates

**Example:**
```
Input: "Build User Authentication API"
Output:
1. API Design & Specification (1 day) - Jan 1-2
2. Database Schema Design (1 day) - Jan 3
3. Endpoint Implementation (3 days) - Jan 4-6
4. Authentication & Authorization (2 days) - Jan 9-10
5. API Testing (2 days) - Jan 11-12
6. API Documentation (1 day) - Jan 13
Total: 10 days
```

#### **Feature 5b: AI Resource Matching**
- **Intelligent Resource Recommendations**
  - Match resources to tasks based on:
    - Skill compatibility (0-50 points)
    - Speed score (0-20 points)
    - Quality score (0-20 points)
    - Current workload (0-10 points)
  
- **Top N Recommendations**
  - Returns best 3-5 matches
  - Explains WHY each person is recommended
  - Shows current workload
  - Match percentage (0-100%)

**Example:**
```
Task: Python Backend Development

Recommendations:
1. John Doe (95% match)
   - Python: 9/10, FastAPI: 8/10
   - Speed: 8/10, Quality: 9/10
   - Current tasks: 2
   
2. Jane Smith (87% match)
   - Python: 10/10
   - Speed: 9/10, Quality: 7/10
   - Current tasks: 5
```

#### **Feature 5c: Risk Prediction**
- **Proactive Risk Analysis**
  - Schedule risk (overdue, deadline approaching)
  - Progress risk (behind schedule)
  - Resource risk (no one assigned)
  
- **Risk Scoring (0-100)**
  - Critical (70+): Immediate action required
  - High (50-70): Monitor closely
  - Medium (30-50): Watch for changes
  - Low (<30): On track

- **Actionable Recommendations**
  - "Consider extending deadline or adding resources"
  - "Assign qualified resource immediately"
  - "Increase task priority and check blockers"

#### **Feature 5d: Project Insights**
- **AI-Generated Project Health Reports**
  - Completion rate
  - Task breakdown (completed/in progress/not started)
  - High-risk task count
  - Health status (Excellent/Good/Fair/At Risk)
  
- **Smart Recommendations**
  - "Too many tasks in progress - focus on completion"
  - "Many tasks not started - consider sprint planning"
  - "Project is on track - keep up the good work!"

**Use Case:** *AI becomes your PM assistant, giving you insights you'd miss*

---

### **6. 📅 Interactive Calendar Grid** ⭐ **NEW!**
**Your Tasks on a Real Calendar**

- **Month View with Full Interactivity**
  - Visual calendar grid (7 days × 5 weeks)
  - Color-coded days:
    - Blue: Tasks scheduled
    - Red: Deadlines
    - Blue border: Today
  
- **Event Dots**
  - Green: Completed tasks
  - Yellow: In progress
  - Gray: Not started
  - Shows up to 5 events per day

- **Smart Navigation**
  - Previous/Next month buttons
  - Quick jump to any month (Jan-Dec)
  - Year navigation
  - Filter by project

- **Click to View Details**
  - Modal popup shows all tasks for that day
  - Task details (name, type, progress, dates)
  - Direct link to task edit
  - Deadline highlighting

**Use Case:** *"What's happening this week?" → See at a glance*

---

### **7. 📊 Kanban Board**
**Visual Workflow Management**

- **Drag-and-Drop Interface**
  - 4 columns: To Do, In Progress, Review, Done
  - Smooth drag-and-drop
  - Auto-save on drop

- **Auto-Progress Update**
  - Drop in "In Progress" → 50% progress
  - Drop in "Review" → 80% progress
  - Drop in "Done" → 100% progress

- **Task Cards**
  - Task name, type, weight
  - Assigned resources
  - Progress bar
  - Color-coded by type

**Use Case:** *Perfect for Agile teams and daily standups*

---

### **8. 📈 Gantt Chart**
**Timeline Visualization Powerhouse**

- **Multiple Views**
  - Daily view (24-hour timeline)
  - Weekly view (7-day timeline)
  - Monthly view (30-day timeline)
  - Overall view (entire project)

- **Interactive Task Bars**
  - Color-coded by progress
  - Hover to see details
  - Visual duration representation
  - Today marker

- **Smart Filtering**
  - Filter by project
  - Switch views instantly
  - Responsive timeline scaling

**Use Case:** *Executive presentations and timeline planning*

---

### **9. 👔 Team Workload View**
**Balance Your Team Capacity**

- **Visual Workload Distribution**
  - Bar charts for each resource
  - Color-coded capacity:
    - Green: Light load (≤3 tasks)
    - Yellow: Moderate load (4-5 tasks)
    - Red: Heavy load (6+ tasks)

- **Task Breakdown**
  - Not Started (gray)
  - In Progress (blue)
  - Completed (green)
  - Total task count

- **Quick Assignment**
  - See who's available
  - Identify overloaded members
  - Balance workload proactively

**Use Case:** *"Who can take on this urgent task?" → Instant answer*

---

### **10. 🐛 Enterprise Issue Tracker**
**Bug & Issue Management**

- **Comprehensive Issue Properties**
  - Title, description, status
  - Severity (Critical/High/Medium/Low)
  - Priority (High/Medium/Low)
  - Phase assignment
  - Due date

- **Multi-Resource Assignment**
  - Multiple people can work on an issue
  - PIC (Person In Charge) tracking

- **Issue Workflow**
  - Status: Open → In Progress → Pending → Blocked → Closed
  - Status change logging
  - Automatic activity tracking

- **Rich Comments System**
  - Regular comments
  - Notes (internal)
  - Resolutions (final fix description)
  - Timestamp tracking

- **File Attachments** (Database ready)
  - Upload screenshots, logs, docs
  - Version tracking
  - File metadata

**Use Case:** *From bug report to resolution in one place*

---

### **11. 📐 Phase Management**
**Structure Your SDLC**

- **Standard Phases**
  - UR (User Requirements)
  - DR (Design Requirements)
  - PU/PT (Prototyping)
  - IFT (Internal Feature Testing)
  - SIT (System Integration Testing)
  - BCT (Business Case Testing)
  - IP (In Production)
  - UAT (User Acceptance Testing)

- **Custom Phase Creation**
  - Add your own phases
  - Order management
  - Per-project customization

- **Phase-Based Organization**
  - Link issues to phases
  - Track progress per phase
  - Phase completion metrics

**Use Case:** *Organize projects by waterfall/agile phases*

---

### **12. 📊 Weekly Snapshots & PB Curves**
**Progress vs Baseline Tracking**

- **Auto-Aggregation**
  - Daily progress → Weekly snapshots
  - Accurate trend analysis
  - ISO week number tracking

- **PB Curve Data**
  - Plan Accumulated (baseline)
  - Actual Accumulated (progress)
  - Visual comparison

- **Excel Export**
  - Populate WeeklyReport_PH(PU).xlsx
  - "PB Curve" sheet auto-fill
  - Ready for executive reports

**Use Case:** *Professional weekly reports in seconds*

---

### **13. 📝 Activity Log & Audit Trail**
**Complete History of Everything**

- **Automatic Event Logging**
  - Task created/updated/deleted
  - Progress changes
  - Comment additions
  - Issue status changes
  - Resource assignments

- **Rich Activity Details**
  - Who did it (user_name)
  - What changed (description)
  - When it happened (timestamp)
  - Associated task/issue

- **Activity Timeline**
  - View all activities for a task
  - View all activities for an issue
  - Project-wide activity feed (future)

**Use Case:** *"Who changed the deadline?" → Check activity log*

---

### **14. 💬 Comment System**
**Collaborate on Tasks & Issues**

- **Task Comments**
  - Add notes, updates, discussions
  - User attribution
  - Timestamp tracking
  - Chronological display

- **Issue Comments**
  - Three types:
    - Comments (general discussion)
    - Notes (internal, team-only)
    - Resolution (final fix description)
  
- **Real-time Updates**
  - Auto-refresh on new comments
  - Visual separation by type

**Use Case:** *Async communication without email chaos*

---

### **15. 📤 Database Backup & Restore**
**Your Data, Your Control**

- **One-Click Backup**
  - Download entire SQLite database
  - Timestamped filename
  - Single file = entire system

- **One-Click Restore**
  - Upload backup file
  - Replace current database
  - Cross-device compatibility

- **Use Cases**
  - Transfer data between PC and mobile
  - Share project state with team
  - Disaster recovery
  - Version control

**Use Case:** *Work on PC, sync to phone, continue on tablet*

---

### **16. ⚙️ Settings & Configuration**
**Customize Your Experience**

- **System Configuration**
  - UI preferences
  - Default values
  - Theme selection (light/dark) - coming soon

- **Global Settings**
  - Default task duration
  - Skip weekends in scheduling
  - Emergency mode threshold

**Use Case:** *Make aiD_PM work YOUR way*

---

### **17. 📱 Cross-Platform Architecture**
**Built for Mobility**

- **Current: Web Application**
  - FastAPI backend
  - Responsive HTML/CSS/JS
  - Works on any browser

- **Future: Mobile Apps**
  - Flutter framework
  - Native Android & iOS
  - Same SQLite database
  - Offline-first design

- **Future: Desktop Apps**
  - macOS, Windows, Linux
  - Native performance
  - System tray integration

**Use Case:** *One codebase, every device*

---

### **18. 🎨 Modern UI/UX**
**Beautiful & Functional**

- **Tailwind CSS Design**
  - Clean, professional look
  - Responsive layouts
  - Color-coded everything

- **75% UI Zoom**
  - More content on screen
  - Optimized density
  - Comfortable viewing

- **Visual Hierarchy**
  - Cards, borders, shadows
  - Clear CTAs (Call-to-Actions)
  - Intuitive navigation

- **Sidebar Navigation**
  - Quick access to all features
  - Active state highlighting
  - Collapsible (future)

**Use Case:** *Looks good = feels good = works good*

---

## 🔥 **What Makes aiD_PM Different?**

### **vs Jira**
| Feature | Jira | aiD_PM |
|---------|------|--------|
| AI Assistant | ❌ | ✅ |
| Local-First | ❌ | ✅ |
| Setup Time | Hours | Minutes |
| Cost | $$$$ | Free |
| Resource DNA | ❌ | ✅ |
| Mobile App | ✅ | Coming Soon |

### **vs Monday.com**
| Feature | Monday | aiD_PM |
|---------|--------|--------|
| AI Task Breakdown | ❌ | ✅ |
| Privacy | Cloud | Local |
| Customization | Limited | Unlimited |
| Risk Prediction | ❌ | ✅ |
| Offline Mode | ❌ | ✅ (coming) |

### **vs Trello**
| Feature | Trello | aiD_PM |
|---------|--------|--------|
| Kanban | ✅ | ✅ |
| Gantt Chart | Add-on | Built-in |
| AI Features | ❌ | ✅ |
| Issue Tracker | Basic | Enterprise |
| Phases | ❌ | ✅ |

---

## 🏗️ **Technical Architecture**

### **Backend**
```
FastAPI (Python 3.11+)
├── High performance async framework
├── Auto-generated API docs (OpenAPI)
├── Type hints for reliability
└── Easy to extend

SQLAlchemy ORM
├── 12 database tables
├── Relationships & constraints
├── Migration-ready
└── SQLite (portable) or PostgreSQL (production)
```

### **Frontend**
```
HTML5 + TailwindCSS + Vanilla JS
├── No heavy frameworks (fast load)
├── Responsive design
├── Progressive enhancement
└── Future: React/Vue for SPA
```

### **AI Layer**
```
ai_assistant.py
├── Rule-based algorithms (no API needed)
├── OpenAI GPT-4 support (optional)
├── Local ML models (future)
└── Pluggable architecture
```

### **Database Schema**
```
12 Core Tables:
1. resources          (team members)
2. projects           (project info)
3. tasks              (task details)
4. task_resources     (multi-assign)
5. weekly_snapshots   (PB curve data)
6. project_phases     (SDLC phases)
7. issues             (bug tracking)
8. issue_resources    (multi-assign)
9. issue_comments     (discussions)
10. issue_attachments (files)
11. activity_logs     (audit trail)
12. comments          (task comments)
```

---

## 🚀 **Getting Started**

### **Quick Start (3 Steps)**

```bash
# 1. Clone & Setup
cd aiD_PM
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 2. Initialize Database
python init_db_complete.py

# 3. Run Server
uvicorn main:app --reload

# 4. Open Browser
http://localhost:8000
```

**First 5 Minutes:**
1. Create a project
2. Add team members (Resources)
3. Create tasks
4. Try AI Assistant
5. View Gantt Chart

---

## 📈 **Roadmap**

### **Phase 1: Foundation** ✅ COMPLETE
- Core PM features
- Database design
- Basic UI

### **Phase 2: Intelligence** ✅ COMPLETE
- AI Assistant
- Risk prediction
- Smart recommendations

### **Phase 3: Collaboration** (Current)
- [ ] Email notifications
- [ ] Real-time updates (WebSocket)
- [ ] User authentication
- [ ] Role-based access

### **Phase 4: Mobile** (Next)
- [ ] Flutter mobile app
- [ ] Offline sync
- [ ] Push notifications

### **Phase 5: Enterprise** (Future)
- [ ] Multi-tenant
- [ ] SSO integration
- [ ] Advanced analytics
- [ ] Custom workflows

---

## 💡 **Use Cases**

### **For Solo Developers**
- Organize your side projects
- Track tasks and progress
- Learn AI-powered PM

### **For Small Teams (2-10)**
- Coordinate work
- Balance workload
- Track bugs and features

### **For Agencies**
- Manage client projects
- Resource allocation
- Professional reports

### **For Enterprise**
- Replace expensive tools
- Keep data private
- Customize workflows

---

## 🎓 **Learning Resources**

### **Documentation**
- `README.md` - Overview
- `QUICKSTART.md` - Getting started
- `COPILOT_CONTEXT.md` - AI prompts
- `CROSS_PLATFORM_GUIDE.md` - Mobile development
- `RECOMMENDED_FEATURES.md` - Future features

### **Code Structure**
```
aiD_PM/
├── main.py              (FastAPI app)
├── models.py            (Database models)
├── database.py          (DB connection)
├── ai_assistant.py      (AI features)
├── excel_engine.py      (Excel export)
├── templates/           (HTML pages)
│   ├── dashboard.html
│   ├── ai_assistant.html
│   ├── kanban.html
│   ├── gantt.html
│   └── ...
└── static/              (CSS, JS, images)
```

---

## 🤝 **Contributing**

**Ways to Contribute:**
1. **Use it** - The best feedback is real usage
2. **Report bugs** - Open issues
3. **Suggest features** - What's missing?
4. **Code** - Pull requests welcome
5. **Spread the word** - Share with friends!

---

## 📊 **System Stats**

```
Total Features:        18+
Lines of Code:         ~15,000
Database Tables:       12
HTML Pages:            15+
API Endpoints:         30+
AI Capabilities:       4
Supported Platforms:   Web (now), Mobile (soon), Desktop (soon)
License:               Open Source (MIT)
```

---

## 🎯 **Key Takeaways**

✅ **aiD_PM is NOT just another PM tool**
- It's AI-powered from the ground up
- It respects your privacy (local-first)
- It's built for the future (cross-platform ready)

✅ **Perfect for teams who want:**
- Intelligence built-in, not bolted-on
- Full control over their data
- Modern UX without the complexity
- Enterprise features without enterprise cost

✅ **Growing fast:**
- Active development
- AI features expanding
- Mobile app coming soon
- Community-driven roadmap

---

## 📞 **Get Started Today**

```
🌐 Web:     http://localhost:8000
📧 Email:   [Your Email]
💬 Discord: [Your Discord]
📦 GitHub:  [Your GitHub]
```

---

## 🌟 **Why You'll Love aiD_PM**

> "It's like having a PM assistant that never sleeps"

> "Finally, a PM tool that understands developers"

> "The AI features save me hours every week"

> "Privacy + Intelligence + Simplicity = Perfect"

---

**Ready to revolutionize your project management?**

**Start in 3 minutes:** `uvicorn main:app --reload`

---

© 2024 aiD_PM | Built with ❤️ and AI | v1.5 - AI Powered 🚀

