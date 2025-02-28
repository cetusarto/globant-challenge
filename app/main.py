from fastapi import FastAPI
from routers import upload_csv, upload_pdf, download
import uvicorn, os


# Initializes API
app = FastAPI(title="Data upload API", description="Handles CSV & PDF uploads for the hired employees data")


# Declare rooth Path
@app.get("/")
def root():
    return {"message": "Welcome to the Hired Employees Upload API. Use /upload/[table name]/csv/ or /upload/[table name]/pdf/ to upload files."}

# Include upload routers
app.include_router(upload_csv.router)
app.include_router(upload_pdf.router)

# Include download routers
app.include_router(download.router)

# Declare path for healthcheck status
@app.post("/healthcheck/")
def health_check():
    return {"status": "API is running"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Default to 8080
    uvicorn.run(app, host="0.0.0.0", port=port)
