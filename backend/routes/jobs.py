
from fastapi import APIRouter, Query
import requests


router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("/")
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

    print(data)

    # Transform API results into a simpler format
    jobs = []
    for job in data.get("data", []):
        print(job.get("job_apply_options"))
        jobs.append({
            "id": job.get("job_id"),
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "website": job.get("employer_website"),
            "location": job.get("job_location"),
            "employment_type": job.get("job_employment_type"),
            "city": job.get("job_city"),
            "state": job.get("job_state"),
            "is_remote": job.get("job_is_remote"),
            "salary_min": job.get("job_min_salary"),
            "salary_max": job.get("job_max_salary"),
            "posted": job.get("job_posted_at"),
            "description": job.get("job_description"),
            "responsibilities": job.get("job_highlights", {}).get("Responsibilities"),
            "qualifications": job.get("job_highlights", {}).get("Qualifications"),
            "benefits": job.get("job_highlights", {}).get("Benefits"),
            "apply_links": [
                {
                    "source": opt.get("publisher"),
                    "link": opt.get("apply_link")
                    }
                    for opt in job.get("apply_options", [])
                    if opt.get("apply_link")
                    ],
            })
    
    return {"results": jobs}
