import json
from pathlib import Path


MEASUREMENT_FIELDS = (
    "cold_build",
    "cold_pip",
    "warm_build",
    "warm_pip",
    "site_size_kb",
    "site_files",
)


def _empty_stats() -> dict:
    return {"raw": [0, 0, 0], "median": 0, "mean": 0, "min": 0, "max": 0, "stdev": 0}


def _default_measurements() -> dict:
    return {field: _empty_stats() for field in MEASUREMENT_FIELDS}


def load_measurements(path: Path) -> dict:
    """Читает measurements.json или возвращает дефолт, если файла нет."""
    if not path.exists():
        return _default_measurements()
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def define_env(env):
    """Загружает measurements.json и регистрирует фильтры Jinja2."""

    data_dir = Path(env.project_dir) / "docs" / "_data"
    measurements_path = data_dir / "measurements.json"
    env.variables["measurements"] = load_measurements(measurements_path)

    for name in ("experiment", "build_info", "pipeline"):
        path = data_dir / f"{name}.json"
        env.variables[name] = json.load(open(path, encoding="utf-8")) if path.exists() else {}

    @env.filter
    def percent_saved(cold, warm):
        """Процент выигрыша warm относительно cold. '—' при делении на ноль."""
        if not cold:
            return "—"
        return round((cold - warm) / cold * 100, 1)