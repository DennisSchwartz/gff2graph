import datetime
import os
import re
from typing import List

from gt.extended import FeatureIndexMemory
from dagster import Config, Output, asset
from ftplib import FTP

from gff2graph.gff2graph.lib import transform_feature_recursive


class GFF2GraphConfig(Config):
    host = 'ftp.ensemblgenomes.ebi.ac.uk'
    base_path = 'pub/plants/'
    file_format = 'gff3'
    genome_release: int = 55
    organism: str
    raw_genome_path: str = 'genomes/'
    graph_data_path: str = 'graph_data/'
    chromosomes: List[str] = []


@asset(code_version="1")
def raw_genome(context, config: GFF2GraphConfig):
    context.log.info(f"Running pipeline with ID {context.run_id}")
    ftp = FTP(config.host)
    ftp.login()
    ftp.cwd(f'{config.base_path}/release-{config.genome_release}/{config.file_format}')
    ftp.cwd(config.organism)

    files = ftp.nlst()
    pattern = re.escape(config.organism) + r'\..*\.' + re.escape(str(config.genome_release)) + '\.gff3\.gz'
    file_name = None
    for f in files:
        if re.match(pattern, f, re.IGNORECASE):
            file_name = f

    if not file_name:
        msg = f'There was no valid file found for {config.organism}. Available files: {files}'
        context.log.error(msg)
        raise Exception(msg)

    if not os.path.exists(config.raw_genome_path):
        os.makedirs(config.raw_genome_path)

    with open(config.raw_genome_path + file_name, 'wb') as f:
        ftp.retrbinary(f'RETR {file_name}', f.write)

    return Output(
        config.raw_genome_path + file_name,
        metadata={
            'output_file': f'{config.organism}.gff3.gz',
            'user_id': 'dummy'
        }
    )


@asset(code_version="1")
def graph_data(context, raw_genome, config: GFF2GraphConfig) -> None:
    feature_index = FeatureIndexMemory()
    # I think this loads the whole file, I couldn't make the streaming work
    feature_index.add_gff3file(filename=raw_genome)
    chromosomes = config.chromosomes
    if not chromosomes:
        chromosomes = feature_index.get_seqids()

    if not os.path.exists(config.graph_data_path):
        os.makedirs(config.graph_data_path)

    now = datetime.datetime.now().isoformat()
    base_file_name = f'{config.graph_data_path}/{now}_{context.run_id}'
    entities_file = open(base_file_name + '_entities.jsonl', 'w')
    relationships_file = open(base_file_name + '_relationships.jsonl', 'w')

    for seq in chromosomes:
        features = feature_index.get_features_for_seqid(seq)
        for f in features:
            transform_feature_recursive(f, entities_sink=entities_file, relationships_sink=relationships_file)


