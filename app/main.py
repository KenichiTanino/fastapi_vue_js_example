import json
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

data = [
    {"id": 1, "name": "山田太郎", "address": "東京都", "gender": "男", "birthdate": "1990年1月1日"},
    {"id": 2, "name": "田中花子", "address": "大阪府", "gender": "女", "birthdate": "1995年5月10日"},
]
next_id = 3


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "data": json.dumps(data, ensure_ascii=False)})


@app.post("/update")
async def update_data(id: int = Form(...), name: str = Form(...), address: str = Form(...), gender: str = Form(...), birthdate: str = Form(...)):
    global data
    for item in data:
        if item["id"] == id:
            item["name"] = name
            item["address"] = address
            item["gender"] = gender
            item["birthdate"] = birthdate
            return {"message": "Data updated", "data": data}
    raise HTTPException(status_code=404, detail="Item not found")


@app.post("/add")
async def add_data(name: str = Form(...), address: str = Form(...), gender: str = Form(...), birthdate: str = Form(...)):
    global data, next_id
    new_item = {"id": next_id, "name": name, "address": address, "gender": gender, "birthdate": birthdate}
    data.append(new_item)
    next_id += 1
    return {"message": "Data added", "data": data}


@app.delete("/delete/{item_id}")
async def delete_data(item_id: int):
    global data
    data = [item for item in data if item["id"] != item_id]
    return {"message": "Data deleted", "data": data}