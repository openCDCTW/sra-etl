import sys

sys.path.append('/home/chen1i6c04/Projects/Benga')
from src.algorithms import profiling


def profile(input_dir, output_dir, database, threads=1, occrrence=95):
    profiling.profiling(output_dir, input_dir, database, threads=threads, occr_level=occrrence,
                        enable_adding_new_alleles=(not False), generate_profiles=(not False),
                        debug=False)