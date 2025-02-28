import requests
import pandas as pd

BASE_URL = "https://globant-challenge-439580738234.us-central1.run.app"

def upload_file(table_name, file_path):
    """Uploads pdf to the database"""
    with open(file_path, "rb") as f:
        response = requests.post(f"{BASE_URL}/upload/pdf/{table_name}/", files={"file": f})

    print(f"Uploading {file_path}: {response.status_code} - {response.json()}")
    return response.status_code


def get_data(view_name):
    """Uses the GET method to return the respective view into a pd df"""
    response = requests.get(f"{BASE_URL}/download/{view_name}/")
    if response.status_code == 200:
        df = pd.DataFrame(response.json())
        print(f"Retrieved {len(df)} rows from {view_name}.")
        return df
    else:
        print(f"Error fetching {view_name}: {response.status_code} - {response.json()}")
        return None
    
def run():
    # Upload employees
    upload_file("employees","../app/data/hired_p1.pdf")
    upload_file("employees","../app/data/hired_p2.pdf")
    upload_file("employees","../app/data/hired_p3.pdf")

    # Upload jobs
    upload_file("jobs","../app/data/jobs.pdf")

    # Upload departments
    upload_file("departments","../app/data/Departamentos.pdf")


    df_job_department = get_data("job_department")
    df_department = get_data("department")

    print("Job Department view")
    print(df_job_department)

    print("Department view")
    print(df_department)


if __name__ == "__main__":
    run()