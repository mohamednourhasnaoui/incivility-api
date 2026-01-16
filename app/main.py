from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import time

app = FastAPI()

# =========================
# In-memory storage
# =========================
complaints = []
submission_times = []

# =========================
# HOME / LOGIN
# =========================
@app.get("/", response_class=HTMLResponse)
def login_page():
    return """
    <html>
    <head>
        <title>Incivility Reporting</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: linear-gradient(120deg, #1e3c72, #2a5298);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
            }
            .card {
                background: white;
                color: black;
                padding: 30px;
                border-radius: 12px;
                width: 320px;
                animation: fadeIn 1s;
            }
            input, button {
                width: 100%;
                padding: 10px;
                margin-top: 10px;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            button {
                background: #2a5298;
                color: white;
                border: none;
                cursor: pointer;
            }
            @keyframes fadeIn {
                from {opacity: 0; transform: translateY(20px);}
                to {opacity: 1; transform: translateY(0);}
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Login</h2>
            <form method="post" action="/login">
                <input name="username" placeholder="Username" required>
                <input name="password" type="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
            <p style="margin-top:10px;font-size:12px;">
                Admin login → username: <b>admin</b>
            </p>
        </div>
    </body>
    </html>
    """

# =========================
# LOGIN LOGIC
# =========================
@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if username == "admin":
        return RedirectResponse("/admin", status_code=303)
    return RedirectResponse("/form", status_code=303)

# =========================
# USER FORM
# =========================
@app.get("/form", response_class=HTMLResponse)
def complaint_form():
    return """
    <html>
    <head>
        <title>Submit Complaint</title>
        <style>
            body { font-family: Arial; background:#f4f6f8; padding:40px; }
            .box {
                max-width:500px;
                margin:auto;
                background:white;
                padding:25px;
                border-radius:10px;
            }
            input, textarea, button {
                width:100%;
                margin-top:10px;
                padding:10px;
            }
            button {
                background:#1e3c72;
                color:white;
                border:none;
            }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Report Incivility</h2>
            <form method="post" action="/submit">
                <input name="category" placeholder="Category" required>
                <input name="location" placeholder="Location" required>
                <textarea name="description" placeholder="Description" required></textarea>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """

# =========================
# SUBMIT COMPLAINT (RATE LIMIT)
# =========================
@app.post("/submit")
def submit(category: str = Form(...), description: str = Form(...), location: str = Form(...)):
    now = time.time()

    # keep only last 60 seconds
    recent = [t for t in submission_times if now - t < 60]
    submission_times.clear()
    submission_times.extend(recent)

    if len(submission_times) >= 3:
        return HTMLResponse(
            "<h2>⛔ Limit reached</h2><p>Max 3 complaints per minute.</p><a href='/form'>Back</a>",
            status_code=429
        )

    submission_times.append(now)

    complaints.append({
        "category": category,
        "description": description,
        "location": location,
        "status": "Pending"
    })

    return RedirectResponse("/form", status_code=303)

# =========================
# ADMIN PANEL
# =========================
@app.get("/admin", response_class=HTMLResponse)
def admin():
    rows = ""
    for i, c in enumerate(complaints):
        rows += f"""
        <tr>
            <td>{c['category']}</td>
            <td>{c['location']}</td>
            <td>{c['description']}</td>
            <td>{c['status']}</td>
            <td>
                <a href="/update/{i}/Pending">Pending</a> |
                <a href="/update/{i}/Solved">Solved</a> |
                <a href="/update/{i}/Denied">Denied</a>
            </td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Admin</title>
        <style>
            body {{ font-family: Arial; padding:30px; }}
            table {{ width:100%; border-collapse: collapse; }}
            th, td {{ border:1px solid #ccc; padding:8px; }}
            th {{ background:#1e3c72; color:white; }}
        </style>
    </head>
    <body>
        <h2>Admin – Complaints</h2>
        <table>
            <tr>
                <th>Category</th>
                <th>Location</th>
                <th>Description</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
            {rows}
        </table>
    </body>
    </html>
    """

# =========================
# UPDATE STATUS
# =========================
@app.get("/update/{index}/{status}")
def update(index: int, status: str):
    if 0 <= index < len(complaints):
        complaints[index]["status"] = status
    return RedirectResponse("/admin", status_code=303)
