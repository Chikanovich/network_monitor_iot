# core imports
from django.utils import timezone
import json
from typing import List

# 3rd party imports
import nmap3
subprocess.call('dir', shell=True)

# local imports
from monitor.models import NetworkUsage

# typedef
NetworkItems = List[NetworkUsage]

scanner = nmap3.NmapScanTechniques()

# TODO: change to your address
# run ipconfig in terminal and find IPv4 address
# leave /24 at the end
ADDR_SPACE = '192.168.1.1/24'


def run_scan():
    print('running scan')
    results = scanner.nmap_ping_scan(ADDR_SPACE)

    mapped = [NetworkUsage(
        date_created=timezone.now(),
        ip_address=[addr['addr']
                    for addr in entry['addresses'] if addr['addrtype'] == 'ipv4'],
        vendor=[addr['vendor'] for addr in entry['addresses'] if addr['addrtype'] == 'mac'])
        for entry in results]

    print('collected')

    bulk_insert(mapped)


def bulk_insert(items: NetworkItems):
    # [print(f'{x.vendor} - {x.ip_address}') for x in items if x.vendor]

    print('insert')
    # inserts all found clients where vendor is not empty string
    NetworkUsage.objects.bulk_create([item for item in items if item.vendor])
