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
    parser.add_argument('-d', required=False, default=False, type=str, help="Database")
    args = parser.parse_args()
    return args


def download(acc_number, save_path):
    sra_save_path = os.path.join(save_path, "SRA", acc_number)
    os.makedirs(sra_save_path)
    url = sra.getURL(acc_number)
    sra_file = sra.download(url, sra_save_path)
    return sra_file


def split(acc_number, save_path, sra_file):
    fastq_save_path = os.path.join(save_path, "FASTQ", acc_number)
    sra.split(sra_file=sra_file, out_path=fastq_save_path)
    return fastq_save_path


def denovo(acc_number, save_path, fastq_save_path):
    denovo_save_path = os.path.join(save_path, "Denovo", acc_number)
    if len(os.listdir(fastq_save_path)) == 1:
        reads = [os.path.join(fastq_save_path, read) for read in os.listdir(fastq_save_path)]
        Assembly.layoutIsSingle(read=reads[0], out_path=denovo_save_path)
    elif len(os.listdir(fastq_save_path)) == 2:
        reads = [os.path.join(fastq_save_path, read) for read in os.listdir(fastq_save_path)]
        Assembly.layoutIsPair(read_1=reads[0], read_2=reads[1], out_path=denovo_save_path)
    else:
        read_1, read_2 = Assembly.cleanBarcode(fastq_save_path)
        Assembly.layoutIsPair(read_1=read_1, read_2=read_2, out_path=denovo_save_path)
    return denovo_save_path


def get_contigs(acc_number, save_path, denovo_save_path):
    contigs_save_path = os.path.join(save_path, 'Contigs', acc_number)
    os.makedirs(contigs_save_path)
    shutil.copy(os.path.join(denovo_save_path, "contigs.fasta"), os.path.join(contigs_save_path, acc_number + ".fa"))
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
    save_path = args.o
    database = args.d

    acc = []
    with open(list_) as lines:
        for line in lines:
            acc.append(line.strip())

    for acc_number in acc:
        sra_file = download(acc_number=acc_number, save_path=save_path)
        fastq_save_path = split(acc_number=acc_number, save_path=save_path, sra_file=sra_file)
        denovo_save_path = denovo(acc_number=acc_number, save_path=save_path, fastq_save_path=fastq_save_path)
        contigs_save_path = get_contigs(acc_number, save_path, denovo_save_path)
        remove(sra_file, fastq_save_path, denovo_save_path)

        if not database:
            profile_out_put = os.path.join(save_path, "Profile", acc_number)
            os.mkdir(profile_out_put)
            profile(contigs_save_path, profile_out_put, database)


if __name__ == '__main__':
    main()