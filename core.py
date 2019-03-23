import os
import sys
import shutil
import configparser
from pathlib import Path
from celery import Celery
from assembly import Assembly
from sra import SequenceReadArchive

config = configparser.ConfigParser()
config.read('config.txt')
profiling_program = config.get('PROFILING', 'Program')
sys.path.append(profiling_program)
from src.algorithms import profiling


app = Celery(backend='redis://', broker="amqp://guest:guest@127.0.0.1:5672")


@app.task
def sra_download_and_split(accession, outdir):
    sra_outdir = Path(outdir, 'sra')
    fastq_dir = Path(outdir, 'fastq', accession)
    sra = SequenceReadArchive(accession=accession, outdir=sra_outdir)
    sra.make_url()
    sra.download()
    sra.split(fastq_dir)
    sra.remove()
    return accession, fastq_dir, outdir


@app.task
def genome_assembly(args):
    accession, fastq_dir, outdir = args
    contig_dir = Path(outdir, 'contig', accession)
    assembly = Assembly(accession=accession, reads_path=fastq_dir, outdir=outdir)
    assembly.denovo()
    assembly.move_contig(contig_dir)
    shutil.rmtree(fastq_dir)
    shutil.rmtree(assembly.outdir)
    return contig_dir, outdir


@app.task
def profile(args, database):
    contig_dir, outdir = args
    accession = os.path.basename(contig_dir)
    os.makedirs(os.path.join(outdir, 'Profile', accession))
    profiling.profiling(os.path.join(outdir, 'Profile', accession), contig_dir, database, threads=1, occr_level=0,
                        enable_adding_new_alleles=True, generate_profiles=True, debug=False)

