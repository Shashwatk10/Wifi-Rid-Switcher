# 🚀 WiFi Switcher

A simple yet practical tool designed to keep your college WiFi connection stable by automatically switching between multiple login IDs.
---
## 💡 Idea

College WiFi systems often have:

Login limits per ID
Speed throttling after usage
Frequent disconnections

This project solves that by using a list of IDs (RIDs) and automatically switching between them based on connection quality.
---
## ⚙️ Features
- 🔄 Automatic login to WiFi portal
- 📶 Monitors internet speed and connection stability
- 🔁 Switches IDs when performance drops
- 📂 Uses a list of IDs from a text file
- ⚡ Fully customizable for any college WiFi system
---
## 🧠 How It Works
- The program logs into your college WiFi portal using an ID from the list
- It continuously monitors the connection speed
- If the speed drops or the connection becomes unstable:
- It switches to another ID
- Repeats the process to maintain a stable connection
---
### 📁 Project Structure
```
wifi-switcher/
│── main.py
│── rids.txt
```
## 🛠️ Setup Instructions
1. Clone the Repository
- git clone https://github.com/your-username/wifi-switcher.git
- cd wifi-switcher
2. Configure Login Portal
- Inside the code, replace the login URL with your college WiFi portal address:
- LOGIN_URL = "YOUR_COLLEGE_WIFI_PORTAL_URL"
3. Add Your Own IDs
- Open rids.txt and replace the existing IDs with your own:
```
ID1
ID2
ID3
...
```
⚠️ The current IDs are specific to my college and won’t work for you.
4. File Placement (Important)
- Keep main.py and rids.txt in the same folder
OR
- If you want them in different locations, update the file path in the code:
file_path = "path/to/your/rids.txt"
5. Run the Program
python main.py
--- 
## ⚠️ Notes
- This project is just an idea implementation
- You are encouraged to modify and improve it
- Works best when adapted to your specific college network system
## 🔓 Open for Customization
#### Feel free to:
- Improve speed detection logic
- Add GUI
- Optimize switching algorithms
- Integrate smarter network checks
## 🤝 Contributing
Pull requests, ideas, and improvements are welcome!
# ⭐ Final Note
- This was built to solve a real everyday problem.
- If it helps you — or inspires you to build something better — that’s a win.