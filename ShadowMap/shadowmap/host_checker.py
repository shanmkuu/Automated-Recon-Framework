import asyncio
import httpx
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

class HostChecker:
    def __init__(self, subdomains: List[str], max_concurrency: int = 50):
        self.subdomains = subdomains
        self.max_concurrency = max_concurrency
        self.alive_hosts = []

    async def _check_target(self, client: httpx.AsyncClient, semaphore: asyncio.Semaphore, target_url: str):
        async with semaphore:
            try:
                # Disable redirects to capture exactly what is at the root
                response = await client.get(target_url, timeout=5.0, follow_redirects=False)
                return {
                    "url": target_url,
                    "status_code": response.status_code,
                    "server": response.headers.get("Server", "Unknown"),
                    "title": self._extract_title(response.text)
                }
            except httpx.RequestError:
                return None

    def _extract_title(self, html_content: str) -> str:
        if not html_content:
            return ""
        try:
            # Very basic extraction without BeautifulSoup
            lower_html = html_content.lower()
            start = lower_html.find("<title>")
            end = lower_html.find("</title>")
            if start != -1 and end != -1:
                return html_content[start + 7:end].strip()
        except Exception:
            pass
        return ""

    async def _run_checks(self):
        logger.info(f"[*] Starting alive host checks on {len(self.subdomains)} subdomains...")
        semaphore = asyncio.Semaphore(self.max_concurrency)
        
        async with httpx.AsyncClient(verify=False) as client:
            tasks = []
            for subdomain in self.subdomains:
                # Check both HTTP and HTTPS
                tasks.append(self._check_target(client, semaphore, f"http://{subdomain}"))
                tasks.append(self._check_target(client, semaphore, f"https://{subdomain}"))
            
            results = await asyncio.gather(*tasks)
            
            for res in results:
                if res:
                    self.alive_hosts.append(res)

    def check(self):
        # httpx triggers DeprecationWarning with loop, standard asyncio flow is preferred
        asyncio.run(self._run_checks())
        logger.info(f"[+] Found {len(self.alive_hosts)} alive endpoints.")
        return self.alive_hosts

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import sys
    if len(sys.argv) > 1:
        domains = sys.argv[1:]
        checker = HostChecker(domains)
        alive = checker.check()
        for a in alive:
            print(a)
