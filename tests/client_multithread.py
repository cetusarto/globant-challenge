import requests
import pandas as pd
import threading
BASE_URL = "https://globant-interview-439580738234.us-central1.run.app"
BASE_URL = "https://globant-interview-439580738234.us-central1.run.app"

def upload_file(table_name, file_path):
    """Uploads a PDF to the API asynchronously."""
    with open(file_path, "rb") as f:
        response = requests.post(f"{BASE_URL}/upload/pdf/{table_name}/", files={"file": f})

    print(f"Uploading {file_path}: {response.status_code} - {response.json()}")

def get_data(view_name, result_dict):
    """Fetches data using the GET method asynchronously."""
    response = requests.get(f"{BASE_URL}/get/{view_name}/")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        result_dict[view_name] = df 
        print(f"Retrieved {len(df)} rows from {view_name}.")
    else:
        print(f"Error fetching {view_name}: {response.status_code} - {response.json()}")

def run():
    # Define files to upload
    files = [
        ("employees", "../app/data/hired_p1.pdf"),
        ("employees", "../app/data/hired_p2.pdf"),
        ("employees", "../app/data/hired_p3.pdf"),
        ("jobs", "../app/data/jobs.pdf"),
        ("departments", "../app/data/Departamentos.pdf"),
    ]

    # Start upload threads
    upload_threads = [threading.Thread(target=upload_file, args=(table, path)) for table, path in files]
    for thread in upload_threads:
        thread.start()

    for thread in upload_threads:
        thread.join()  

    # Start GET request threads
    result_dict = {} 
    get_threads = [
        threading.Thread(target=get_data, args=("job_department", result_dict)),
        threading.Thread(target=get_data, args=("department", result_dict)),
    ]
    for thread in get_threads:
        thread.start()

    for thread in get_threads:
        thread.join()  

    # Print retrieved data
    print("Job Department View:\n", result_dict.get("job_department"))
    print("Department View:\n", result_dict.get("department"))

if __name__ == "__main__":
    run()
