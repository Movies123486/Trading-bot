from __future__ import annotations

from datetime import date
from pathlib import Path

from .env_checks import check_environment
from .filesystem import ensure_hive_partition
from .logging_utils import configure_logging
from .manifest import create_run_manifest
from .settings import Settings


def main() -> None:
    settings = Settings()
    logger = configure_logging(settings.log_level)
    env = check_environment(settings.ntp_server)
    logger.info("environment", details=env)

    partition = ensure_hive_partition(settings.data_dir, "BTCUSDT", "1h", date.today())
    logger.info("data_partition", path=str(partition))

    manifest = create_run_manifest(settings, Path("manifests"))
    logger.info("manifest_created", path=str(manifest))


if __name__ == "__main__":
    main()
