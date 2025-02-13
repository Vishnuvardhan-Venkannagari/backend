from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from EC2!"}


@app.get("/test")
def test():
    return {"message": "Hello from EC2!"}
