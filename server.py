from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pathlib import Path

html = Path('index.html')
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    if not html.exists():
        return 'page is creating, please update page after 1-2 minute'
    return html.read_text()
