import logging
import subprocess

def run(cmd, do_check=True, do_shell=False, get_out=False):
    '''

    Args:
        cmd: command list to run, or command string if do_shell == True
        do_check: throw CalledProcessError when exit code != 0
        do_shell: interpret command as shell command
        get_out: return output

    Returns:

    '''
    if isinstance(cmd, list):
        cmd_str = ' '.join(cmd)
    elif isinstance(cmd, str):
        cmd_str = cmd
    logging.debug(cmd_str)

    if get_out:
        return subprocess.run(cmd, check=do_check, shell=do_shell, stdout=subprocess.PIPE).stdout
    else:
        subprocess.run(cmd, check=do_check, shell=do_shell)

def kill(pid):
    run(['kill', '-KILL', str(pid)])

def sleep(secs):
    run(['sleep', secs])