import os
import shutil
import subprocess


def SPAdes_cmd(reads, out):
    if len(reads) == 2:
        cmd = ["python", "spades.py",
               "-1", reads[0],
               "-2", reads[1],
               "-t", "8",
               "-o", out,
               "--careful"]
    else:
        cmd = ["python", "spades.py",
               "-s", reads[0],
               "-t", "8",
               "-o", out,
               "--careful"]
    return cmd


def get_contig(accession, out, assembly_result):
    out_path = os.path.join(out, 'Contigs', accession)
    os.makedirs(out_path)
    shutil.copy(os.path.join(assembly_result, "contigs.fasta"), os.path.join(out_path, accession + ".fa"))
    return out_path


class Assembly:
    def __init__(self, accession, reads, out):
        self.accession = accession
        self.reads = [os.path.join(reads, read) for read in os.listdir(reads)]
        self.out = os.path.join(out, 'Assembly', self.accession)
        os.makedirs(self.out)

    def denovo(self):
        if len(self.reads) > 2:
            reads = self._clean_barcode()
            cmd = SPAdes_cmd(reads=reads, out=self.out)
        else:
            cmd = SPAdes_cmd(reads=self.reads, out=self.out)
        subprocess.call(cmd, stdout=subprocess.DEVNULL)
        return self.out

    def _clean_barcode(self):
        reads_size = {read: os.stat(read).st_size for read in self.reads}
        reads_size_sort = sorted(reads_size, key=lambda x: reads_size[x], reverse=True)
        return reads_size_sort[0:2]
