from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("assets")
OUT.mkdir(exist_ok=True)

ADMIN_CSS = """
:root{--bg:#0f172a;--card:#1e293b;--text:#f8fafc;--muted:#94a3b8;--accent:#38bdf8;--ok:#10b981;--bad:#ef4444;--border:#334155}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font-family:Arial,sans-serif}.header{height:76px;background:var(--card);padding:0 40px;border-bottom:1px solid var(--border);display:flex;justify-content:space-between;align-items:center}.header h1{margin:0;color:var(--accent);font-size:25px}.container{max-width:1220px;margin:38px auto;padding:0 22px}.toolbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}button{background:var(--accent);color:white;border:0;padding:11px 19px;border-radius:8px;font-weight:700}table{width:100%;border-collapse:collapse;background:var(--card);border-radius:12px;overflow:hidden}th,td{padding:15px 18px;text-align:right;border-bottom:1px solid var(--border)}th{background:#111827;color:var(--muted);font-size:13px}.badge{padding:5px 10px;border-radius:20px;font-size:12px;font-weight:700}.active{background:rgba(16,185,129,.18);color:var(--ok)}.inactive{background:rgba(239,68,68,.18);color:var(--bad)}.api{background:#0b1220;padding:8px;border-radius:6px;font-family:monospace;color:var(--accent);border:1px solid var(--border);font-size:12px}.muted{font-size:12px;color:var(--muted)}.note{margin-top:16px;color:var(--muted);font-size:12px}.flow{margin-top:260px;background:var(--card);border:1px solid var(--border);padding:24px;border-radius:14px;display:flex;justify-content:space-around;direction:ltr}.flow div{text-align:center;color:var(--accent);font-weight:700}.flow small{display:block;color:var(--muted);font-weight:400;margin-top:5px}
"""

def admin_html(state="table"):
    table = """<table><thead><tr><th>المعرف</th><th>اسم المتجر</th><th>الحالة</th><th>مفتاح API</th><th>النوع والشخصية</th><th>رابط ووكومرس</th><th>إجراءات</th></tr></thead><tbody>
    <tr><td>#1</td><td><b>Demo Perfume Store</b></td><td><span class='badge active'>نشط</span></td><td><div class='api'>demo_a1b2...7f9c</div></td><td class='muted'>perfume<br><b style='color:#38bdf8'>dotdot_robot</b></td><td class='muted' dir='ltr'>https://demo-store.example</td><td>إيقاف</td></tr>
    <tr><td>#2</td><td><b>Electronics Demo</b></td><td><span class='badge active'>نشط</span></td><td><div class='api'>demo_c3d4...2ab1</div></td><td class='muted'>electronics<br><b style='color:#38bdf8'>tulip_fairy</b></td><td class='muted' dir='ltr'>https://electronics.example</td><td>إيقاف</td></tr>
    <tr><td>#3</td><td><b>Sandbox Client</b></td><td><span class='badge inactive'>موقوف</span></td><td><div class='api'>demo_e5f6...9d30</div></td><td class='muted'>general<br><b style='color:#38bdf8'>dotdot_robot</b></td><td class='muted' dir='ltr'>https://sandbox.example</td><td>تفعيل</td></tr></tbody></table>"""
    modal = """<div style='position:fixed;inset:0;background:rgba(0,0,0,.72);display:flex;align-items:center;justify-content:center'><div style='width:520px;background:#1e293b;border:1px solid #334155;border-radius:18px;padding:30px'><h2>إضافة متجر جديد</h2><div style='display:grid;gap:12px'><label>اسم المتجر<input value='Demo Fashion Store'></label><label>نوع المتجر<select><option>clothing</option></select></label><label>شخصية الذكاء الاصطناعي<select><option>dotdot_robot</option></select></label><label>WooCommerce URL<input value='https://fashion-demo.example'></label></div><div style='display:flex;gap:10px;margin-top:20px'><button style='flex:1'>حفظ وتوليد المفتاح</button><button style='flex:1;background:transparent;border:1px solid #475569'>إلغاء</button></div><p class='muted'>Demo values only — no production credentials.</p></div></div><style>label{color:#cbd5e1}input,select{display:block;width:100%;margin-top:6px;padding:12px;border-radius:8px;border:1px solid #334155;background:#0f172a;color:white}</style>"""
    flow = """<div class='flow'><div>Client Store<small>External storefront</small></div><div>→</div><div>Embedded Widget<small>Persona-aware assistant</small></div><div>→</div><div>Nexus API<small>Scoped access</small></div><div>→</div><div>Tenant Store<small>Store-specific config</small></div></div>"""
    extra = modal if state == "modal" else flow if state == "architecture" else ""
    return f"<!doctype html><html lang='ar' dir='rtl'><meta charset='utf-8'><style>{ADMIN_CSS}</style><body><div class='header'><h1>NexusAI Admin</h1><div>مرحباً، كرم</div></div><div class='container'><div class='toolbar'><h2>إدارة المتاجر (Clients)</h2><button>+ إضافة متجر جديد</button></div>{table}<div class='note'>Portfolio demo data only — no production API keys or client credentials are shown.</div>{extra}</div></body></html>"

ROBOT_CSS = """
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 50% 50%,#1e3c72,#2a5298,#0a192f);height:100vh;display:flex;overflow:hidden;font-family:Arial,sans-serif}.store{flex:1;padding:55px;display:grid;grid-template-columns:repeat(2,1fr);gap:30px;align-content:center}.card{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);padding:24px;border-radius:15px;color:#fff;text-align:center}.icon{font-size:42px}.title{font-size:20px;font-weight:700;margin:12px 0}.price{color:#00e5ff;font-weight:700}.robot-wrap{width:410px;display:flex;justify-content:center;align-items:center;position:relative}.robot{position:relative;width:320px;height:480px}.msg{position:absolute;top:-15px;left:50%;transform:translateX(-50%);background:white;color:#ff3366;padding:15px 24px;border-radius:20px;font-weight:700;font-size:17px;text-align:center;min-width:245px;border:2px solid #ff3366;z-index:3}.instructions{position:absolute;top:22px;left:22px;color:#fff;font-size:18px;opacity:.9}
"""

def robot_html(focus="phone"):
    messages={"phone":"📱 هل تبحث عن أفضل كاميرا؟ هذا الهاتف هو طلبك!","perfume":"🧴 لو بدك عطراً يومياً قوياً، جرّب هذا الخيار.","watch":"⌚ للهدية الفاخرة، الساعة هي الاختيار الأوضح."}
    cards="""<div class='card'><div class='icon'>🧴</div><div class='title'>عطر ديور سوفاج</div><div class='price'>120 دولار</div></div><div class='card'><div class='icon'>⌚</div><div class='title'>ساعة رولكس كلاسيكية</div><div class='price'>5000 دولار</div></div><div class='card'><div class='icon'>📱</div><div class='title'>آيفون 15 برو ماكس</div><div class='price'>1199 دولار</div></div><div class='card'><div class='icon'>🕶️</div><div class='title'>نظارة شمسية ريبان</div><div class='price'>150 دولار</div></div>"""
    robot="""<svg viewBox='0 0 300 480' width='100%' height='100%'><defs><radialGradient id='body' cx='40%' cy='30%' r='70%'><stop offset='0%' stop-color='#fff'/><stop offset='60%' stop-color='#d1f2eb'/><stop offset='100%' stop-color='#76d7c4'/></radialGradient></defs><ellipse cx='150' cy='190' rx='65' ry='70' fill='url(#body)'/><rect x='65' y='30' width='170' height='110' rx='55' fill='url(#body)'/><rect x='80' y='50' width='140' height='70' rx='35' fill='#172033'/><circle cx='115' cy='80' r='14' fill='#fff'/><circle cx='115' cy='80' r='7' fill='#0a192f'/><circle cx='185' cy='80' r='14' fill='#fff'/><circle cx='185' cy='80' r='7' fill='#0a192f'/><path d='M140 100 Q150 108 160 100' fill='none' stroke='#1abc9c' stroke-width='4'/><rect x='90' y='120' width='120' height='150' rx='30' fill='#455a64'/><rect x='58' y='180' width='24' height='60' rx='12' fill='url(#body)'/><rect x='218' y='180' width='24' height='60' rx='12' fill='url(#body)'/><ellipse cx='110' cy='300' rx='15' ry='40' fill='#00e5ff'/><ellipse cx='190' cy='300' rx='15' ry='40' fill='#00e5ff'/><text x='150' y='205' text-anchor='middle' font-size='22' font-weight='700' fill='#dff'>NEXUS AI</text></svg>"""
    return f"<!doctype html><html lang='ar' dir='rtl'><meta charset='utf-8'><style>{ROBOT_CSS}</style><body><div class='instructions'>راقب ذكاء الروبوت في التسويق! 💰</div><div class='store'>{cards}</div><div class='robot-wrap'><div class='robot'><div class='msg'>{messages[focus]}</div>{robot}</div></div></body></html>"

CLIENT_CSS = """
*{box-sizing:border-box}body{font-family:Arial,sans-serif;background:#f4f4f9;padding:28px;color:#111;margin:0}.product-card{background:white;padding:22px;margin:10px;border-radius:10px;box-shadow:0 5px 15px rgba(0,0,0,.1);display:inline-block;width:270px;vertical-align:top}.bar{background:white;padding:18px;border-radius:10px;box-shadow:0 5px 15px rgba(0,0,0,.08);margin:22px 0}input{padding:11px;width:310px;border-radius:5px;border:1px solid #ccc}button{padding:11px 16px;background:#00d8ef;border:none;border-radius:5px;font-weight:700}.widget{position:fixed;left:30px;bottom:30px;width:330px;background:#0f172a;color:#fff;border-radius:18px;box-shadow:0 15px 35px rgba(0,0,0,.25);padding:19px}.widget h3{color:#38bdf8;margin-top:0}.msg{background:#1e293b;padding:13px;border-radius:12px;margin-top:10px;line-height:1.55}
"""

def client_html(state="recommend"):
    messages={"welcome":"مرحباً! اسألني عن أي منتج وسأقارن الخيارات لك.","recommend":"إذا بدك جهاز للألعاب والتصميم، اللابتوب هو الخيار الأقوى 👾","compare":"<b>مقارنة سريعة:</b><br>اللابتوب للأداء والعمل الثقيل، أما شاشة 4K فهي أفضل لتجربة العرض والمحتوى."}
    return f"<!doctype html><html lang='ar' dir='rtl'><meta charset='utf-8'><style>{CLIENT_CSS}</style><body><h1>مرحباً بك في متجرنا التجريبي للإلكترونيات</h1><p>موقع تجريبي يوضح حقن مساعد Nexus AI في متجر عميل خارجي.</p><div class='bar'><input value='demo_key_for_showcase' readonly><button>تفعيل الذكاء الاصطناعي</button></div><div class='product-card'><h2>لابتوب ألعاب</h2><p>أقوى لابتوب للمصممين واللاعبين.</p></div><div class='product-card'><h2>شاشة ذكية 4K</h2><p>شاشة بحجم 65 بوصة وألوان مذهلة.</p></div><div class='widget'><h3>Nexus AI</h3><div>مساعد المتجر الذكي</div><div class='msg'>{messages[state]}</div></div></body></html>"

PREVIEWS = {
    "nexus-admin-overview.png": admin_html("table"),
    "nexus-admin-add-store.png": admin_html("modal"),
    "nexus-admin-architecture.png": admin_html("architecture"),
    "nexus-robot-phone.png": robot_html("phone"),
    "nexus-robot-perfume.png": robot_html("perfume"),
    "nexus-robot-watch.png": robot_html("watch"),
    "nexus-client-welcome.png": client_html("welcome"),
    "nexus-client-recommendation.png": client_html("recommend"),
    "nexus-client-comparison.png": client_html("compare"),
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    for name, html in PREVIEWS.items():
        page.set_content(html, wait_until="load")
        page.screenshot(path=str(OUT / name), full_page=False)
    browser.close()

print(f"Generated {len(PREVIEWS)} sanitized Nexus AI showcase previews.")
