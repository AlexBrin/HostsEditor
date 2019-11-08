#!/usr/bin/python3
from terminaltables import AsciiTable
from argparse import ArgumentParser
import os
import sys
from hostseditor import color, log

VERSION = '1.0.1'


def _readline(placeholder, default):
    try:
        return input(color.YELLOW + ' + ' + placeholder + color.BLUE + ' (' + default + ')' + color.NULL + ': ') \
               or default
    except KeyboardInterrupt as exception:
        log.error(str(exception))
        sys.exit(0)


class Editor:

    def _init(self):
        self.os = None
        self.file = None
        self.comments = []
        self.hosts = {}
        self.exit = False
        self.command = False

    @staticmethod
    def get_current_os():
        if sys.platform.startswith('win'):
            os_num = '2'
        elif os.getenv('WSL_DISTRO_NAME', None) or os.getenv('WSLENV', None):
            os_num = '3'
        else:
            os_num = '1'

        os_list = {
            '1': "linux",
            '2': "windows",
            '3': "wsl"
        }

        return os_list[os_num]

    @staticmethod
    def _get_hosts_path(os_code):
        host_paths = {
            "windows": "C:\\Windows\\System32\\drivers\\etc\\hosts",
            "linux": "/etc/hosts",
            "wsl": "/mnt/c/Windows/System32/drivers/etc/hosts"
        }

        if os_code not in host_paths:
            log.error("Invalid name of the operating system")
            sys.exit(0)

        return host_paths[os_code]

    def _load_hosts_file(self):
        self.file = open(Editor._get_hosts_path(self.os), 'r+')

        for line in self.file:
            line = line.replace("\n", '', -1)

            if not line or line[0] == '#':
                if line.find('HostsEditor') == -1:
                    self.comments.append(line)
                continue

            line = line.split(' ')
            if len(line) < 2:
                continue

            self.hosts[line[1]] = line[0]

    def _select_system(self):
        self.os = Editor.get_current_os()

    def _parse_args(self):
        parser = ArgumentParser(description="Simple hosts file editor")
        parser.add_argument('-a', '--add', type=str, help="Add domain", metavar='domain')
        parser.add_argument('-rm', '--remove', type=str, help="Remove domain", metavar='domain')
        parser.add_argument('-list', '--list', help="Print a table of domain and IP addresses", action="store_true")
        parser.add_argument('--raw', help="Print a raw data of domain and IP addresses (please, use with `-list`)",
                            action="store_true")
        parser.add_argument('--ip', type=str, help="IP for the specified domain (please, use with `-a`)",
                            metavar='IP')
        parser.add_argument('-v', '--version', action="version", version="HostsEditor " + VERSION,
                            help="Print version")
        args = parser.parse_args()

        if args.add is not None:
            if args.ip is not None:
                ip = args.ip
            else:
                ip = '127.0.0.1'

            self.add(args.add, ip)
            print("Host `" + args.add + "` (" + ip + ") has been added")
        elif args.remove is not None:
            self.remove(args.remove)
            print("Host `" + args.remove + "` has been deleted")
        elif args.list:
            if args.raw:
                for host in self.hosts:
                    print(host + " " + self.hosts[host])
            else:
                self.print_hosts_list()
        else:
            return

        self.update_file()

        self.command = True
        
    def get_os(self):
        return self.os

    def update_file(self):
        hosts = self.comments.copy()

        hosts.append("# <HostsEditor>\n")
        for host in self.hosts:
            hosts.append(self.hosts[host] + " " + host)
        hosts.append("\n# </HostsEditor>")

        f = open(self._get_hosts_path(self.os), 'w')
        f.write("\n".join(hosts))
        f.close()

    def __init__(self):
        self._init()
        self._select_system()
        self._load_hosts_file()
        self._parse_args()

    def _exit(self):
        self.exit = True
        self.update_file()

    def add(self, host, ip='127.0.0.1'):
        self.hosts[host] = ip
        return True

    def _add(self):
        host = readline("Host", "localhost")
        ip = readline("IP", "127.0.0.1")
        self.add(host, ip)
        log.info("Host `" + host + "` (" + ip + ") has been added")

    def remove(self, host):
        if host not in self.hosts:
            return False

        del self.hosts[host]
        return True

    def _remove(self):
        host = readline("Host", "localhost")
        self.remove(host)
        log.info("Host `" + host + "` has been deleted")

    def get_hosts_list(self):
        return self.hosts

    def print_hosts_list(self):
        table_data = [
            ["Hostname", "IP"]
        ]

        for host in self.hosts:
            table_data.append([host, self.hosts[host]])

        print(AsciiTable(table_data).table)

    def _wait_input(self):
        log.info("1. Host list")
        log.info("2. Add host")
        log.info("3. Delete host")
        log.info("0. Exit")

        action_list = {
            '0': self._exit,
            '1': self.print_hosts_list,
            '2': self._add,
            '3': self._remove
        }
        action = readline("Action", '1')

        if action not in action_list:
            log.error("Unknown action")
            return

        action_list[action]()

    def run(self):
        while not self.command:
            if self.exit:
                log.info("Bye")
                sys.exit(0)

            self._wait_input()


if __name__ == '__main__':
    Editor().run()
