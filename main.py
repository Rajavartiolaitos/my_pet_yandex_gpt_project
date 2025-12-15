import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from db import Base, engine, get_user_requests, add_user_data
from yandex_gpt_client import get_answer_from_yandex_gpt


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    print("Запись внесена")
    yield

app = FastAPI(title='Мой невероятный (на самом деле нет) пет-проект', lifespan=lifespan)

@app.post("/questions")
def send_request(request: Request, answer: str, role="Отвечай на мои вопросы так, как если бы ты был клоуном."):
    user_ip_address = request.client.host
    result = get_answer_from_yandex_gpt(role, answer)
    add_user_data(
        ip_address=user_ip_address,
        answer=answer,
        role=role,
        response=result
    )
    return {'message': result}

@app.get("/requests_list")
def return_my_requests(request: Request):
    user_ip_address = request.client.host
    user_requests = get_user_requests(ip_address=user_ip_address)
    return user_requests


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", log_level="info")
