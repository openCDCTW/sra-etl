from urllib.request import urlopen
from urllib.error import URLError
import subprocess

import wget


class SequenceReadArchive:
    @staticmethod
    def split(sra_file, out):
        cmd = ["fastq-dump", sra_file, '--gzip', '--outdir', out, '--split-files']
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
    def download(url, out):
        file_path = wget.download(url=url, out=out)
        return file_path

