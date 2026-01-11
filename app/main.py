from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def say_hell():
    return {"message": "Hello!"}