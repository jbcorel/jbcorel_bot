import logging
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.routing.messages import router as m_router
from src.depends import connect_and_init_db, close_db_connect, connect_and_init_redis, close_redis
from src.common.error import BadRequest, UnprocessableError, InternalError
from src.config import Config

logging.basicConfig(level=logging.INFO, stream=sys.stdout)



app = FastAPI(openapi_prefix='/messages')

app.include_router(
    m_router,
    tags=['messages']
    )
 
app.add_event_handler("startup", Config.app_settings_validate)
app.add_event_handler("startup", connect_and_init_db)
app.add_event_handler("startup", connect_and_init_redis)
app.add_event_handler("shutdown", close_db_connect)
app.add_event_handler("shutdown", close_redis)


@app.exception_handler(BadRequest)
async def bad_request_handler(req: Request, exc: BadRequest) -> JSONResponse:
    return exc.gen_err_resp()


@app.exception_handler(RequestValidationError)
async def invalid_req_handler(
    req: Request,
    exc: RequestValidationError
) -> JSONResponse:
    logging.error(f'Request invalid. {str(exc)}')
    return JSONResponse(
        status_code=400,
        content={
            "type": "about:blank",
            'title': 'Bad Request',
            'status': 400,
            'detail': [str(exc)]
        }
    )


@app.exception_handler(UnprocessableError)
async def unprocessable_error_handler(
    req: Request,
    exc: UnprocessableError
) -> JSONResponse:
    return exc.gen_err_resp()


@app.exception_handler(InternalError)
async def internal_error_handler(
    req: Request, 
    exc: InternalError
) -> JSONResponse:
    return exc.gen_err_resp()