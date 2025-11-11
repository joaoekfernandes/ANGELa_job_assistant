
from fastapi import APIRouter, Query
import requests
import re


router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

def extract_city(location_str: str):
    if not location_str:
        return None
    # Remove commas, split by spaces, pick first part, etc.
    city = re.split(",|–|-", location_str)[0].strip()
    return city


@router.get("/")
def get_jobs(query: str = Query(...),
             location: str = Query(None),
             remote: bool = Query(False)
             ):


    # Call the external API dynamically
    api_url = "https://jsearch.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-key": "50543b5350msh6045016fe73417cp12ee22jsnc05ce7578b40",
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }
    # params = {"query": query, "location": location, "num_pages": 1}
    params = {"query": f"{query} in {location}", "num_pages": 1}

    response = requests.get(api_url, headers=headers, params=params)
    data = response.json()

    # print(data)

    # Transform API results into a simpler format
    jobs = []
    for job in data.get("data", []):

        # normalizing the city name to be able to search it easily
        job_loc_raw = job.get("job_city") or job.get("job_location")
        job_city_normalized = extract_city(job_loc_raw)
        
        if remote and not job.get("job_is_remote"):
            continue  # skip if user requested remote jobs only and this job is not remote

        jobs.append({
            "id": job.get("job_id"),
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "website": job.get("employer_website"),
            "employment_type": job.get("job_employment_type"),
            # "city": job.get("job_city"),
            "city": job_city_normalized,
            "state": job.get("job_state"),
            "location": job.get("job_location"),
            "is_remote": job.get("job_is_remote"),
            "salary": (f"${int(job.get('job_min_salary')):,} - ${int(job.get('job_max_salary')):,} / year"
                       if job.get("job_min_salary") and job.get("job_max_salary")
                       else None),
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
