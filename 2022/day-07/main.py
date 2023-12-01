import sys

class CommandExecution:
    def __init__(self, command, output):
        self.command = command
        self.output = output

    def __str__(self):
        return '\n'.join([f'$ {self.command}'] + self.output)

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def __str__(self):
        return self.to_string(depth=0)

    def to_string(self, depth):
        return (depth * '  ') + f'- {self.name} (file, size={self.size})\n'


class Dir:
    def __init__(self, name):
        self.name = name
        self.files = {}

    def add_file(self, file):
        self.files[file.name] = file

    def get_dir(self, name):
        return self.files.setdefault(name, Dir(name))

    @property
    def size(self):
        return sum(f.size for f in self.files.values())

    def __str__(self):
        return self.to_string(depth=0)

    def to_string(self, depth):
        s = [(depth * '  ') + f'- {self.name} (dir)\n']
        for f in sorted(self.files.values(), key=lambda f: f.name):
            s.append(f.to_string(depth + 1))
        return ''.join(s)

    def get_child_directories(self):
        for f in sorted(self.files.values(), key=lambda x: x.name):
            if type(f) is Dir:
                yield f
                yield from f.get_child_directories()


def input_to_command_history(lines):
    cur_command = ''
    cur_output = []
    commands = []
    for line in lines:
        if line.startswith('$ '):
            if cur_command:
                commands.append(CommandExecution(cur_command, cur_output))
            cur_command = line[2:]
            cur_output = []
        elif cur_command:
            cur_output.append(line)
        else:
            raise Exception(f"Got unknown content: {line!r} (not a command and no current command to add output for)")

    commands.append(CommandExecution(cur_command, cur_output))

    return commands


def parse_ls_output(d, ls_output):
    for line in ls_output:
        if line.startswith('dir '):
            dir_name = line[4:]
            yield Dir(dir_name)
        else:
            size, fname = line.split(' ', 1)
            size = int(size)
            yield File(fname, size)

def main(input_file):
    lines = []
    for line in input_file.readlines():
        line = line.strip()
        if not line:
            continue
        lines.append(line)

    commands = input_to_command_history(lines)

    cwd = root = Dir('/')
    dir_stack = [root]
    for c in commands:
        if c.command.startswith('cd '):
            assert len(c.output) == 0
            dir_name = c.command[3:]
            if dir_name == '..':
                cwd = dir_stack.pop()
            elif dir_name == '/':
                cwd = root
                dir_stack = []
            else:
                dir_stack.append(cwd)
                cwd = cwd.get_dir(dir_name)
        elif c.command.startswith('ls'):
            for f in parse_ls_output(cwd, c.output):
                cwd.add_file(f)

    print(root)

    small_dirs = [d for d in root.get_child_directories() if d.size <= 100000]
    print(sum(d.size for d in small_dirs))

    disk_size = 70000000
    free_disk = disk_size - root.size

    for dir in reversed(list(root.get_child_directories())):
        if (free_disk + dir.size) >= 30000000:
            print(dir.size)
            break

if __name__ == "__main__":
    main(sys.stdin)
