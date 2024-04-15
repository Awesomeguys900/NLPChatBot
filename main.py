from fastapi import FastAPI
from chat import get_Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/chat/{message}")
async def readItem(message: str):
    message = message.replace("%", " ")
    response = get_Response(message)
    return {"response": response}
