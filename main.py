import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys
import pkgutil
import importlib

# app = FastAPI()
app = fastapi.FastAPI(version='1.0.0',
                      description=f"RestAPI for SOTAOG-DOE Platform",
                      openapi_url="/openapi.json",
                      title="SOTAOG-DOE")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],  # Add other necessary origins
    allow_credentials=True,
    allow_methods=["*"],  # Ensure all methods (GET, POST, etc.) are allowed
    allow_headers=["*"],  # Ensure all headers (including 'authtoken') are allowed
)

package_dir = os.getcwd() + "/sotaog_doe_api"
sys.path.append(os.path.abspath(package_dir))
@app.on_event("startup")
def onStart():
    # print("Onstart", package_dir)
    for module_info in pkgutil.iter_modules([str(package_dir)]):
        module = importlib.import_module(f'{module_info.name}')#routers.
        # print(hasattr(module, 'router'))
        if hasattr(module, 'router'):
            app.include_router(module.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Hello from EC2!"}


@app.get("/test")
def test():
    return {"message": "Hello from EC2!"}


# @app.get("/download-report", response_class=FileResponse)
# def download_report():
#     """ Endpoint to download the generated report file """
#     file_path = "PARETO_report.xlsx"

#     # Check if the file exists before serving it
#     if not os.path.exists(file_path):
#         return {"error": "Report file not found!"}

#     return FileResponse(
#         path=file_path,
#         filename="PARETO_report.xlsx",
#         media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#     )
