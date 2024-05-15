from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

items = []


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


# Function to get the partial list as a string
async def render_item_list(request: Request, items):
    # Here we generate the template response for the items list
    return templates.TemplateResponse("partials/item_list.html", {"request": request, "items": items})


@app.post("/add-item", response_class=HTMLResponse)
async def add_item(request: Request, item: str = Form(...)):
    items.append(item)
    return await render_item_list(request, items)


@app.get("/remove-item/{item_id}", response_class=HTMLResponse)
async def remove_item(request: Request, item_id: int):
    if 0 <= item_id < len(items):
        items.pop(item_id)
    return await render_item_list(request, items)
