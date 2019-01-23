import sys
import os
import shutil
import click
from assembly import Assembly
from sra import SequenceReadArchive
sys.path.append('Benga')
from src.algorithms import profiling


@click.command()
@click.argument('sra_list', type=click.Path(exists=True))
@click.argument('out', type=click.Path(exists=True))
@click.argument('database')
def run(sra_list, out, database):
    acc = []
    with open(sra_list) as lines:
        for line in lines:
            acc.append(line.strip())

    for acc_number in acc:
        sra = SequenceReadArchive(accession=acc_number, outdir=out)
        sra.make_url()
        sra.download()
        sra.split()
        sra.remove()

        assembly = Assembly(accession=acc_number, reads=sra.fastq_dir, outdir=out)
        assembly.denovo()
        assembly.move_cotig()

        profile = os.path.join(out, 'Profile', acc_number)
        os.makedirs(profile, exist_ok=True)

        profiling.profiling(profile, assembly.contig_out, database, threads=1, occr_level=95,
                            enable_adding_new_alleles=True, generate_profiles=True, debug=False)

        shutil.rmtree(sra.fastq_dir)
        shutil.rmtree(assembly.out)
