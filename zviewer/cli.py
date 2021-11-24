import cmd
import zviewer

class ZViewerShell(cmd.Cmd):
    intro = 'Welcome to Zendesk Viewer (zviewer).\nType help or ? to list commands.\n'
    prompt= '(zendesk) '

    def do_connect(self, args):
        raise NotImplementedError

    def do_tickets(self, args):
        raise NotImplementedError

    def do_ticket(self, args):
        raise NotImplementedError

    def do_exit(self, args):
        return True

    def do_quit(self, args):
        return True

def parse(arg):
    return tuple(map(int, arg.split()))
