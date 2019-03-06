import sys
import os
import shutil
from celery import Celery
from assembly import Assembly
from sra import SequenceReadArchive
sys.path.append('/home/chen1i6c04/Projects/Benga')
from src.algorithms import profiling

app = Celery(backend='redis://', broker="amqp://guest:guest@127.0.0.1:5672")


@app.task
def sra_download_and_split(accession, outdir):
    sra = SequenceReadArchive(accession=accession, outdir=outdir)
    sra.make_url()
    sra.download()
    sra.split()
    sra.remove()
    return accession, sra.fastq_dir, outdir


@app.task
def genome_assembly(args):
    accession, fastq_dir, outdir = args
    assembly = Assembly(accession=accession, reads_path=fastq_dir, outdir=outdir)
    assembly.denovo()
    assembly.move_contig()
    shutil.rmtree(fastq_dir)
    shutil.rmtree(assembly.assembly_dir)
    return assembly.contig_out, outdir


@app.task
def profile(args, database):
    contig_dir, outdir = args
    accession = os.path.basename(contig_dir)
    os.makedirs(os.path.join(outdir, 'Profile', accession))
    profiling.profiling(os.path.join(outdir, 'Profile', accession), contig_dir, database, threads=1, occr_level=0,
                        enable_adding_new_alleles=True, generate_profiles=True, debug=False)

