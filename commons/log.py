import logging
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent.parent / "logs" / "frame.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=str(LOG_FILE),
    # Use UTF-8 BOM to improve browser charset detection on Jenkins artifacts.
    encoding="utf-8-sig",
    force=True,
)

logger = logging.getLogger()
