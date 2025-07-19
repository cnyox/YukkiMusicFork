<img src="https://telegra.ph/file/c0e014ff34f34d1056627.png" align="right" width="200" height="200"/>

# Yukki Music Bot <img src="https://img.shields.io/github/v/release/TeamYukki/YukkiMusicBot?color=black&logo=github&logoColor=black&style=social" alt="RELEASE">

[Yukki Music Bot](https://github.com/TeamYukki/YukkiMusicBot) is a Powerful Telegram Music+Video Bot written in Python using Pyrogram and Py-Tgcalls by which you can stream songs, video and even live streams in your group calls via various sources.

* Youtube, Soundcloud, Apple Music, Spotify, Resso, Live Streams and Telegram Audios & Videos support.
* Written from scratch, making it stable and less crashes with attractive thumbnails.
* Loop, Seek, Shuffle, Specific Skip, Playlists etc support
* Multi-Language support


# ⚡️ Getting Started [[Documentation](https://notreallyshikhar.gitbook.io/yukkimusicbot/)]

> The official [documentation site](https://notreallyshikhar.gitbook.io/yukkimusicbot/) contains a lot of information. The best place to start is from the deployment section.

## ⚠️ Heroku Deployment

<h4>Click the button below to deploy Yukki on Heroku!</h4>    
<a href="https://heroku.com/deploy?template=https://github.com/cntml/YukkiMusicFork"><img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blueviolet?style=for-the-badge&logo=heroku" width="200""/></a>

> Want detailed explanation of Heroku Deployment? [Click Here](https://notreallyshikhar.gitbook.io/yukkimusicbot/deployment/heroku)


## 🍪 Avoiding Bans

### Option 1: Premium API
```env
API_URL=https://tgmusic.fallenapi.fun
API_KEY=your-secret-key
```
📌 Get keys: [Contact @AshokShau](https://t.me/AshokShau) or [@FallenApiBot](https://t.me/FallenApiBot)

## Option 2: Cookies

# **📜 Using Cookies for Authentication**  

### **🔹 Method: Netscape HTTP Cookie File**  
To authenticate requests using browser cookies, follow these steps:  

> ⚠️ **Important Note:**  
> - Always use a **secondary account** for generating cookies.  
> - Once cookies are uploaded, **do not log in again** on that account—it may invalidate the session prematurely.  

---

## **📌 Step 1: Export Cookies in Netscape Format**  
Use a browser extension to export cookies as a **`cookies.txt`** file in **Netscape HTTP format**:  

### **🌐 Recommended Extensions:**  
| Browser | Extension | Download Link |  
|---------|-----------|---------------|  
| **Chrome** | `Get cookies.txt` | [Chrome Web Store](https://chromewebstore.google.com/detail/get-cookiestxt-clean/ahmnmhfbokciafffnknlekllgcnafnie) |  
| **Firefox** | `cookies.txt` | [Firefox Add-ons](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) |  

### **📥 How to Export:**  
1. Install the extension.  
2. Navigate to the target website (YouTube.com) and log in.  
3. Click the extension icon and select **"Export cookies.txt"**.  
4. Save the file.  

---

## **📌 Step 2: Upload Cookies to a Paste Service**  
Host your `cookies.txt` on a text-sharing service:  

### **🔗 Recommended Paste Services:**  
- **[BatBin](https://batbin.me)** (Recommended, no login required)  
- **[PasteBin](https://pastebin.com)** (Requires account for long-term pastes)  

### **📤 Upload Steps:**  
1. Open the paste service.  
2. Copy-paste the **entire content** of `cookies.txt`.  
3. Click **"Create Paste"** and copy the URL.  

---

## **📌 Step 3: Set the Environment Variable**  
Add the paste URL to your **`COOKIES_URL`** environment variable.  

### **⚙️ Example:**  
```env
COOKIES_URL=https://batbin.me/abc123, https://pastebin.com/raw/xyz456
```  
*(Supports multiple URLs separated by commas)*  

---

### **❓ Troubleshooting**  
🔸 **Session Invalid?** → Generate new cookies and avoid logging in elsewhere.  
🔸 **403 Errors?** → Ensure cookies are fresh and not expired.

---

### **✅ Best Practices**  
✔ **Rotate cookies** periodically to avoid bans.  
✔ **Use private/incognito mode** when generating cookies.  
✔ **Monitor session activity** to detect early invalidation.  

---

#### **🎉 Enjoy using cookies!**

---

## 🖇 Generating Pyrogram String Session

<p>
<a href="https://telegram.tools/session-string-generator#pyrogram"><img src="https://img.shields.io/badge/Generate%20On%20Site-blueviolet?style=for-the-badge&logo=appveyor" width="200""/></a>
<a href="https://t.me/strgen_bot"><img src="https://img.shields.io/badge/TG%20String%20Gen%20Bot-blueviolet?style=for-the-badge&logo=appveyor" width="200""/></a>
</p>

## 🖇 VPS Deployment

1. **Upgrade & Update:**
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **Install Required Packages:**
   ```bash
   sudo apt-get install python3-pip ffmpeg -y
   ```
3. **Setting up PIP**
   ```bash
   sudo pip3 install -U pip
   ```
4. **Installing Node**
   ```bash
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash && source ~/.bashrc && nvm install v18
   ```
5. **Clone the Repository**
   ```bash
   git clone https://github.com/cntml/YukkiMusicFork && cd YukkiMusicFork
   ```
6. **Install Requirements**
   ```bash
   pip3 install -U -r requirements.txt
   ```
7. **Create .env  with sample.env**
   ```bash
   cp sample.env .env
   ```
   - Edit .env with your vars
8. **Editing Vars:**
   ```bash
   vi .env
   ```
   - Edit .env with your values.
   - Press `I` button on keyboard to start editing.
   - Press `Ctrl + C`  once you are done with editing vars and type `:wq` to save .env or `:qa` to exit editing.
9. **Installing tmux**
    ```bash
    sudo apt install tmux -y && tmux
    ```
10. **Fill vars through setup cmd**
    ```bash
     bash setup
     ```
11. **Run the Bot**
    ```bash
    bash start
    ```

# 🏷 Support / Assistance

Reach out to the maintainer at one of the following places:

- [GitHub Issues](https://github.com/TeamYukki/yukkimusicbot/issues/new?assignees=&labels=question&template=SUPPORT_QUESTION.md&title=support%3A+)
- Contact options listed on [this GitHub profile](https://github.com/TeamYukki)
- [Telegram Support](https://t.me/YukkiSupport)

If you want to say **thank you** or/and support active development of YukkiMusicBot:

- Add a [GitHub Star](https://github.com/TeamYukki/YukkiMusicBot) to the project.
- Fork the Repo :)
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your personal blog.

Together, we can make **YukkiMusicBot** better!
# 📑 Acknowledgement / Credits

Special thanks to these amazing projects/people which/who help power Yukki Music Bot:

- [Pyrogram](https://github.com/pyrogram/pyrogram)
- [Py-Tgcalls](https://github.com/pytgcalls/pytgcalls)
- [CallsMusic Team](https://github.com/Callsmusic)
- [TheHamkerCat](https://github.com/TheHamkerCat)
- [Charon Baglari](https://github.com/XCBv021)


Reminder that you are great, you are enough, and your presence is valued. If you are struggling with your mental health, please reach out to someone you love and consult a professional.
