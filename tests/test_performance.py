import time

def test_page_load_time(page):
    start = time.time()
    page.goto("https://trade.multibank.io/")
    end = time.time()

    assert end - start < 5