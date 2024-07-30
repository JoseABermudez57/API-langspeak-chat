import uvicorn
from src.infrastructure.dependencies import init_rabbitmq, init_routers
from fastapi import FastAPI

# from pydantic import BaseModel
#
#
# class TextInput(BaseModel):
#     text: str
#
#
# class AnalysisResult(BaseModel):
#     original_text: str
#     filtered_text: str
#     sentiment: str
#     score: float


app = FastAPI()

init_routers(app)


def main():
    init_rabbitmq()


if __name__ == "__main__":
    main()
    uvicorn.run("main:app", host="0.0.0.0", port=8083, reload=True)
