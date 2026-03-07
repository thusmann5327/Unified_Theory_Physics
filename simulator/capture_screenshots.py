#!/usr/bin/env python3
"""
Screenshot capture script for Universe Simulator debugging.
Captures views at different zoom levels to identify visualization issues.
"""

import asyncio
from playwright.async_api import async_playwright
import os
from datetime import datetime

SCREENSHOT_DIR = "/var/www/universe.eldon.food/debug_screenshots"
BASE_URL = "http://localhost:5200"

async def capture_screenshots():
    """Capture screenshots at all zoom levels."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
        page.set_default_timeout(60000)  # 60 second timeout

        print(f"Loading simulator at {BASE_URL}...")
        await page.goto(BASE_URL, wait_until='load')
        await page.wait_for_timeout(5000)  # Wait for Three.js to initialize

        screenshots = []

        # 1. Initial view
        print("Capturing: Initial view")
        path = f"{SCREENSHOT_DIR}/{timestamp}_01_initial.png"
        await page.screenshot(path=path, full_page=False)
        screenshots.append(("Initial", path))

        # 2. Execute JavaScript to switch zoom levels directly
        zoom_levels = [
            ("Universe", 0),
            ("Galaxy", 1),
            ("Solar", 2),
            ("Planetary", 3),
            ("Geological", 4),
            ("Earth", 5),
        ]

        for name, level in zoom_levels:
            print(f"Capturing: {name} (level {level})")
            try:
                await page.evaluate(f"setZoomLevel({level})")
                await page.wait_for_timeout(2000)
                path = f"{SCREENSHOT_DIR}/{timestamp}_{level+2:02d}_{name.lower()}.png"
                await page.screenshot(path=path)
                screenshots.append((name, path))
            except Exception as e:
                print(f"  Error: {e}")

        # 3. Galaxy with helix visible
        print("Capturing: Galaxy + Helix")
        try:
            await page.evaluate("setZoomLevel(1)")  # Galaxy
            await page.wait_for_timeout(1000)
            await page.evaluate("if (!showHelix) toggleHelix()")
            await page.wait_for_timeout(1000)
            path = f"{SCREENSHOT_DIR}/{timestamp}_08_galaxy_helix.png"
            await page.screenshot(path=path)
            screenshots.append(("Galaxy+Helix", path))
        except Exception as e:
            print(f"  Error: {e}")

        # 4. Universe with all elements
        print("Capturing: Universe + All Elements")
        try:
            await page.evaluate("setZoomLevel(0)")  # Universe
            await page.wait_for_timeout(1000)
            await page.evaluate("""
                if (!showBrackets) toggleBrackets();
                if (!showHelix) toggleHelix();
                if (!showWall) toggleWall();
                if (!showHinges) toggleHinges();
            """)
            await page.wait_for_timeout(1000)
            path = f"{SCREENSHOT_DIR}/{timestamp}_09_universe_all.png"
            await page.screenshot(path=path)
            screenshots.append(("Universe+All", path))
        except Exception as e:
            print(f"  Error: {e}")

        await browser.close()

        print(f"\n{'='*60}")
        print(f"Captured {len(screenshots)} screenshots to {SCREENSHOT_DIR}")
        print(f"{'='*60}")
        for name, path in screenshots:
            print(f"  {name}: {os.path.basename(path)}")

        return screenshots

if __name__ == "__main__":
    asyncio.run(capture_screenshots())
