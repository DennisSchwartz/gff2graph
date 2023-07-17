from dagster import Definitions, load_assets_from_modules

from . import assets
from .assets import GFF2GraphConfig

all_assets = load_assets_from_modules([assets])

defs = Definitions(
    assets=all_assets,
)