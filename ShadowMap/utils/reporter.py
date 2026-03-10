import json
import os
import datetime
from typing import List, Dict, Any

class Reporter:
    def __init__(self, domain: str, subdomains: List[str], alive_hosts: List[Dict], port_results: Dict[str, List[int]]):
        self.domain = domain
        self.subdomains = subdomains
        self.alive_hosts = alive_hosts
        self.port_results = port_results
        self.report_dir = os.path.join("reports", self.domain)
        
        # Ensure report directory exists
        os.makedirs(self.report_dir, exist_ok=True)

    def generate(self):
        self._generate_json()
        self._generate_markdown()
        print(f"[*] Reports generated in: {self.report_dir}/")
        
        # Create a tiny helper file for out-of-band visual reconnaissance
        self._generate_urls_list()

    def _generate_json(self):
        data = {
            "domain": self.domain,
            "scan_date": datetime.datetime.now().isoformat(),
            "total_subdomains": len(self.subdomains),
            "subdomains": self.subdomains,
            "alive_hosts_count": len(self.alive_hosts),
            "alive_hosts": self.alive_hosts,
            "port_scan_results": self.port_results
        }
        json_path = os.path.join(self.report_dir, "scan_results.json")
        with open(json_path, 'w') as f:
            json.dump(data, f, indent=4)

    def _generate_markdown(self):
        md_path = os.path.join(self.report_dir, "summary.md")
        with open(md_path, 'w') as f:
            f.write(f"# ShadowMap Recon Report: `{self.domain}`\n\n")
            f.write(f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Overview\n\n")
            f.write(f"- **Total Subdomains Discovered:** {len(self.subdomains)}\n")
            f.write(f"- **Total Alive Hosts:** {len(self.alive_hosts)}\n\n")
            
            f.write("## Alive Hosts\n\n")
            if not self.alive_hosts:
                f.write("No alive hosts discovered.\n\n")
            else:
                f.write("| URL | Status Code | Server | Page Title | Open Ports |\n")
                f.write("| --- | :---: | --- | --- | --- |\n")
                
                for host in self.alive_hosts:
                    url = host.get('url', '')
                    status = host.get('status_code', 'N/A')
                    server = host.get('server', 'Unknown')
                    title = host.get('title', '')
                    
                    # Extract hostname for ports mapping
                    import urllib.parse
                    hostname = urllib.parse.urlparse(url).hostname or ""
                    
                    ports = self.port_results.get(hostname, [])
                    ports_str = ", ".join(map(str, ports)) if ports else "None"
                    
                    # Clean title escaping
                    title = title.replace('|', '').replace('\n', ' ')
                    
                    f.write(f"| {url} | `{status}` | {server} | {title} | `{ports_str}` |\n")
            
            f.write("\n## All Subdomains\n\n")
            if not self.subdomains:
                f.write("No subdomains discovered.\n\n")
            else:
                f.write("```text\n")
                for sub in self.subdomains:
                    f.write(f"{sub}\n")
                f.write("```\n")

    def _generate_urls_list(self):
        # Generates a simple text file of all alive URLs to be easily consumed
        urls_path = os.path.join(self.report_dir, "alive_urls.txt")
        with open(urls_path, 'w') as f:
            for host in self.alive_hosts:
                f.write(f"{host.get('url')}\n")
