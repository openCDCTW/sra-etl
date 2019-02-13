import sys
import os
import shutil
import click
from assembly import Assembly
from sra import SequenceReadArchive
sys.path.append('/home/chen1i6c04/Projects/Benga')
from src.algorithms import profiling


@click.command()
@click.argument('accession', type=click.STRING)
@click.argument('out', type=click.Path(exists=True))
@click.option('--database', default=False)
def main(accession, out, database):
    sra = SequenceReadArchive(accession=accession, outdir=out)
    sra.make_url()
    # sra.download()
    sra.split()
    # sra.remove()

    assembly = Assembly(accession=accession, reads_path=sra.fastq_dir, outdir=out)
    assembly.denovo()
    shutil.rmtree(sra.fastq_dir)
    if database:
        profile = os.path.join(out, 'Profile', accession)
        os.makedirs(profile, exist_ok=True)
        try:
            assembly.move_contig()
            profiling.profiling(profile, assembly.contig_out, database, threads=1, occr_level=0,
                                enable_adding_new_alleles=True, generate_profiles=True, debug=False)
        except FileNotFoundError:
            pass
    else:
        try:
            assembly.move_contig()
        except FileNotFoundError:
            pass
    shutil.rmtree(assembly.assembly_dir)


if __name__ == '__main__':
    main()
