# ingestion/pdf_async.py
from concurrent.futures import ThreadPoolExecutor
import time

from .pdf_extract import extract_pdf_text

pdf_tasks = {}
executor = ThreadPoolExecutor(max_workers=1)


def launch_pdf_task(task_id: str, pdf_bytes: bytes, max_pages: int = 5) -> None:
    """
    Launch async PDF extraction and store future in pdf_tasks.
    """

    def _job():
        time.sleep(0.5)
        text = extract_pdf_text(pdf_bytes, max_pages=max_pages)
        return text

    future = executor.submit(_job)
    pdf_tasks[task_id] = {"future": future, "stage": "processing"}
