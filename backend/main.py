from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from routes import jobs
import requests

app = FastAPI()

# Allow frontend origins (localhost + any random Angular port)
origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # ✅ allowed origins
    allow_credentials=True,
    allow_methods=["*"],             # ✅ allow all HTTP methods
    allow_headers=["*"],             # ✅ allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Backend is working!"}


app.include_router(jobs.router)

@app.get("/api/jobs")
def get_jobs(query: str = Query(...), location: str = Query(None)):
    # Call the external API dynamically
    api_url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": "50543b5350msh6045016fe73417cp12ee22jsnc05ce7578b40",
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    params = {"query": query, "location": location}

    response = requests.get(api_url, headers=headers, params=params)
    data = response.json()

    # Transform API results into a simpler format
    jobs = []
    for job in data.get("data", []):
        jobs.append({
            "id": job.get("job_id"),
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_location"),
            "city": job.get("job_city"),
            "state": job.get("job_state"),
            "is_remote": job.get("job_is_remote"),
            "employment_type": job.get("job_employment_type"),
            "salary_min": job.get("job_min_salary"),
            "salary_max": job.get("job_max_salary"),
            "posted": job.get("job_posted_at"),
            "description": job.get("job_description"),
            "responsibilities": job.get("job_highlights", {}).get("Responsibilities"),
            "qualifications": job.get("job_highlights", {}).get("Qualifications"),
            "benefits": job.get("job_highlights", {}).get("Benefits"),
            "apply_links": job.get("job_apply_options"),
        })
    
    return {"results": jobs}

# @app.get('/dashboard')
# def get_dashboard():
#     # Mocked dashboard payload — replace with real DB/service logic
#     return {
#         'userName': 'João',
#         'stats': {
#             'applications': 14,
#             'interviews': 3,
#             'courses': 2,
#             'recommendations': 7,
#         },
#         'recent': [
#             { 'title': 'Applied: Frontend Dev', 'when': '2 days ago', 'summary': 'Submitted application for Frontend Developer.' },
#             { 'title': 'Interview: Mock Round', 'when': '3 days ago', 'summary': 'Completed a mock interview session.' },
#             { 'title': 'Course Completed', 'when': '1 week ago', 'summary': 'Finished Advanced JS Algorithms.' },
#         ],
#     }
