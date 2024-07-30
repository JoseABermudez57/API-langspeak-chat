import uvicorn
from src.infrastructure.dependencies import init_routers
from fastapi import FastAPI

app = FastAPI()

init_routers(app)


# def main():
#     init_rabbitmq()


if __name__ == "__main__":
    # main()
    uvicorn.run("main:app", host="0.0.0.0", port=8083)
