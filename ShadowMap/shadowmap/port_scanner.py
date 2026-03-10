import subprocess
import xml.etree.ElementTree as ET
import urllib.parse
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class PortScanner:
    def __init__(self, alive_hosts: List[Dict]):
        self.alive_hosts = alive_hosts

    def scan(self) -> Dict[str, List[int]]:
        """
        Scans the alive hosts and returns a dictionary mapping
        hostname -> list of open ports.
        """
        # First, extract unique hostnames
        hosts_to_scan = set()
        for host in self.alive_hosts:
            url = host.get("url", "")
            if url:
                parsed = urllib.parse.urlparse(url)
                if parsed.hostname:
                    hosts_to_scan.add(parsed.hostname)
        
        results = {}
        for host in hosts_to_scan:
            open_ports = self._scan_host(host)
            results[host] = open_ports
            
        return results

    def _scan_host(self, host: str) -> List[int]:
        open_ports = []
        logger.info(f"[*] Executing nmap scan on {host}")
        try:
            # -T4 (timing), -F (fast scan: 100 ports), -Pn (no ping)
            # Output in XML format to stdout
            proc = subprocess.run(
                ['nmap', '-T4', '-F', '-Pn', '-oX', '-', host],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            if proc.stdout:
                open_ports = self._parse_nmap_xml(proc.stdout)
                logger.info(f"[+] nmap found {len(open_ports)} open ports on {host}: {open_ports}")
            else:
                logger.warning(f"[-] nmap returned no output for {host}.")
        except FileNotFoundError:
            logger.error("[-] nmap not found. Please ensure nmap is installed and in your PATH.")
        except Exception as e:
            logger.error(f"[-] Error running nmap on {host}: {e}")
            
        return open_ports

    def _parse_nmap_xml(self, xml_output: str) -> List[int]:
        open_ports = []
        try:
            root = ET.fromstring(xml_output)
            for host in root.findall('host'):
                ports = host.find('ports')
                if ports:
                    for port in ports.findall('port'):
                        state = port.find('state')
                        if state is not None and state.get('state') == 'open':
                            port_id = port.get('portid')
                            if port_id:
                                open_ports.append(int(port_id))
        except ET.ParseError:
            logger.error("[-] Failed to parse nmap XML output.")
        except Exception as e:
            logger.error(f"[-] Error parsing nmap XML: {e}")
            
        return open_ports

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    scanner = PortScanner([{"url": "http://scanme.nmap.org"}])
    res = scanner.scan()
    print(res)
