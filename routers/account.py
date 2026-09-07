from typing import Optional
from fastapi import APIRouter, Request, Header, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError, HTTPException

router = APIRouter()
templates: Jinja2Templates = Jinja2Templates(directory='templates')

@router.post('/', response_class=HTMLResponse)
async def acc_post(
    request: Request,
    hx_request: Optional[str] = Header(None),
    login: Optional[str] = Form(None),
    passw: Optional[str] = Form(None)
):
    if not hx_request:
        raise HTTPException(400, 'Invalid Request')
    
    user = 'Test'
    user_pass = '123456'
    
    if not (login == user and passw == user_pass):
        raise HTTPException(401, 'Not a valid user!')
    
    context = {
        "name": "Shopping List"
    }
    
    return templates.TemplateResponse(request, 'partials/account.html', context)