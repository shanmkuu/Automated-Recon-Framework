import requests
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

class Enumerator:
    def __init__(self, domain):
        self.domain = domain

    def _enum_crtsh(self):
        logger.info(f"[*] Starting crt.sh enumeration for {self.domain}")
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%.{self.domain}&output=json"
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name_value = entry.get('name_value', '')
                    # names can be separated by newlines
                    for name in name_value.split('\n'):
                        name = name.strip()
                        if name and not name.startswith('*'):
                            subdomains.add(name)
            else:
                logger.error(f"[-] crt.sh returned status code {response.status_code}")
        except Exception as e:
            logger.error(f"[-] Error enumerating crt.sh: {e}")
        
        logger.info(f"[+] crt.sh found {len(subdomains)} subdomains.")
        return subdomains

    def _enum_sublist3r(self):
        logger.info(f"[*] Starting Sublist3r enumeration for {self.domain}")
        subdomains = set()
        out_file = "sublist3r_out.txt"
        try:
            # We assume sublist3r is available in the system PATH
            process = subprocess.run(
                ['sublist3r', '-d', self.domain, '-n', '-o', out_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                with open(out_file, 'r') as f:
                    for line in f:
                        name = line.strip()
                        if name:
                            subdomains.add(name)
                # Cleanup
                import os
                os.remove(out_file)
            except FileNotFoundError:
                logger.warning("[-] Sublist3r output file not generated. Sublist3r might not be installed or failed.")
                
        except Exception as e:
            logger.error(f"[-] Error running sublist3r: {e}")
            
        logger.info(f"[+] Sublist3r found {len(subdomains)} subdomains.")
        return subdomains

    def enumerate(self):
        print(f"[*] Enumerating subdomains for {self.domain}...")
        results_crtsh = self._enum_crtsh()
        results_sublist3r = self._enum_sublist3r()
        
        all_subdomains = results_crtsh.union(results_sublist3r)
        
        # Ensure domain itself is included if valid
        all_subdomains.add(self.domain)
        
        sorted_subdomains = sorted(list(all_subdomains))
        print(f"[+] Total unique subdomains found: {len(sorted_subdomains)}")
        return sorted_subdomains

if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) > 1:
        domain = sys.argv[1]
        enum = Enumerator(domain)
        domains = enum.enumerate()
        for d in domains:
            print(d)
