import re
import cmd
from typing import Optional
from zviewer.api import ZendeskService, ZendeskServiceError

class ZViewerShell(cmd.Cmd):
    intro = 'Welcome to Zendesk Viewer (zviewer).\nType help or ? to list commands.\n'
    prompt= '(zendesk) '

    def __init__(self, api_service: ZendeskService) -> None:
        self.api_service = api_service
        self.truncate_threshold = 50
        # credit: https://stackoverflow.com/a/39520512
        self.aliases = {'e': self.do_exit,
                        'q': self.do_quit,
                        'h': self.do_help}

        super().__init__()

    def do_tickets(self, _args):
        try:
            tickets = self.api_service.list_tickets()
            start = 0
            viewing = True
            while viewing:
                print("+"+"-"*60+"+")
                for ticket in tickets[start:start+25]:
                    self._preview_ticket(ticket)
                    print("+"+"-"*60+"+")

                if len(tickets) > 25:
                    c = input(f"\nTickets {start+1}..{min(start+25,len(tickets))}/{len(tickets)}, press:\n\t(n) next page\n\t(p) prev page\n\t(q) to quit\n\t\n")
                    if c.startswith('n') or not c:
                        start = min(len(tickets)-25, start+25)
                    elif c.startswith('p'):
                        start = max(0, start-25)
                    elif c.startswith('q'):
                        viewing = False
                print("")

        except ZendeskServiceError as e:
            print(f"ZendeskServiceError: {e}")

    def do_ticket(self, args):
        try:
            args = args.split()
            if not args:
                print("Usage: ticket id/id_range [id/id_range] ... ")
            id_ranges = []
            for param in args:
                id_range = self._id_range(param)
                if id_range:
                    id_ranges.append(id_range)
                else:
                    print(f"id_range: '{param}' is invalid")
            
            ticket_ids = [
                id 
                for _range in id_ranges
                for id in range(_range[0], _range[1]+1)
            ]
            self._display_tickets(ticket_ids)

        except ZendeskServiceError as e:
            print(f"ZendeskServiceError: {e}")

    def _id_range(self, param: str) -> Optional[tuple[int, int]]:
        if param.isdigit():
            return (int(param), int(param))
        elif re.match(r'^\d+-\d+$', param):
            start, end = map(int, param.split('-'))
            if start <= end:
                return (start, end)
            else:
                return None
        else:
            return None

    def do_exit(self, args):
        return True

    def do_quit(self, args):
        return True

    # credit: https://stackoverflow.com/a/39520512
    def default(self, line):
        cmd, arg, line = self.parseline(line)
        if cmd and cmd in self.aliases:
            return self.aliases[cmd](arg)
        else:
            print(f"*** Unknown syntax: {line}")
    
    def _truncate(self, s: str) -> str:
        if len(s) <= self.truncate_threshold:
            return s
        else:
            return s[:47]+'...'
    
    def _preview_ticket(self, ticket) -> None:
        print(f"Ticket #{ticket['id']}")
        print(f"Subject: {self._truncate(ticket['subject'])}")
        print(f"Description:\n{self._truncate(ticket['description'])}")
    
    def _display_tickets(self, ticket_ids: list[int]) -> None:
        print("")
        if not ticket_ids:
            return
        elif len(ticket_ids) == 1:
            ticket_id = ticket_ids[0]
            ticket = self.api_service.get_ticket(ticket_id)
            if not ticket:
                print(f"Ticket #{ticket_id} not found.")
            else:
                self._print_ticket(ticket)
            print("")
        else:
            retrieved = set()
            requested = set(ticket_ids)
            tickets = self.api_service.get_tickets(ticket_ids)
            for ticket in tickets:
                retrieved.add(ticket['id'])
                self._print_ticket(ticket)
                print("")
            not_found = requested.difference(retrieved) 
            if not_found:
                print(f"Tickets {','.join(['#'+str(i) for i in not_found])} not found")

    def _print_ticket(self, ticket):
        print(f"Ticket #{ticket['id']}")
        print(f"Subject: {ticket['subject']}")
        print(f"Description:\n{ticket['description']}")
        print("")
        print(f"View ticket: [{self._ticket_to_url(ticket)}]")
    
    def _ticket_to_url(self, ticket) -> str:
        url = self.api_service.get_url()
        return f"{url}/agent/tickets/{ticket['id']}"