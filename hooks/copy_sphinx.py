import shutil
from pathlib import Path


def on_post_build(config, **kwargs):
    source = Path(config["docs_dir"]).parent / "sphinx" / "_build" / "html"
    target = Path(config["site_dir"]) / "sphinx"
    if not source.is_dir():
        return
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns(".*"))