from typing import re

from dagster import Config, asset
from ftplib import FTP


class GFFLoaderConfig(Config):
    host = 'ftp.ensemblgenomes.ebi.ac.uk'
    base_path = 'pub/plants/'
    file_format = 'gff3'
    genome_release: int = 55
    organism: str
    output_path: str = './gff_files'


@asset(code_version=1)
def raw_genome(config: GFFLoaderConfig, context):
    context.log.info("My run ID is {context.run_id}")
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

    with open(config.download_path + file_name, 'wb') as f:
        ftp.retrbinary(f'RETR {file_name}', f.write)
