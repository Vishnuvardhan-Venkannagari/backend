import fastapi
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import sys
import pkgutil
import importlib
import traceback

app = fastapi.FastAPI(#version='1.0.0',
                      title="SOTAOG-DOE",
                      description=f"RestAPI for SOTAOG-DOE Platform",
                      openapi_url="/openapi.json",
                      docs_url="/docs",
                      redoc_url="/redoc"
                    )

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


@app.middleware('http')
async def authMiddleware(request: fastapi.Request, call_next):
    auth_user = await authenticate()
    if auth_user == "Success":
        return await call_next(request)    
    return await call_next(request)


async def authenticate():
    return "Success"

@app.middleware('http')
async def contextMiddleware(request: fastapi.Request, call_next):
    try:
        resp = await call_next(request)
        response_body = b""
        async for chunk in resp.body_iterator:
            response_body += chunk

        return fastapi.Response(content=response_body, status_code=resp.status_code, headers=dict(resp.headers))

    except Exception as exe:
        """
        Exception error
        """
        # errFormat = error
        errFormat = '''Error: 
        Stack Trace:
        %s
        ''' % (traceback.format_exc())
        print(errFormat)
        return fastapi.responses.JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred.", "error": str(errFormat)}
        )
    

@app.get("/")
def read_root():
    return {"message": "Hello from EC2!"}


@app.get("/api/test")
def test():
    return {"message": "Hello from EC2!"}

auth_router = fastapi.APIRouter(prefix="/api/auth", tags=["Auth"])
@auth_router.get("/me")
async def me(request: fastapi.Request):
    return "Success"

app.include_router(auth_router)

