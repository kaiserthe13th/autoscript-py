import yaml
from util import err, argv
from os import path
realpath = path.realpath

class Import:
    def __init__(self, visited, prog, exec_time, repeat_time):
        self.visited, self.prog, self.exec_time, self.repeat_time = (
            visited, prog, exec_time, repeat_time
        )

class Importer:
    def __init__(self, loc: str, visited: list):
        self.loc = loc
        self.visited = visited
    
    def import_(self, exec_time, repeat_time):
        try:
            with open(self.loc) as f:
                src = yaml.safe_load(f.read())
                progs_ = src.get('prog')
                if not progs_ and progs_ != []:
                    err('`prog` for script not provided')
                    exit(1)
                exec_time = src.get('time') or exec_time
                repeat_time = src.get('repeat') or repeat_time
                imports = src.get('import')
                if imports:
                    if isinstance(imports, str):
                        if realpath(imports) not in self.visited:
                            imported = Importer(realpath(imports), self.visited + [realpath(imports)]).import_()
                            progs_ += imported.prog
                            self.visited += imported.visited
                    elif isinstance(imports, list):
                        for i in imports:
                            if realpath(i) not in self.visited:
                                imported = Importer(realpath(i), self.visited + [realpath(i)]).import_()
                                progs_ += imported.prog
        except FileNotFoundError as e:
            err(f'script at `{self.loc}` not found? maybe you need to create it. run `{argv[0]} --init` to initialize a script')
            exit(1)
        return Import(self.visited, progs_, exec_time, repeat_time)
