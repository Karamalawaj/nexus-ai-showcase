from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path("assets")
OUT.mkdir(exist_ok=True)

BASE = """
*{box-sizing:border-box}body{margin:0;font-family:Inter,'Segoe UI',Arial,sans-serif;background:#070a12;color:#f6f8fc}
:root{--bg:#070a12;--panel:#101624;--panel2:#151c2c;--line:#222d42;--muted:#8e9aaf;--violet:#765cf6;--cyan:#35ccec;--green:#43d99b}
.brand{font-weight:900;letter-spacing:-.7px}.brand i{font-style:normal;color:#8b7cf6}.pill{border:1px solid #2b3750;border-radius:999px;padding:6px 10px;font-size:10px;color:#aeb8ca}
"""

def shell(body, extra=""):
    return f"<!doctype html><html lang='en'><meta charset='utf-8'><style>{BASE}{extra}</style><body>{body}</body></html>"

def admin(state="overview"):
    css="""
    .top{height:76px;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;padding:0 54px;background:rgba(8,11,19,.9)}
    .wrap{max-width:1260px;margin:auto;padding:36px 28px}.heading{display:flex;justify-content:space-between;align-items:end;margin-bottom:22px}.heading h1{font-size:30px;margin:0}.heading p{margin:7px 0 0;color:var(--muted);font-size:11px}
    button{background:linear-gradient(135deg,var(--violet),#5b43d8);border:0;color:#fff;padding:12px 16px;border-radius:11px;font-weight:800}.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:17px}
    .metric{background:linear-gradient(145deg,#121927,#0c111d);border:1px solid var(--line);padding:17px;border-radius:16px}.metric small{color:var(--muted);font-size:9px}.metric b{display:block;font-size:24px;margin:7px 0}.metric em{font-style:normal;color:var(--green);font-size:9px}
    table{width:100%;border-collapse:separate;border-spacing:0;border:1px solid var(--line);border-radius:17px;overflow:hidden;background:#0d131f}th,td{padding:15px 16px;border-bottom:1px solid #202a3e;text-align:left;font-size:11px}th{font-size:9px;color:var(--muted);background:#0a0f19}tr:last-child td{border-bottom:0}.status{color:var(--green);background:rgba(67,217,155,.08);padding:5px 8px;border-radius:20px}.key{font-family:monospace;color:#aab5c8}.persona{color:#a996ff}
    .modalbg{position:fixed;inset:0;background:rgba(2,4,10,.78);backdrop-filter:blur(10px);display:grid;place-items:center}.modal{width:570px;background:#101624;border:1px solid #2b3750;border-radius:22px;padding:28px;box-shadow:0 40px 100px #0009}.modal h2{margin:0 0 5px}.modal>p{color:var(--muted);font-size:11px;margin-bottom:22px}.form{display:grid;grid-template-columns:1fr 1fr;gap:12px}.field{background:#0a0f19;border:1px solid #253149;border-radius:11px;padding:12px}.field small{display:block;color:#78859a;font-size:9px;margin-bottom:7px}.field b{font-size:11px}.wide{grid-column:1/-1}.actions{display:flex;gap:9px;margin-top:18px}.ghost{background:#171e2d;border:1px solid #2a364d}
    .arch{display:grid;grid-template-columns:1fr 58px 1fr 58px 1fr 58px 1fr;align-items:center;margin-top:28px}.node{height:150px;border:1px solid #263249;border-radius:18px;background:linear-gradient(145deg,#121927,#0c111d);padding:20px}.node b{display:block;margin:9px 0}.node small{color:var(--muted);line-height:1.5}.ico{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,var(--violet),var(--cyan));display:grid;place-items:center}.arrow{text-align:center;color:#58647a;font-size:24px}.safe{margin-top:20px;border:1px solid #203348;background:#0a151d;padding:14px;border-radius:13px;color:#77d9b0;font-size:10px}
    """
    rows="""<table><thead><tr><th>TENANT</th><th>STATUS</th><th>API ACCESS</th><th>STORE TYPE</th><th>AI PERSONA</th><th>COMMERCE ENDPOINT</th></tr></thead><tbody>
    <tr><td><b>Atelier Fragrance</b><br><small style='color:#68758b'>Tenant #01</small></td><td><span class='status'>● Active</span></td><td class='key'>a13f2c••••••9b70</td><td>Perfume</td><td class='persona'>Dot Robot</td><td>atelier.example</td></tr>
    <tr><td><b>Nova Tech</b><br><small style='color:#68758b'>Tenant #02</small></td><td><span class='status'>● Active</span></td><td class='key'>c45e81••••••1aa2</td><td>Electronics</td><td class='persona'>Tulip</td><td>nova.example</td></tr>
    <tr><td><b>Studio Market</b><br><small style='color:#68758b'>Tenant #03</small></td><td><span style='color:#f6b85b'>● Paused</span></td><td class='key'>9e721a••••••45d0</td><td>General</td><td class='persona'>Dot Robot</td><td>studio.example</td></tr></tbody></table>"""
    metrics="""<div class='metrics'><div class='metric'><small>CONNECTED STORES</small><b>3</b><em>Tenant network</em></div><div class='metric'><small>ACTIVE TENANTS</small><b>2</b><em>● Operational</em></div><div class='metric'><small>AI PERSONAS</small><b>2</b><em>Context aware</em></div><div class='metric'><small>CENTRAL API</small><b style='font-size:18px;color:var(--green)'>Online</b><em>Rate limited</em></div></div>"""
    top="<div class='top'><div class='brand'>NEXUS <i>AI</i></div><span class='pill'>PRIVATE SaaS CONTROL PLANE</span></div>"
    heading="<div class='heading'><div><h1>Commerce intelligence</h1><p>Manage isolated client stores, AI personas and scoped integrations.</p></div><button>+ Connect store</button></div>"
    extra=""
    if state=="modal":
        extra="""<div class='modalbg'><div class='modal'><span class='pill'>TENANT ONBOARDING</span><h2>Connect a new store</h2><p>Create an isolated commerce tenant and select its assistant persona.</p><div class='form'><div class='field'><small>STORE NAME</small><b>Maison Demo</b></div><div class='field'><small>STORE TYPE</small><b>Perfume & lifestyle</b></div><div class='field'><small>AI PERSONA</small><b>Dot Robot</b></div><div class='field'><small>STATUS</small><b style='color:var(--green)'>Ready to activate</b></div><div class='field wide'><small>WOOCOMMERCE ENDPOINT</small><b>https://maison-demo.example</b></div></div><div class='actions'><button>Create tenant & key</button><button class='ghost'>Cancel</button></div></div></div>"""
    elif state=="architecture":
        rows="""<div class='arch'><div class='node'><div class='ico'>01</div><b>Client Store</b><small>Independent storefront and brand experience.</small></div><div class='arrow'>→</div><div class='node'><div class='ico'>02</div><b>Embedded Widget</b><small>Store-aware assistant loaded through scoped access.</small></div><div class='arrow'>→</div><div class='node'><div class='ico'>03</div><b>Central API</b><small>Rate limits, session logic and AI orchestration.</small></div><div class='arrow'>→</div><div class='node'><div class='ico'>04</div><b>Tenant Context</b><small>Store configuration, persona and commerce layer.</small></div></div><div class='safe'>✓ Portfolio-safe architecture view · production secrets and infrastructure intentionally omitted</div>"""
        metrics=""
    return shell(top+f"<main class='wrap'>{heading}{metrics}{rows}</main>"+extra,css)

def storefront(mode="welcome"):
    css="""
    body{background:#f7f8fb;color:#0b1020}.nav{height:74px;background:#fff;border-bottom:1px solid #e7eaf0;padding:0 6vw;display:flex;align-items:center;justify-content:space-between}.nav .brand{font-size:20px}.nav span{font-size:10px;color:#778196;margin-left:20px}.hero{max-width:1180px;margin:auto;padding:48px 24px 20px;display:grid;grid-template-columns:1.05fr .95fr;gap:38px;align-items:center}.eyebrow{font-size:9px;color:#765cf6;font-weight:900;letter-spacing:1.4px}.hero h1{font-size:48px;line-height:1.08;letter-spacing:-2px;margin:10px 0 15px}.hero p{color:#717b8f;line-height:1.7;font-size:12px}.art{height:290px;border-radius:28px;background:radial-gradient(circle at 70% 25%,#35ccec55,transparent 27%),linear-gradient(145deg,#171e33,#090d18);position:relative;overflow:hidden}.art:after{content:'NEXUS';position:absolute;bottom:-15px;left:15px;font-size:95px;font-weight:900;color:#ffffff0b}.cube{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-9deg);width:145px;height:190px;border-radius:27px;background:linear-gradient(145deg,#765cf6,#35ccec);box-shadow:0 30px 60px #0008}.cube:after{content:'AI';position:absolute;inset:15px;border:1px solid #ffffff44;border-radius:20px;display:grid;place-items:center;color:#fff;font-size:50px;font-weight:900}.products{max-width:1180px;margin:auto;padding:18px 24px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{background:#fff;border:1px solid #e6e9ef;border-radius:18px;padding:12px}.pic{height:105px;border-radius:13px;background:linear-gradient(145deg,#edf0f5,#dce1ea);display:grid;place-items:center;font-size:34px}.card b{display:block;font-size:11px;margin:10px 0 4px}.card small{color:#7c8698}.widget{position:fixed;left:28px;bottom:28px;width:365px;background:#0d1220;color:#fff;border:1px solid #27304a;border-radius:22px;box-shadow:0 30px 80px #05081766;overflow:hidden}.wh{padding:14px 16px;border-bottom:1px solid #222c42;display:flex;justify-content:space-between}.wh b{font-size:11px}.online{color:#43d99b;font-size:9px}.chat{padding:14px}.bot{background:#171f31;border:1px solid #263149;padding:11px;border-radius:13px;font-size:10px;line-height:1.55}.user{margin:8px 0 8px 50px;background:linear-gradient(135deg,#765cf6,#654bdc);padding:10px;border-radius:13px;font-size:10px}.result{border:1px solid #2a3650;border-radius:12px;padding:10px;margin-top:8px}.result strong{font-size:10px}.result small{display:block;color:#9aa5b8;margin-top:4px}.chips{display:flex;gap:5px;margin-top:9px}.chips i{font-style:normal;border:1px solid #303c58;border-radius:20px;padding:6px 8px;font-size:8px;color:#b7c1d2}
    """
    msgs={
      "welcome":"<div class='bot'>Hi 👋 Tell me what matters most and I’ll narrow the catalog for you.</div><div class='chips'><i>Work & design</i><i>Best value</i><i>Compare</i></div>",
      "recommend":"<div class='user'>I need something powerful for design and travel.</div><div class='bot'>Creator Pro is the strongest fit: portable, high-performance and better suited to your workload.</div><div class='result'><strong>Creator Pro Laptop · Recommended</strong><small>Best match for performance + mobility</small></div>",
      "compare":"<div class='user'>Compare the laptop with the tablet.</div><div class='bot'>For sustained creative work choose the laptop. The tablet wins for portability and quick review.</div><div class='chips'><i>Performance: Laptop</i><i>Mobility: Tablet</i></div>"
    }
    widget=f"<aside class='widget'><div class='wh'><b>✦ Nexus AI<br><small style='color:#77849a'>Shopping assistant</small></b><span class='online'>● ONLINE</span></div><div class='chat'>{msgs[mode]}</div></aside>"
    body="""<div class='nav'><div class='brand'>NOVA <i>TECH</i></div><div><span>DEVICES</span><span>COLLECTIONS</span><span>SUPPORT</span></div></div><section class='hero'><div><div class='eyebrow'>SMARTER SHOPPING · POWERED BY NEXUS AI</div><h1>Better tech.<br>Smarter choice.</h1><p>A sanitized storefront demo showing how Nexus AI can live inside a client brand instead of replacing it.</p></div><div class='art'><div class='cube'></div></div></section><section class='products'><div class='grid'><div class='card'><div class='pic'>▣</div><b>Creator Pro Laptop</b><small>Performance workstation</small></div><div class='card'><div class='pic'>◉</div><b>Pulse Watch</b><small>Everyday intelligence</small></div><div class='card'><div class='pic'>◫</div><b>Studio Tablet</b><small>Portable creative canvas</small></div></div></section>"""
    return shell(body+widget,css)

def persona():
    css="""
    .stage{height:900px;background:radial-gradient(circle at 72% 20%,#765cf644,transparent 28%),radial-gradient(circle at 18% 82%,#35ccec22,transparent 30%),#070a12;display:grid;grid-template-columns:1fr 430px}.catalog{padding:70px}.tag{font-size:9px;letter-spacing:1.5px;color:#9c8cff}.catalog h1{font-size:42px;line-height:1.1;margin:10px 0}.catalog>p{color:var(--muted);font-size:12px;max-width:500px;line-height:1.7}.cards{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:34px}.card{height:180px;border:1px solid var(--line);border-radius:18px;background:linear-gradient(145deg,#121927,#0c111d);padding:18px}.card span{font-size:32px}.card b{display:block;margin:16px 0 6px}.card small{color:var(--muted)}.side{border-left:1px solid var(--line);display:grid;place-items:center}.robot{width:270px;height:390px;position:relative}.head{position:absolute;left:35px;top:25px;width:200px;height:125px;border-radius:62px;background:linear-gradient(145deg,#e9f5f5,#80d5ca);box-shadow:0 25px 70px #35ccec22}.screen{position:absolute;inset:20px;border-radius:40px;background:#121a2c}.eye{position:absolute;top:38px;width:24px;height:24px;border-radius:50%;background:white}.eye:after{content:'';position:absolute;inset:7px;border-radius:50%;background:#765cf6}.e1{left:38px}.e2{right:38px}.body{position:absolute;left:68px;top:160px;width:135px;height:150px;border-radius:35px;background:linear-gradient(145deg,#263149,#151c2c);border:1px solid #394761}.body:after{content:'NEXUS AI';position:absolute;top:62px;left:26px;font-size:15px;font-weight:900;color:#dce4f2}.jet{position:absolute;bottom:18px;left:91px;width:34px;height:70px;border-radius:50%;background:linear-gradient(#fff,#35ccec);filter:drop-shadow(0 0 15px #35ccec)}.jet.j2{left:148px}.bubble{position:absolute;right:220px;top:70px;width:245px;background:#fff;color:#11182a;padding:16px;border-radius:18px;font-size:11px;line-height:1.5;box-shadow:0 25px 70px #0008}.bubble b{color:#765cf6}
    """
    body="""<div class='stage'><section class='catalog'><div class='tag'>CONTEXT-AWARE COMMERCE PERSONA</div><h1>Products become<br>conversation context.</h1><p>The assistant can react to the product a shopper is exploring and turn catalog context into a focused recommendation.</p><div class='cards'><div class='card'><span>◈</span><b>Noir 01</b><small>Woody · evening · confident</small></div><div class='card'><span>▣</span><b>Creator Pro</b><small>Design · performance · mobile</small></div><div class='card'><span>◉</span><b>Pulse Atelier</b><small>Gift · classic · refined</small></div><div class='card'><span>◇</span><b>Frame One</b><small>Lightweight · everyday</small></div></div></section><aside class='side'><div class='robot'><div class='bubble'><b>Creator Pro</b> matches this shopper best: strong creative performance without giving up portability.</div><div class='head'><div class='screen'><i class='eye e1'></i><i class='eye e2'></i></div></div><div class='body'></div><div class='jet'></div><div class='jet j2'></div></div></aside></div>"""
    return shell(body,css)

PREVIEWS={
 "nexus-admin-overview.png":admin("overview"),
 "nexus-admin-add-store.png":admin("modal"),
 "nexus-admin-architecture.png":admin("architecture"),
 "nexus-robot-phone.png":persona(),
 "nexus-robot-perfume.png":persona(),
 "nexus-robot-watch.png":persona(),
 "nexus-client-welcome.png":storefront("welcome"),
 "nexus-client-recommendation.png":storefront("recommend"),
 "nexus-client-comparison.png":storefront("compare"),
}
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={"width":1440,"height":900},device_scale_factor=1)
    for name,html in PREVIEWS.items():
        page.set_content(html,wait_until="load")
        page.screenshot(path=str(OUT/name),full_page=False)
    browser.close()
print(f"Generated {len(PREVIEWS)} sanitized Nexus AI showcase previews.")
