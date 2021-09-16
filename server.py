from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from make_html import main as make_html
from pathlib import Path
import concurrent.futures
import time


def update_html():
    while True:
        make_html()
        time.sleep(60)


with concurrent.futures.ThreadPoolExecutor() as pool:
    pool.submit(update_html)


html = Path('index.html')
app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    if not html.exists():
        return 'page is creating, please update page after 1-2 minute'
    return html.read_text()
