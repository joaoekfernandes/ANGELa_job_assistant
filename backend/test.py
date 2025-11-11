from services.job_service import search_jobs

if __name__ == "__main__":
    jobs = search_jobs("data analyst", "New York", remote=True)
    print(f"Found {len(jobs)} jobs")
    if jobs:
        print(jobs[0]["job_title"], "-", jobs[0]["employer_name"])

