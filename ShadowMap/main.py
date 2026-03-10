import argparse
import sys
import logging
import time
from shadowmap.enumerator import Enumerator
from shadowmap.host_checker import HostChecker
from shadowmap.port_scanner import PortScanner
from utils.reporter import Reporter

# Setup basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("ShadowMap")

BANNER = r"""
  ___ _               _               __  __           
 / __| |_  __ _ __| |_____ __ _|  \/  |__ _ _ __  
 \__ \ ' \/ _` / _` / _ \ V  V / |\/| / _` | '_ \ 
 |___/_||_\__,_\__,_\___/\_/\_/|_|  |_\__,_| .__/ 
                                           |_|    
    Modular Reconnaissance Framework (v1.0)
"""

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="ShadowMap - Automated Reconnaissance Framework")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--concurrency", type=int, default=50, help="Max concurrency for HTTP requests (default: 50)")
    
    args = parser.parse_args()
    domain = args.domain

    logger.info(f"Starting reconnaissance on target: {domain}")
    start_time = time.time()

    # Step 1: Subdomain Enumeration
    logger.info("--- [ Phase 1: Subdomain Enumeration ] ---")
    enumerator = Enumerator(domain)
    subdomains = enumerator.enumerate()
    if not subdomains:
        logger.error("No subdomains found. Exiting.")
        sys.exit(1)
        
    logger.info(f"Discovered {len(subdomains)} subdomains:")
    for sub in subdomains:
        logger.info(f"  -> {sub}")

    # Step 2: Alive Host Checking
    logger.info("--- [ Phase 2: Alive Host Checking ] ---")
    checker = HostChecker(subdomains, max_concurrency=args.concurrency)
    alive_hosts = checker.check()
    if not alive_hosts:
        logger.error("No alive hosts found. Exiting.")
        sys.exit(1)

    # Step 3: Port Scanning
    logger.info("--- [ Phase 3: Port Scanning ] ---")
    scanner = PortScanner(alive_hosts)
    port_results = scanner.scan()

    # Step 4: Reporting
    logger.info("--- [ Phase 4: Reporting ] ---")
    reporter = Reporter(domain, subdomains, alive_hosts, port_results)
    reporter.generate()

    elapsed = time.time() - start_time
    logger.info(f"Reconnaissance completed in {elapsed:.2f} seconds.")
    logger.info(f"Target: {domain} | Subdomains: {len(subdomains)} | Alive Hosts: {len(alive_hosts)}")

if __name__ == "__main__":
    main()
