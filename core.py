import argparse
import os
import shutil

from sra import SequenceReadArchive as sra
from assembly import Assembly
from profiling import profile


def user_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', required=True, help="SRA Accession List")
    parser.add_argument('-o', required=True, help="Export path")
    parser.add_argument('-db', required=False, default=False, type=str, help="Database")
    args = parser.parse_args()
    return args


def download(acc_number, out):
    path = os.path.join(out, "SRA", acc_number)
    os.makedirs(path)
    url = sra.getURL(acc_number)
    sra_file = sra.download(url, path)
    return sra_file


def split(acc_number, out, sra_file):
    path = os.path.join(out, "FASTQ", acc_number)
    sra.split(sra_file=sra_file, out=path)
    return path


def denovo(acc_number, out, fastq_save_path):
    assembly_result = os.path.join(out, "Denovo", acc_number)
    if len(os.listdir(fastq_save_path)) == 1:
        reads = [os.path.join(fastq_save_path, read) for read in os.listdir(fastq_save_path)]
        Assembly.layoutIsSingle(read=reads[0], out=assembly_result)
    elif len(os.listdir(fastq_save_path)) == 2:
        reads = [os.path.join(fastq_save_path, read) for read in os.listdir(fastq_save_path)]
        Assembly.layoutIsPair(read_1=reads[0], read_2=reads[1], out=assembly_result)
    else:
        read_1, read_2 = Assembly.cleanBarcode(fastq_save_path)
        Assembly.layoutIsPair(read_1=read_1, read_2=read_2, out=assembly_result)
    return assembly_result


def get_contigs(acc_number, out, assembly_result):
    contigs_save_path = os.path.join(out, 'Contigs', acc_number)
    os.makedirs(contigs_save_path)
    shutil.copy(os.path.join(assembly_result, "contigs.fasta"), os.path.join(contigs_save_path, acc_number + ".fa"))
    return contigs_save_path


def remove(*args):
    for path in args:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)
        else:
            pass


def main():
    args = user_parser()
    list_ = args.l
    out = args.o
    database = args.db

    acc = []
    with open(list_) as lines:
        for line in lines:
            acc.append(line.strip())

    for acc_number in acc:
        sra_file = download(acc_number=acc_number, out=out)
        fastq_save_path = split(acc_number=acc_number, out=out, sra_file=sra_file)
        assembly_result = denovo(acc_number=acc_number, out=out, fastq_save_path=fastq_save_path)
        contigs_save_path = get_contigs(acc_number, out, assembly_result)
        remove(sra_file, fastq_save_path, assembly_result)

        if not database:
            profile_out_put = os.path.join(out, "Profile", acc_number)
            os.mkdir(profile_out_put)
            profile(contigs_save_path, profile_out_put, database)


if __name__ == '__main__':
    main()