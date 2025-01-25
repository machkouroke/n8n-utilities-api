from fastapi import FastAPI
from traceback import print_exception
from urllib.request import Request

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

import uvicorn

import routes_prono

app = FastAPI()


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        # you probably want some kind of logging here
        print_exception(e)
        return Response("Internal server error", status_code=500)

app.middleware('http')(catch_exceptions_middleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(routes_prono.router, prefix='/pronos')

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, reload=True)
