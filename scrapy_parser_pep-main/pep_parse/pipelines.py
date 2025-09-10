import csv
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Optional


class PepParsePipeline:
    """Формирует сводку по статусам PEP в CSV."""

    def __init__(self):
        self.status_counts = Counter()
        self.total = 0
        self.results_dir: Optional[Path] = None
        self.timestamp: Optional[str] = None

    def _resolve_results_dir(self, spider) -> Path:
        feeds = spider.settings.get("FEEDS") or {}
        try:
            first_key = next(iter(feeds))
            return Path(str(first_key)).parent
        except Exception:
            return Path(spider.settings.get("RESULTS_DIR", "results"))

    def open_spider(self, spider):
        self.results_dir = self._resolve_results_dir(spider)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def process_item(self, item, spider):
        status = (item.get("status") or "").strip()
        self.status_counts[status] += 1
        self.total += 1
        return item

    def close_spider(self, spider):
        if self.results_dir is None:
            self.results_dir = self._resolve_results_dir(spider)
            self.results_dir.mkdir(parents=True, exist_ok=True)
        if self.timestamp is None:
            self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        out_path = self.results_dir / f"status_summary_{self.timestamp}.csv"
        with out_path.open("w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Статус", "Количество"])
            for status, count in sorted(self.status_counts.items()):
                writer.writerow([status, count])
            writer.writerow(["Total", self.total])
