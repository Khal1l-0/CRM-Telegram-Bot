# CRM Telegram Bot for Educational Centers

## 📌 Description
This Telegram bot is designed for educational center administrators, automating group management, notifications, and certificate generation. It helps reduce the workload on staff and improves the organization of the learning process.

The bot supports three languages: Russian, English, and Uzbek.

💡 **Important:** When creating new Telegram groups, the bot logs into the account to automatically add participants and manage the group.

🕐 **Logging:** Every day at 23:59, the bot automatically sends log files to the developer for monitoring and troubleshooting.

## 🔹 Features
✅ **Group management:** automatic group creation, adding and removing participants.  
✅ **Notifications:** sending reminders for lessons, notifications about cancellations, and important events.  
✅ **Certificate generation:** automatic generation of certificates upon course completion.  
✅ **Feedback:** accepts client requests and provides information about the center.  

## ✅ Roles
- **CEO:** Full access, including adding and managing subjects and teachers. Can manage all aspects of the system.
- **Administrator:** Access to group management, sending notifications, and managing participants.
- **Teacher:** Access to assigned groups and ability to work with teaching materials.

💡 For stable bot operation, it is recommended to add subjects and teachers through the CEO role, and then proceed with administrative tasks.

## 🔧 Technologies Used
- **Python + Aiogram** — for interacting with the Telegram API.
- **Pillow** — for certificate generation.
- **SQLite** — database for storing information.

## 🚀 Installation and Setup
### Clone the repository:
```sh
git clone https://github.com/Khal1l-0/CRM-Telegram-Bot.git
cd repository
```

### Install dependencies:
```sh
pip install -r requirements.txt
```

### Set up environment variables:
In the `.env` file, add the following lines, replacing the values with your own:
```ini
API_ID=29586910  # Your API ID
API_HASH=5937975a3d8ab904b7f7a834cafe4076  # Your API Hash
TOKEN=7919609778:AAG2mlNACnBw-ApWgIikjxX8YiSrzwKmtVQ  # Your bot's token
BOT_LINK=uzadmincrm_bot  # Your bot's link
DEV=1624466663  # Your Telegram ID (or Developer ID)
```

### Run the bot:
```sh
python main.py
```

💡 Once the environment variables are set, the bot is ready to go! 🚀

---

P.S. The code is not perfect, but it works. Who has written perfect code anyway? 😉
