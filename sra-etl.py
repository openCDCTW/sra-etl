import subprocess
from concurrent.futures import ProcessPoolExecutor
import click


@click.command()
@click.argument('SRA_List', type=click.Path(exists=True))
@click.argument('out', type=click.Path(exists=True))
@click.option('--database', default=False)
@click.option('--parallel', '-p', is_flag=True, help='Run by multiprocess')
def main(sra_list, out, database, parallel):
    with open(sra_list, 'r') as file:
        sra_list = file.read()
    sra_list = sra_list.splitlines()

    cmds = []
    for item in sra_list:
        if database:
            cmd = ['python', 'core.py', item, out, '--database', database]
            cmds.append(cmd)
        else:
            cmd = ['python', 'core.py', item, out]
            cmds.append(cmd)

    if parallel:
        with ProcessPoolExecutor(4) as executor:
            executor.map(subprocess.call, cmds)
    else:
        for cmd in cmds:
            subprocess.call(cmd)


if __name__ == '__main__':
    main()

