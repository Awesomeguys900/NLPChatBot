from fastapi import FastAPI
from chat import get_Response
from fastapi.middleware.cors import CORSMiddleware
from ExtraFunctionality import mathsSolver
from ExtraFunctionality import weatherFind

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
    try:
         return(f"response: {str(mathsSolver(message))}")
    except:
        response = get_Response(message)
    return {"response": response}
