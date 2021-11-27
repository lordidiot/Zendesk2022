import argparse
from re import L
from zviewer.cli import ZViewerShell
from zviewer.api import ZendeskService

def main():
    parser = argparse.ArgumentParser(description='Ticket Viewer for Zendesk API.',
                                     allow_abbrev=True)
    parser.add_argument('subdomain', type=str,
                        help='subdomain for your Zendesk workspace')
    parser.add_argument('--user', '-u', type=str, help='username', required=True)
    parser.add_argument('--pass', '-p', type=str, help='password', required=True)
    args = parser.parse_args()
    args = vars(args)
    api_service = ZendeskService(args['subdomain'],
                                 args['user'], args['pass'])
    ZViewerShell(api_service).cmdloop()

if __name__ == '__main__':
    main()
