from typing import *
from uuid import uuid4
from tempfile import gettempdir
from pathlib import Path
import os
import time
import subprocess
import multiprocessing as mp


class Process:
    """
        A class to manage processes with methods to start, stop, restart, and join them.
        Processes are identified by a name and a list of commands to execute.
        The class also handles cleanup upon deletion, including killing the process and removing temporary files.
    """
    
    def __init__(self, name: str, command: List[str]):
        self.name = name
        self.command = command
        self.run_process: subprocess.Popen = None
        self.uuid: str = uuid4().__str__()
        self.path_stdout = Path(gettempdir()) / f'{self.uuid}-stdout.txt'
        self.path_stderr = Path(gettempdir()) / f'{self.uuid}-stderr.txt'

    
    def run(self) -> subprocess.Popen:
        return subprocess.Popen(
            self.command,
            text=True,
            shell=True,
            stdout=open(f'{self.path_stdout}', 'w+', encoding='utf-8'),
            stderr=open(f'{self.path_stderr}', 'w+', encoding='utf-8'),
        )

    def start(self) -> None:
        self.run_process = self.run()

    def stop(self) -> None:
        self.run_process.terminate()
    
    def kill(self) -> None:
        self.run_process.kill()
    
    def join(self, timeout:int=None) -> None:
        self.run_process.wait(timeout)

    def restart(self) -> None:
        self.kill()
        self.start()

    def __str__(self) -> str:
        return f"Process(name={self.name}, commands={self.commands})"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Process):
            return False
        return self.name == other.name
    
    def __hash__(self) -> int:
        return hash(self.name)
    
    def __del__(self):
        try: self.kill()
        except NotImplementedError: pass

        try: os.remove(self.path_stderr)
        except Exception as exc: 
            raise Warning(f'The temporary file(stderr) could not be deleted, Exption: {exc.__class__.__name__}')
        
        try: os.remove(self.path_stdout)
        except Exception as exc: 
            raise Warning(f'The temporary file(stdout) could not be deleted, Exption: {exc.__class__.__name__}')