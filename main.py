from flask import Flask, request, render_template_string, session, redirect, url_for
import datetime

app = Flask(__name__)

# ---------------------------
# --- CONFIGURE HERE ------
# ---------------------------
ADMIN_USER = "H455AN"
ADMIN_PASS = "HASSAN-0.1"
app.secret_key = "change_this_to_a_random_secret"

# --- Logs ---
log_output = []

# ---------------------------
# --- LOGIN PAGE HTML ------
# ---------------------------
login_page = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Secure Login</title>
  <style>
    body, html {
      margin: 0;
      padding: 0;
      height: 100%;
      overflow: hidden;
      font-family: "Segoe UI", Roboto, Arial, sans-serif;
      color: #fff;
    }

    /* 🌧️ Rain background */
    canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background: #000000; /* 🔴 Dark Red background */
    }

    /* 🔲 Login Card - Glassmorphism */
    .login-box {
      background: rgba(255, 255, 255, 0.08);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 45px;
      border-radius: 18px;
      width: 90%;
      max-width: 420px;
      text-align: center;

      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);

      box-shadow: 0 12px 40px rgba(0,0,0,0.6);
      animation: fadeIn 1.2s ease-in-out;
    }

    .login-box h2 {
      margin-bottom: 25px;
      font-size: 26px;
      font-weight: 600;
      letter-spacing: 1px;
      color: #00ffcc;
    }

    input {
      padding: 14px;
      margin: 12px 0;
      border: none;
      border-radius: 10px;
      width: 100%;
      font-size: 16px;
      outline: none;
      transition: 0.3s;
    }
    input:focus {
      box-shadow: 0 0 8px #00ffcc;
    }

    button {
      padding: 14px;
      background: linear-gradient(135deg, #00ffcc, #28a745);
      color: white;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      font-size: 18px;
      width: 100%;
      font-weight: bold;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    button:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 15px rgba(0,255,200,0.4);
    }

    /* ✨ Smooth animation */
    @keyframes fadeIn {
      from { opacity: 0; transform: translate(-50%, -45%); }
      to { opacity: 1; transform: translate(-50%, -50%); }
    }

    /* 📱 Mobile responsive */
    @media (max-width: 600px) {
      .login-box {
        padding: 28px;
      }
      .login-box h2 {
        font-size: 22px;
      }
      input, button {
        font-size: 15px;
        padding: 12px;
      }
    }
  </style>
</head>
<body>
  <canvas id="rain"></canvas>
  <div class="login-box">
    <h2>🔐 HR LOCK NAME BOT</h2>
    <form action="/login" method="post">
      <input type="text" name="name" placeholder="👤 Username" required><br>
      <input type="password" name="password" placeholder="🔑 Password" required><br>
      <button type="submit">Login</button>
    </form>
  </div>

  <script>
    const canvas = document.getElementById("rain");
    const ctx = canvas.getContext("2d");
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    let drops = [];
    for (let i = 0; i < 200; i++) {
      drops.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        l: Math.random() * 1 + 15,
        xs: -1 + Math.random() * 2,
        ys: Math.random() * 10 + 10
      });
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.strokeStyle = "rgba(174,194,224,0.5)";
      ctx.lineWidth = 1;
      ctx.lineCap = "round";
      for (let d of drops) {
        ctx.beginPath();
        ctx.moveTo(d.x, d.y);
        ctx.lineTo(d.x + d.xs, d.y + d.l * d.ys / 20);
        ctx.stroke();
      }
      move();
    }

    function move() {
      for (let d of drops) {
        d.x += d.xs;
        d.y += d.ys;
        if (d.y > canvas.height) {
          d.x = Math.random() * canvas.width;
          d.y = -20;
        }
      }
    }

    function animate() {
      draw();
      requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener("resize", () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    });
  </script>
</body>
</html>
"""


# ---------------------------
# --- IFRAME PAGE HTML -----
# ---------------------------
# ---------------------------
# --- IFRAME PAGE HTML -----
# ---------------------------
iframe_page = """
<!doctype html>
<html>
<head>
  <title>Bot Hosting</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      margin: 0;
      height: 100vh;
      overflow: hidden;
      font-family: Arial, sans-serif;
      background: #000;
    }
    iframe {
      width: 100%;
      height: 100vh;
      border: none;
    }

    /* 🔘 Semi-transparent logout button */
    .logout-btn {
      position: fixed;
      top: 15px;
      right: 15px;
      background: rgba(255, 0, 0, 0.4); /* semi-transparent red */
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 20px;
      font-size: 14px;
      text-decoration: none;
      cursor: pointer;
      z-index: 1000;
      transition: 0.3s;
    }
    .logout-btn:hover {
      background: rgba(255, 0, 0, 0.7);
    }

    /* 📱 Mobile adjustments */
    @media (max-width: 600px) {
      .logout-btn {
        font-size: 12px;
        padding: 6px 12px;
        top: 10px;
        right: 10px;
      }
    }
  </style>
</head>
<body>
  <a href="/logout" class="logout-btn">Logout</a>
  <iframe src="http://fi8.bot-hosting.net:21565/"></iframe>
</body>
</html>
"""


# ---------------------------
# --- ROUTES ---------------
# ---------------------------
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('show_login'))
    return render_template_string(iframe_page, user=session['user'])

@app.route('/login', methods=['GET'])
def show_login():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template_string(login_page)

@app.route('/login', methods=['POST'])
def login():
    name = request.form.get('name', '')
    password = request.form.get('password', '')
    if name == ADMIN_USER and password == ADMIN_PASS:
        session['logged_in'] = True
        session['user'] = name
        log_output.append(f"[🔐] {name} logged in at {datetime.datetime.now().strftime('%H:%M:%S')}")
        return redirect(url_for('index'))
    else:
        log_output.append(f"[❌] Failed login attempt for '{name}'")
        return redirect(url_for('show_login'))

@app.route('/logout')
def logout():
    user = session.pop('user', None)
    session['logged_in'] = False
    log_output.append(f"[🚪] {user if user else 'User'} logged out")
    return redirect(url_for('show_login'))

# ---------------------------
# --- RUN -------------------
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
