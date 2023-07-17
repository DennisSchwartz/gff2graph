from argparse import ArgumentParser

from dagster import RunConfig

from gff2graph import defs
from gff2graph import GFF2GraphConfig


def run_pipeline(organism, chromosomes):
    run_config = GFF2GraphConfig(organism=organism, chromosomes=chromosomes)
    job = defs.get_implicit_global_asset_job_def()

    job.execute_in_process(
        run_config=RunConfig(
            ops={
                "raw_genome": run_config,
                "graph_data": run_config
            }
        )
    )


def create_argument_parser() -> ArgumentParser:
    parser = ArgumentParser(description='Load plant genomes from Ensembl into graph-compatible JSON files.')
    parser.add_argument('-o',
                        '--organism',
                        type=str,
                        required=True,
                        help='The organism to load. Available options can be found at '
                        'https://ftp.ensemblgenomes.ebi.ac.uk/pub/plants/release-55/gff3/')
    parser.add_argument('-c',
                        '--chromosomes',
                        type=str,
                        nargs='*',
                        help='Chromosomes to process. Default: all. Example: -c 1 3 5')
    return parser


if __name__ == '__main__':
    args = create_argument_parser().parse_args()
    run_pipeline(args.organism, args.chromosomes)
