# FastAPI Dockerized Solution on Cloud Run + Cloud SQL
The following app presents a quick scalable solution for a problem set for an interview. The requirements where divided in two steps for a REST API:

- An endpoint that handles the upload of up to 1000 rows for three different tables and saves it in a structured database.
- An endpoint that retrieves two tables for analysis of the preuploaded data.

The solution uses the framework of FastAPI and saves the data in a PSQL instance located in Cloud SQL. It also hosts the API in a Cloud Run service.

## Installation and running
To install this project, follow the steps on the Dockerfile or simply build the image with it. Running the build will set the uvicorn server in the port 8080. If Docker is to be avoided, just running the 

    pip install -r requirements.txt

command inside the project folder to secure the libraries to be used. To run the server use the command

    uvicorn app.main:app --host 0.0.0.0 --port 8000

to run a local version of the server.

## API Requirements
The requirements that this API is expected to fulfill are:
- Receive PDF file uploads
- Transform and validate file
- Store validated data in a structured Database
- Get the analytics proposed by the problem

The security and network part of the infrastructre will be left to many assumptions. The solution leaves out many exploits.

## FastAPI
The framework and speed of development that FastAPI has is nearly unmatched. It also posseses higher reliability that some other frameworks like Flask and has a built in data validation with Pydantic. With this framework the selected routes were:
- POST /pdf/{table_name}/ : Uploads in the pdf format for table_name (employee, jobs or departments)
- POST /pdf/{table_name}/ : Uploads in the csv format for table_name (employee, jobs or departments). This path is still in revision
- GET /{view_name}/ : Gets in the json format the defined analytic view (job_department,department)

## SQL database
The DDL of the tables are explicitly defined inside the /app/sql/ folder. Here it can be seen the definition of the three tables, as well as the views for the two 


