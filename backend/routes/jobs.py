# from fastapi import APIRouter, Query
# from flask import jsonify
# from requests import request
# from main import app
# from services.job_service import search_jobs

# router = APIRouter(prefix="/jobs", tags=["Jobs"])

# @router.get("/search")
# # @app.route("/api/jobs")
# def get_jobs():
#     query = request.args.get("query", "")
#     location = request.args.get("location", "")
#     results = search_jobs(query, location)
    
#     # Simplify each job object
#     jobs = []
#     for job in results:
#         jobs.append({
#             "title": job.get("job_title"),
#             "company": job.get("employer_name"),
#             "location": job.get("job_location"),
#             "link": job.get("job_apply_link"),
#             "description": job.get("job_description", "")[:300] + "...",  # shorter text
#             "salary": job.get("job_salary") or f"${job.get('job_min_salary', '')} - ${job.get('job_max_salary', '')}",
#             "posted": job.get("job_posted_at"),
#         })
    
#     return jsonify(jobs)


# # def get_jobs(
# #     skill: str = Query(..., description="Main skill or keyword, e.g. Python Developer"),
# #     location: str = Query(None, description="Location, e.g. Chicago, IL"),
# #     remote: bool = Query(False, description="Include remote jobs only")
# # ):
# #     jobs = search_jobs(skill, location, remote)
# #     return {"results": jobs}


from fastapi import APIRouter, Query
from services.job_service import search_jobs

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("/")
def get_jobs(
    query: str = Query("", description="Job title or keyword"),
    location: str = Query("", description="Job location"),
    remote: bool = Query(False, description="Include remote jobs only")
):
    results = search_jobs(query, location)

    jobs = []
    for job in results:
        jobs.append({
            "title": job.get("job_title"),
            "company": job.get("employer_name"),
            "location": job.get("job_location"),
            "link": job.get("job_apply_link"),
            "description": job.get("job_description", "")[:300] + "...",
            "salary": job.get("job_salary") or f"${job.get('job_min_salary', '')} - ${job.get('job_max_salary', '')}",
            "posted": job.get("job_posted_at"),
        })

    return {"results": jobs}
