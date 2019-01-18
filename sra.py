from urllib.request import urlopen
from urllib.error import URLError
import subprocess

import wget


class SequenceReadArchive:
    @staticmethod
    def split(sra_file, out_path):
        cmd = ["fastq-dump", sra_file, '--gzip', '--outdir', out_path, '--split-files']
        subprocess.call(cmd, stdout=subprocess.DEVNULL)

    @staticmethod
    def getURL(accession):
        url = 'ftp://ftp.ncbi.nlm.nih.gov/sra/sra-instant/reads/ByRun/sra/{}/{}/{}/{}'.format(
            accession[0:3], accession[0:6], accession, accession + '.sra')
        return url

    @staticmethod
    def checkURL(url):
        try:
            urlopen(url)
            return True
        except URLError:
            return False

    @staticmethod
    def download(url, save_path):
        file_path = wget.download(url=url, out=save_path)
        return file_path

