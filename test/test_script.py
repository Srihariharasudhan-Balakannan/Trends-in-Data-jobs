import scrape_data as scraper 
import save_data as saver
import time
from concurrent.futures import ThreadPoolExecutor

def scrape_and_save_jobs(job_role, cnt):
    print(f"Starting scraping for: {job_role}")
    start_time = time.time()
    try:
        job_list = scraper.get_jobs(job_role=job_role, cnt=cnt)
        num_jobs_found = len(job_list)
        filename = f"{job_role.replace(' ', '_').lower()}_output.json"
        saver.save_dicts_to_json(job_list, filename)
    except Exception as e:
        print(f"Error scraping or saving for '{job_role}': {e}")
        num_jobs_found = 0
        filename = "Error"
    end_time = time.time()
    time_taken = end_time - start_time
    return {
        "job_role": job_role,
        "jobs_found": num_jobs_found,
        "time_taken_seconds": time_taken,
        "output_file": filename
    }

if __name__ == '__main__':
    job_roles = [
        "Data Engineer",
        "Data Analyst",
        "Data Architect",
        "Data Scientist",
        "Machine Learning Engineer"
    ]
    
    jobs_per_role_count = 500
    overall_start_time = time.time()

    print("\n--- Scraping Summary ---\n")
    for role in job_roles:
        result = scrape_and_save_jobs(role, jobs_per_role_count)
        print(f"Role: {result['job_role']}")
        print(f"  Jobs Found: {result['jobs_found']}")
        print(f"  Time Taken: {result['time_taken_seconds']:.2f} seconds")
        print(f"  Output File: {result['output_file']}")
        print("-" * 30)

    overall_end_time = time.time()
    overall_total_time = overall_end_time - overall_start_time
    overall_total_time_minutes = overall_total_time / 60

    print(f"\nOverall total time taken for all job roles: {overall_total_time:.2f} seconds")
    print(f"Overall total time taken for all job roles: {overall_total_time_minutes:.2f} minutes")
