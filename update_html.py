import time
from make_html import main as make_html

while True:
    try:
        make_html()
    except Exception as e:
        print(f'error while make_html:\n{e}')
    time.sleep(60 * 10)
