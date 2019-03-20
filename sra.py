import os
import subprocess


class SequenceReadArchive:
    def __init__(self, accession, outdir):
        self.accession = accession
        self.outdir = os.path.join(outdir, 'SRA')
        self.url = None
        self.sra_file = os.path.join(self.outdir, self.accession + '.sra')
        self.fastq_dir = os.path.join(outdir, 'Fastq', self.accession)
        os.makedirs(self.outdir, exist_ok=True)
        os.makedirs(self.fastq_dir, exist_ok=True)

    def make_url(self):
        url = 'ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/{}/{}/{}/{}'.format(
            self.accession[0:3], self.accession[0:6], self.accession, self.accession + '.sra')
        self.url = url

    def download(self):
        subprocess.call(['wget', self.url, '-O', self.sra_file], stderr=subprocess.DEVNULL)

    def split(self):
        cmd = ["fastq-dump", self.sra_file, '--outdir', self.fastq_dir, '--split-files', '--gzip']
        subprocess.call(cmd, stdout=subprocess.DEVNULL)

    def remove(self):
        os.remove(self.sra_file)
