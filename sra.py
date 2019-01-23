import os
import subprocess
import wget


class SequenceReadArchive:
    def __init__(self, accession, outdir):
        self.accession = accession
        self.outdir = outdir
        self.url = None
        self.sra_file = None
        self.fastq_dir = None

    def make_url(self):
        url = 'ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/{}/{}/{}/{}'.format(
            self.accession[0:3], self.accession[0:6], self.accession, self.accession + '.sra')
        self.url = url

    def download(self):
        out = os.path.join(self.outdir, 'SRA')
        os.makedirs(out, exist_ok=True)
        self.sra_file = wget.download(url=self.url, out=out)

    def split(self):
        out = os.path.join(self.out, 'FastQC', self.accession)
        os.makedirs(out)
        cmd = ["fastq-dump", self.sra_file, '--gzip', '--outdir', out, '--split-files']
        subprocess.call(cmd, stdout=subprocess.DEVNULL)
        self.fastq_dir = out

    def remove(self):
        os.remove(self.sra_file)
