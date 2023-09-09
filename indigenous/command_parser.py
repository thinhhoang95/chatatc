def parse_command(command):
    # Given a command in the format of command_name(arg1, arg2, ...), return a tuple of (command_name, [arg1, arg2, ...])
    command = command.strip()
    command_name = command.split('(')[0]
    args = command.split('(')[1].split(')')[0].split(',')
    args = [arg.strip() for arg in args]
    # Remove all ' or " in args
    args = [arg.replace("'", "").replace('"', '') for arg in args]
    return command_name, args