from fastapi import FastAPI, Request
from app.router.recipes import recipe
from datetime import datetime

app = FastAPI()

app.include_router(recipe.router, prefix="/recipes")

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.now()
    method_name = request.method
    url = request.url
    headers = request.headers
    query_params = request.query_params
    path_params = request.path_params
    cookies = request.cookies
    client = request.client
    
    with open ("request_log.txt", mode="a") as request_file:
        content = f"\nmethod: {method_name}, url: {url}, headers: {headers}, query_params: {query_params}, path_params: {path_params}, cookies: {cookies}, client: {client} received at {datetime.now()}"
        
        request_file.write(content)
        
    response = await call_next(request)
    
    process_time = datetime.now() - start_time
    response.headers["X-Time-Elapsed"] = str(process_time)
    
    return response