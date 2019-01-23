import sys
import os
import shutil
import click
from assembly import Assembly, get_contig
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
        sra = SequenceReadArchive(accession=acc_number, out=out)
        sra.get_url()
        sra.download()
        sra.split()
        sra.remove()

        assembly = Assembly(accession=acc_number, reads=sra.to_fastq, out=out)
        assembly_result = assembly.denovo()

        contig = get_contig(accession=acc_number, out=out, assembly_result=assembly_result)

        profile = os.path.join(out, 'Profile', acc_number)
        os.makedirs(profile, exist_ok=True)

        profiling.profiling(profile, contig, database, threads=1, occr_level=95,
                            enable_adding_new_alleles=True, generate_profiles=True, debug=False)

        shutil.rmtree(sra.to_fastq)
        shutil.rmtree(assembly_result)
