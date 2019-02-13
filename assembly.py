import os
import shutil
import subprocess


def spades_cmd(reads, out):
    if len(reads) == 2:
        cmd = ["spades.py",
               "-1", reads[0],
               "-2", reads[1],
               "-t", "8",
               "-o", out,
               "--careful"]
    else:
        cmd = ["spades.py",
               "-s", reads[0],
               "-t", "8",
               "-o", out,
               "--careful"]
    return cmd


class Assembly:
    def __init__(self, accession, reads_path, outdir):
        self.accession = accession
        self.reads = [os.path.join(reads_path, read) for read in os.listdir(reads_path)]
        self.assembly_dir = os.path.join(outdir, 'Assembly', self.accession)
        self.contig_out = os.path.join(outdir, 'Contig', self.accession)
        os.makedirs(self.assembly_dir)
        os.makedirs(self.contig_out)

    def denovo(self):
        if len(self.reads) > 2:
            reads = self._clean_barcode()
            cmd = spades_cmd(reads=reads, out=self.assembly_dir)
        else:
            cmd = spades_cmd(reads=self.reads, out=self.assembly_dir)
        subprocess.call(cmd, stdout=subprocess.DEVNULL)

    def _clean_barcode(self):
        reads_size = {read: os.stat(read).st_size for read in self.reads}
        reads_size_sort = sorted(reads_size, key=lambda x: reads_size[x], reverse=True)
        return reads_size_sort[0:2]

    def move_contig(self):
        contig_file = os.path.join(self.assembly_dir, "contigs.fasta")
        shutil.copy(contig_file, os.path.join(self.contig_out, self.accession + ".fa"))
