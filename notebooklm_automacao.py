import asyncio
import subprocess
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
LINKS_FILE = BASE_DIR / "notebooklm_links.txt"
BRAVE_PATHS = [
    "/usr/bin/brave-browser",
    "/usr/bin/brave",
    "/opt/brave.com/brave/brave-browser",
]
BRAVE_PROFILE = Path.home() / ".config/BraveSoftware/Brave-Browser"
CDP_URL = "http://127.0.0.1:9222"
NOTEBOOKLM_URL = "https://notebooklm.google.com/"

def brave_path():
    for p in BRAVE_PATHS:
        if Path(p).exists():
            return p
    return None

def links():
    if not LINKS_FILE.exists():
        return []
    return [x.strip() for x in LINKS_FILE.read_text(encoding="utf-8").splitlines() if x.strip()]

def start_brave(path):
    subprocess.Popen([
        path, "--remote-debugging-port=9222",
        "--remote-allow-origins=http://127.0.0.1",
        f"--user-data-dir={BRAVE_PROFILE}",
        "--no-first-run", "--no-default-browser-check", "--start-maximized"
    ])

async def cdp_ready():
    import requests
    try:
        return requests.get(f"{CDP_URL}/json/version", timeout=2).ok
    except requests.RequestException:
        return False

async def click_text(page, names):
    for name in names:
        for locator in [
            page.get_by_role("button", name=name),
            page.get_by_text(name, exact=True)
        ]:
            try:
                if await locator.count() and await locator.first.is_visible():
                    await locator.first.click(timeout=2500)
                    return True
            except Exception:
                pass
    return False

async def main():
    urls = links()
    if not urls:
        print("Nenhum link em notebooklm_links.txt")
        return

    brave = brave_path()
    if not brave:
        print("Brave não encontrado.")
        return

    if not await cdp_ready():
        start_brave(brave)
        for _ in range(20):
            if await cdp_ready():
                break
            await asyncio.sleep(0.5)

    if not await cdp_ready():
        print("Não foi possível conectar ao Brave na porta 9222.")
        print("Feche todas as janelas do Brave e tente novamente.")
        return

    async with async_playwright() as pw:
        browser = await pw.chromium.connect_over_cdp(CDP_URL)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else await context.new_page()

        await page.goto(NOTEBOOKLM_URL, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(5000)

        await click_text(page, ["Add source", "Add sources", "Adicionar fonte", "Adicionar fontes"])
        await page.wait_for_timeout(1000)
        await click_text(page, ["YouTube", "YouTube URL", "YouTube link"])
        await page.wait_for_timeout(1000)

        selectors = [
            "textarea",
            'input[type="url"]',
            'input[placeholder*="YouTube" i]',
            'textarea[placeholder*="YouTube" i]',
            "input"
        ]

        box = None
        for selector in selectors:
            loc = page.locator(selector)
            try:
                for i in range(await loc.count()):
                    candidate = loc.nth(i)
                    if await candidate.is_visible():
                        box = candidate
                        break
            except Exception:
                pass
            if box:
                break

        if not box:
            print("Campo de URL do NotebookLM não encontrado. A interface pode ter mudado.")
            return

        for url in urls:
            await box.fill(url)
            await box.press("Enter")
            await page.wait_for_timeout(2000)

        print(f"{len(urls)} links processados. Brave continuará aberto.")

if __name__ == "__main__":
    asyncio.run(main())
