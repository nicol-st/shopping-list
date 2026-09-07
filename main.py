# GLOBAL IMPORTS
import uvicorn, logging
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from datetime import date

# LOCAL IMPORTS
from modules import config as cfg
from routers import account

# LOGGING FORMATTER
# logging.basicConfig(format=f'%(asctime)s | %(levelname)s - %(message)s', datefmt='%d.%m.%Y %H:%M:%S', level=logging.INFO, filename='./logs/server.log', force=True)

# CONSTANTS
CREATED = date(2026, 8, 31)

# LIFESPAN
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    logging.info('Server startup...')

    yield
    
    #SHUTDOWN
    logging.info('Server shutdown...')
    
# APP CONFIG
app: FastAPI = FastAPI( 
    lifespan=lifespan,
    docs_url=None if not cfg.DEBUGGING else "/docs",
    redoc_url=None if not cfg.DEBUGGING else "/redoc"
)

# TEMPLATES AND MOUNTS
templates: Jinja2Templates = Jinja2Templates(directory='templates')
app.mount('/css', StaticFiles(directory='static/css'), name='css')
app.mount('/js', StaticFiles(directory='static/js'), name='js')

# ROUTERS
app.include_router(account.router, prefix='/acc', tags=['account', 'sign in', 'log in', 'manage'])

# MAIN ENDPOINT GET METHOD
@app.get('/', response_class=HTMLResponse)
async def main_get(
    request: Request,
):
    
    context = {
        "name": "Shopping List"
    }
    
    return templates.TemplateResponse(request, 'index.html', context)

# ERROR 404 HANDLER
@app.exception_handler(400)
async def custom_400_handler(
    request: Request,
    detail
):
    context = {
        "name": "Shopping List - Error 400",
        "code": detail.status_code,
        "message": detail.detail
    }
    return templates.TemplateResponse(request, 'errors/400.html', context)

# UNKNOWN ERROR HANDLER
@app.exception_handler(HTTPException)
async def custom_error_handler (
    request: Request,
    detail
):
    context = {
        "name": "Shopping List - Unknown Error",
        "code": detail.status_code,
        "message": detail.detail
    }
    return templates.TemplateResponse(request, 'errors/unknown.html', context)

if __name__ == "__main__": 
    if cfg.DEBUGGING:
        uvicorn.run(app='main:app', host=cfg.DEBUGGING_SOCKET, port=cfg.DEBUGGING_PORT, reload=True, reload_excludes=["test.py"])
    else: # PROD MODE  
        uvicorn.run(app='main:app', host='0.0.0.0', port=cfg.PORT, reload=True)