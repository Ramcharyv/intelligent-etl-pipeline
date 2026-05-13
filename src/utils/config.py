import os
from dataclasses import dataclass, field


@dataclass
class PipelineConfig:
    env: str = "databricks"
    run_id: str = "dev"

    # Storage paths — update these after cluster starts
    raw_data_path: str = field(default="")
    bronze_path: str = field(default="")
    silver_path: str = field(default="")
    gold_clean_path: str = field(default="")
    gold_quarantine_path: str = field(default="")
    mlflow_tracking_uri: str = field(default="databricks")

    # ML thresholds
    contamination: float = 0.05
    zscore_threshold: float = 3.5
    alert_threshold: float = 0.10

    # Alerting
    slack_webhook_url: str = field(default="")

    def __post_init__(self):
        base = "/FileStore/intelligent_etl"

        if not self.raw_data_path:
            self.raw_data_path = f"{base}/raw"
        if not self.bronze_path:
            self.bronze_path = f"{base}/delta/bronze/orders"
        if not self.silver_path:
            self.silver_path = f"{base}/delta/silver/orders"
        if not self.gold_clean_path:
            self.gold_clean_path = f"{base}/delta/gold/orders_clean"
        if not self.gold_quarantine_path:
            self.gold_quarantine_path = f"{base}/delta/gold/orders_quarantine"

        self.contamination = float(
            os.getenv("ML_CONTAMINATION", self.contamination))
        self.alert_threshold = float(
            os.getenv("ALERT_THRESHOLD", self.alert_threshold))