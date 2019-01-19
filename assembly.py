import subprocess
import os


class Assembly:
    @staticmethod
    def cleanBarcode(fastq_save_path):
        size = {}
        for fastq in os.listdir(fastq_save_path):
            fastq_file = os.path.join(fastq_save_path, fastq)
            size[fastq_file] = os.stat(fastq_file).st_size

        sort_size = sorted(size, key=lambda x: size[x], reverse=True)
        return sort_size[0], sort_size[1]
        
    @staticmethod
    def layoutIsPair(read_1, read_2, out):
        cmd = ["python", "spades.py",
               "-1", read_1,
               "-2", read_2,
               "-t", "8",
               "-o", out,
               "--careful"]
        subprocess.call(cmd, stdout=subprocess.DEVNULL)

    @staticmethod
    def layoutIsSingle(read, out):
        cmd = ["python", "spades.py",
               "-s", read,
               "-t", "8",
               "-o", out,
               "--careful"]
        subprocess.call(cmd, stdout=subprocess.DEVNULL)