#!/usr/bin/env python3

import os
import argparse
import json
import webbrowser

# suprisingly this works in PyPi, but not locally. For local usage replace ".lib." with "lib."
from .lib.config import Config
from .lib.servers import Servers
from .lib.sites import Sites
from .lib.tokens import Tokens
from .lib.statistics import Statistics

__version__ = '1.0.3'

cfg = Config(__version__)
cli = argparse.ArgumentParser(prog='sleurencli', description='CLI for Sleuren Monitoring')
cli_subcommands = dict()

def check_columns(columns):
    """Show or hide columns in ASCII table view"""
    for column in columns:
        if '0id' == column.lower():
            cfg.hide_ids = True
        elif 'id' == column.lower():
            cfg.hide_ids = False

# --- config functions ---

def config_print(args):
    """Sub command for config print"""
    cfg.print()

def config_save(args):
    """Sub command for config save"""
    if args.api_key:
        cfg.api_key = args.api_key

    cfg.saveToFile()

def config(args):
    """Sub command for config"""
    config_print(args)

# --- dashboard functions ---

def dashboard(args):
    """Sub command for dashboard"""
    webbrowser.open('https://sleuren.com/dashboard')

# --- servers functions ---

def servers_add(args):
    """Sub command for servers add"""
    tokens = Tokens(cfg)
    token = tokens.token()
    if not token:
        print('First create a user token by executing:')
        print()
        print('sleurencli tokens create')
        print('sleurencli tokens list')
        print()
        token = '[YOUR_PROJECT_TOKEN]'

    print('Please login via SSH to each of the servers you would like to add and execute the following command:')
    print()
    print('wget -q -N sleuren.com/sleuren.sh && bash sleuren.sh', token)

def servers_list(args):
    """Sub command for servers list"""
    check_columns(args.columns)
    servers = Servers(cfg)
    servers.format = args.output
    servers.list(args.issues, args.sort, args.reverse, args.limit, args.tag)

def servers_remove(args):
    """Sub command for servers remove"""
    print("Please login via SSH to each of the servers you would like to remove.")
    print("First stop the monitoring agent by running \"service sleuren stop\" then run \"pip3 uninstall sleuren\". After 15 minutes you are able to remove the server.")

def servers_update(args):
    """Sub command for servers update"""
    servers = Servers(cfg)
    pattern = ''
    if args.id:
        pattern = args.id
    elif args.name:
        pattern = args.name
    servers.setTags(pattern, args.tag)

def servers(args):
    """Sub command for servers"""
    cli_subcommands[args.subparser].print_help()

# --- signup functions ---

def signup(args):
    """Sub command for signup"""
    webbrowser.open('https://sleuren.com')

# --- sites functions ---

def sites_add(args):
    """Sub command for sites add"""
    sites = Sites(cfg)

    if args.file:
        if os.path.isfile(args.file):
            with open(args.file) as file:
                lines = file.readlines()
                for line in lines:
                    sites.add(line.strip())
        else:
            print('ERROR: File', args.file, 'to import not found')
    elif args.url:
        sites.add(args.url, protocol=args.protocol, name=args.name, force=args.force)
    else:
        print('You need to specify at least a name with --name [name]')

def sites_list(args):
    """Sub command for sites list"""
    check_columns(args.columns)
    sites = Sites(cfg)
    sites.format = args.output
    sites.list(id=args.id, url=args.url, name=args.name, location=args.location, pattern=args.pattern, issuesOnly=args.issues, sort=args.sort, reverse=args.reverse, limit=args.limit)

def sites_remove(args):
    """Sub command for sites remove"""
    sites = Sites(cfg)
    sites.remove(id=args.id, url=args.url, name=args.name, location=args.location, pattern=args.pattern)

def sites(args):
    """Sub command for sites"""
    cli_subcommands[args.subparser].print_help()

# --- statistics functions ---

def statistics(args):
    """Sub command for statistics"""
    statistics = Statistics(cfg)
    statistics.print(format=args.output)

# --- tokens functions ---

def tokens_create(args):
    """Sub command for tokens create"""
    tokens = Tokens(cfg)
    tokens.create()

def tokens_list(args):
    """Sub command for tokens list"""
    tokens = Tokens(cfg)
    tokens.list(format=args.output)

def tokens(args):
    """Sub command for tokens"""
    cli_subcommands[args.subparser].print_help()

def performCLI():
    """Parse the command line parameters and call the related functions"""

    subparsers = cli.add_subparsers(title='commands', dest='subparser')
    cli.add_argument('-v', '--version', action='store_true', help='print CLI version')

    # config

    cli_config = subparsers.add_parser('config', help='configure connection to sleuren account')
    cli_config.set_defaults(func=config)

    config_subparsers = cli_config.add_subparsers(title='commands', dest='subparser')

    cli_config_print = config_subparsers.add_parser('print', help='print current settings for Sleuren')
    cli_config_print.set_defaults(func=config_print)

    cli_config_save = config_subparsers.add_parser('save', help='save current settings for Sleuren to ' + cfg.filename)
    cli_config_save.set_defaults(func=config_save)
    cli_config_save.add_argument('-a', '--api-key', metavar='key', help='specify your API KEY for Sleuren')


    # dashboard

    cli_dashboard = subparsers.add_parser('dashboard', help='open Sleuren Dashboard in your Web Browser')
    cli_dashboard.set_defaults(func=dashboard)

    # servers

    cli_servers = subparsers.add_parser('servers', help='list and manage monitored servers')
    cli_servers.set_defaults(func=servers)
    cli_servers_subparsers = cli_servers.add_subparsers(title='commands', dest='subparser')

    cli_servers_add = cli_servers_subparsers.add_parser('add', help='activate monitoring for a server')
    cli_servers_add.set_defaults(func=servers_add)

    cli_servers_list = cli_servers_subparsers.add_parser('list', help='list monitored servers')
    cli_servers_list.set_defaults(func=servers_list)
    cli_servers_list.add_argument('--id', nargs='?', default='', metavar='id', help='update server with given ID')
    cli_servers_list.add_argument('--name', nargs='?', default='', metavar='name', help='update server with given name')
    cli_servers_list.add_argument('--tag', nargs='*', default='', metavar='tag', help='only list servers matching these tags')
    cli_servers_list.add_argument('--issues', action='store_true', help='show only servers with issues')

    cli_servers_list.add_argument('--columns', nargs='*', default='', metavar='col', help='specify columns to print in table view or remove columns with 0 as prefix e.g. "0id"')
    cli_servers_list.add_argument('--sort', nargs='?', default='', metavar='col', help='sort by specified column. Reverse sort by adding --reverse')
    cli_servers_list.add_argument('--reverse', action='store_true', help='show in descending order. Works only together with --sort')
    cli_servers_list.add_argument('--limit', nargs='?', default=0, type=int, metavar='n', help='limit the number of printed items')

    cli_servers_list.add_argument('--output', choices=['json', 'csv', 'table'], default='table', help='output format for the data')
    cli_servers_list.add_argument('--json', action='store_const', const='json', dest='output', help='print data in JSON format')
    cli_servers_list.add_argument('--csv', action='store_const', const='csv', dest='output', help='print data in CSV format')
    cli_servers_list.add_argument('--table', action='store_const', const='table', dest='output', help='print data as ASCII table')

    cli_servers_remove = cli_servers_subparsers.add_parser('remove', help='remove monitoring for a server')
    cli_servers_remove.set_defaults(func=servers_remove)

    cli_servers_update = cli_servers_subparsers.add_parser('update', help='set tags for a server')
    cli_servers_update.set_defaults(func=servers_update)
    cli_servers_update.add_argument('--id', nargs='?', default='', metavar='id', help='update server with given ID')
    cli_servers_update.add_argument('--name', nargs='?', default='', metavar='name', help='update server with given name')
    cli_servers_update.add_argument('--tag', nargs='*', default='', metavar='tag', help='set these tags for one or more servers specified')

    # signup

    cli_signup = subparsers.add_parser('signup', help='sign up for Sleuren')
    cli_signup.set_defaults(func=signup)

    # sites

    cli_sites = subparsers.add_parser('sites', help='list and manage monitored websites')
    cli_sites.set_defaults(func=sites)
    cli_sites_subparsers = cli_sites.add_subparsers(title='commands', dest='subparser')

    cli_sites_add = cli_sites_subparsers.add_parser('add', help='activate monitoring for a site')
    cli_sites_add.set_defaults(func=sites_add)
    cli_sites_add.add_argument('--url', nargs='?', metavar='url', help='url of site that should be monitored')
    cli_sites_add.add_argument('--name', nargs='?', metavar='name', help='name of site that should be monitored (optional)')
    cli_sites_add.add_argument('--protocol', nargs='?', default='https', metavar='protocol', help='specify a different protocol than https')
#    cli_sites_add.add_argument('--port', nargs='?', default=443, type=int, metavar='port', help='specify a different port than 443')
    cli_sites_add.add_argument('--force', action='store_true', help='add new monitor even if already exists')
    cli_sites_add.add_argument('--file', nargs='?', default='', metavar='file', help='file containing one URL per line to monitor')

    cli_sites_list = cli_sites_subparsers.add_parser('list', help='list sites')
    cli_sites_list.set_defaults(func=sites_list)
    cli_sites_list.add_argument('--id', nargs='?', default='', metavar='id', help='list site with given ID')
    cli_sites_list.add_argument('--url', nargs='?', default='', metavar='url', help='list site with given url')
    cli_sites_list.add_argument('--name', nargs='?', default='', metavar='name', help='list site with given name')
    cli_sites_list.add_argument('--location', nargs='?', default='', metavar='location', help='list sites monitored from given location')
    cli_sites_list.add_argument('--pattern', nargs='?', default='', metavar='pattern', help='list sites with pattern included in URL')
    cli_sites_list.add_argument('--issues', action='store_true', help='show only sites with issues')

    cli_sites_list.add_argument('--columns', nargs='*', default='', metavar='col', help='specify columns to print in table view or remove columns with 0 as prefix e.g. "0id"')
    cli_sites_list.add_argument('--sort', nargs='?', default='', metavar='col', help='sort by specified column. Reverse sort by adding --reverse')
    cli_sites_list.add_argument('--reverse', action='store_true', help='show in descending order. Works only together with --sort')
    cli_sites_list.add_argument('--limit', nargs='?', default=0, type=int, metavar='n', help='limit the number of printed items')

    cli_sites_list.add_argument('--output', choices=['json', 'csv', 'table'], default='table', help='output format for the data')
    cli_sites_list.add_argument('--json', action='store_const', const='json', dest='output', help='print data in JSON format')
    cli_sites_list.add_argument('--csv', action='store_const', const='csv', dest='output', help='print data in CSV format')
    cli_sites_list.add_argument('--table', action='store_const', const='table', dest='output', help='print data as ASCII table')

    cli_sites_remove = cli_sites_subparsers.add_parser('remove', help='remove a contact')
    cli_sites_remove.set_defaults(func=sites_remove)
    cli_sites_remove.add_argument('--id', nargs='?', default='', metavar='id', help='remove site with given ID')
    cli_sites_remove.add_argument('--url', nargs='?', default='', metavar='url', help='remove site with given url')
    cli_sites_remove.add_argument('--name', nargs='?', default='', metavar='name', help='remove site with given name')
    cli_sites_remove.add_argument('--location', nargs='?', default='', metavar='location', help='remove sites monitored from given location')
    cli_sites_remove.add_argument('--pattern', nargs='?', default='', metavar='pattern', help='remove sites with pattern included in URL')

    # statistics

    cli_statistics = subparsers.add_parser('statistics', help='print statistics')
    cli_statistics.set_defaults(func=statistics)
    cli_statistics.add_argument('--output', choices=['csv', 'table'], default='table', help='output format for the data')
    cli_statistics.add_argument('--csv', action='store_const', const='csv', dest='output', help='print data in CSV format')
    cli_statistics.add_argument('--table', action='store_const', const='table', dest='output', help='print data as ASCII table')

    # user tokens

    cli_tokens = subparsers.add_parser('tokens', help='list or create tokens')
    cli_tokens.set_defaults(func=tokens)
    cli_tokens_subparsers = cli_tokens.add_subparsers(title='commands', dest='subparser')

    cli_tokens_create = cli_tokens_subparsers.add_parser('create', help='create new user token')
    cli_tokens_create.set_defaults(func=tokens_create)

    cli_tokens_list = cli_tokens_subparsers.add_parser('list', help='list tokens')
    cli_tokens_list.set_defaults(func=tokens_list)
    cli_tokens_list.add_argument('--output', choices=['json', 'csv', 'table'], default='table', help='output format for the data')
    cli_tokens_list.add_argument('--json', action='store_const', const='json', dest='output', help='print data in JSON format')
    cli_tokens_list.add_argument('--csv', action='store_const', const='csv', dest='output', help='print data in CSV format')
    cli_tokens_list.add_argument('--table', action='store_const', const='table', dest='output', help='print data as ASCII table')

    # Parse
    cli_subcommands['config'] = cli_config
    cli_subcommands['dashboard'] = cli_dashboard
    cli_subcommands['servers'] = cli_servers
    cli_subcommands['signup'] = cli_signup
    cli_subcommands['sites'] = cli_sites
    cli_subcommands['statistics'] = cli_statistics
    cli_subcommands['tokens'] = cli_tokens

    args = cli.parse_args()
    if args.subparser == None:
        if args.version:
            print('Sleuren CLI Version:', __version__)
        elif 'func' in args:
            # statistics, signup and dashboard is shown directly without subparser
            if args.func == config:
                cli_config.print_help()
            elif args.func == servers:
                cli_servers.print_help()
            elif args.func == sites:
                cli_sites.print_help()
            elif args.func == tokens:
                cli_tokens.print_help()
            else:
                cli.print_help()
        else:
            cli.print_help()
    else:
        args.func(args)

def main():
    performCLI()

if __name__ == '__main__':
    main()
