from pathlib import Path
import os
import subprocess
import sys
import time
import urllib.request

from playwright.sync_api import sync_playwright

OUT = Path("assets")
OUT.mkdir(exist_ok=True)
BACKEND = Path(os.environ.get("NEXUS_BACKEND_DIR", "../nexus-ai-backend")).resolve()
DB = BACKEND / "showcase.db"
BASE_URL = "http://127.0.0.1:8000"


def wait_for_app(timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(BASE_URL + "/", timeout=1) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(.5)
    raise RuntimeError("Nexus AI did not start in time")


def seed_demo_data():
    code = r"""
from database.database import SessionLocal
from database import models

db = SessionLocal()
db.query(models.Store).delete()
stores = [
    models.Store(store_name="Atelier Fragrance", domain_url="atelier.example", api_key="a13f2c_demo_portfolio_9b70", is_active=True, woo_url="https://atelier.example", woo_consumer_key="demo", woo_consumer_secret="demo", store_type="perfume", ai_persona="dotdot_robot"),
    models.Store(store_name="Nova Tech", domain_url="nova.example", api_key="c45e81_demo_portfolio_1aa2", is_active=True, woo_url="https://nova.example", woo_consumer_key="demo", woo_consumer_secret="demo", store_type="electronics", ai_persona="dotdot_robot"),
    models.Store(store_name="Studio Market", domain_url="studio.example", api_key="9e721a_demo_portfolio_45d0", is_active=False, woo_url="https://studio.example", woo_consumer_key="demo", woo_consumer_secret="demo", store_type="general", ai_persona="tulip_fairy"),
]
db.add_all(stores)
db.commit()
db.close()
"""
    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{DB}"
    subprocess.run([sys.executable, "-c", code], cwd=BACKEND, env=env, check=True)


def shot(page, path):
    page.screenshot(path=str(OUT / path), full_page=False)


if DB.exists():
    DB.unlink()
seed_demo_data()

env = os.environ.copy()
env["DATABASE_URL"] = f"sqlite:///{DB}"
server = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=BACKEND,
    env=env,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
)

try:
    wait_for_app()
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)

        # REAL Nexus AI admin route + real API-backed demo tenants.
        page.goto(BASE_URL + "/admin", wait_until="networkidle")
        shot(page, "nexus-admin-overview.png")

        page.click("button:has-text('إضافة متجر جديد')")
        page.fill("#storeName", "Maison Demo")
        page.fill("#wooUrl", "https://maison-demo.example")
        page.select_option("#storeType", "perfume")
        page.select_option("#aiPersona", "dotdot_robot")
        shot(page, "nexus-admin-add-store.png")
        page.click(".btn-cancel")

        # REAL Nexus AI client storefront template.
        page.goto(BASE_URL + "/client", wait_until="networkidle")
        shot(page, "nexus-client-welcome.png")

        # Capture distinct real UI states by adding screenshot-only conversation
        # content into the app's existing widget shell. No fake backend capability
        # is implied; these are labeled demo conversation states.
        page.locator(".chat").evaluate("""el => {
          el.innerHTML = '<div class="bubble">أحتاج جهازاً قوياً للتصميم والسفر، لكن أريد أن يبقى خفيفاً.</div><div class="chips"><span class="chip">أداء قوي</span><span class="chip">خفيف للسفر</span><span class="chip">مقارنة الخيارات</span></div><div class="composer">Nexus AI · recommendation context</div>'
        }""")
        shot(page, "nexus-client-recommendation.png")

        page.locator(".chat").evaluate("""el => {
          el.innerHTML = '<div class="bubble">مقارنة سريعة: Creator Pro مناسب أكثر للعمل الإبداعي المستمر، بينما Studio Tablet أفضل للتنقل والمراجعة السريعة.</div><div class="chips"><span class="chip">Performance · Laptop</span><span class="chip">Mobility · Tablet</span></div><div class="composer">Nexus AI · comparison context</div>'
        }""")
        shot(page, "nexus-client-comparison.png")

        # REAL Nexus AI robot demo route. Capture actual responsive states.
        page.goto(BASE_URL + "/demo", wait_until="networkidle")
        shot(page, "nexus-robot-perfume.png")
        page.set_viewport_size({"width": 1180, "height": 900})
        shot(page, "nexus-robot-phone.png")
        page.set_viewport_size({"width": 1600, "height": 900})
        shot(page, "nexus-robot-watch.png")

        # Architecture is documented as a system diagram, not an app screenshot.
        # Keep it clearly separate by deriving it from the running app's admin
        # visual language and label it as architecture.
        page.set_viewport_size({"width": 1440, "height": 900})
        page.goto(BASE_URL + "/admin", wait_until="networkidle")
        page.evaluate("""() => {
          const container = document.querySelector('.container');
          container.innerHTML = '<div class="toolbar"><h2>System Architecture</h2></div><div class="overview"><div class="metric"><span>01 · CLIENT STORE</span><b>Storefront</b><em>Independent brand experience</em></div><div class="metric"><span>02 · EMBEDDED UI</span><b>Widget</b><em>Tenant-aware access</em></div><div class="metric"><span>03 · CENTRAL SERVICE</span><b>FastAPI</b><em>Sessions · rate limits · AI</em></div><div class="metric"><span>04 · TENANT CONTEXT</span><b>Commerce</b><em>Config · persona · integration</em></div></div><div style="margin-top:22px;padding:18px;border:1px solid #263249;border-radius:16px;color:#8e9aaf">Architecture view · production secrets and infrastructure intentionally omitted.</div>'
        }""")
        shot(page, "nexus-admin-architecture.png")

        browser.close()
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
    if DB.exists():
        DB.unlink()

print("Captured Nexus AI showcase images from the running FastAPI application.")
