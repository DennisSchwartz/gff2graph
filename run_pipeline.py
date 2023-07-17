from dagster import RunConfig

from gff2graph.gff2graph import defs
from gff2graph.gff2graph.assets import GFF2GraphConfig

gff2graph_job = defs.get_implicit_global_asset_job_def()

run_config = GFF2GraphConfig(organism="arabidopsis_thaliana")

result = gff2graph_job.execute_in_process(
    run_config=RunConfig(ops={
        "raw_genome": run_config,
        "graph_data": run_config
    })
)
