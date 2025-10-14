# Automatic Database Backup

### 📦 Module Version: 1.0.0  
**Compatible with:** Odoo 17 , Odoo 18 & Odoo 19 (Community and Enterprise)

---

## 🧭 Overview
The **Automatic Database Backup** module helps you protect your business data by scheduling automatic Odoo database backups.  
You can configure when, where, and how your backups are created — ensuring that your data is safe and easily restorable at any time.

With this module, you no longer need to manually back up your database. It works silently in the background using Odoo’s cron scheduler.

---

## 🚀 Key Features

- 🕒 **Automatic Scheduled Backups** — daily, weekly, or custom intervals.  
- 💾 **Local or Remote Storage** (optional cloud integration).  
- 🔐 **Secure Backup Creation** — full database dump with file integrity.  
- 🧾 **Backup Management Interface** — view, download, or delete backups.  
- 📊 **Backup Logs & History** — track every backup action.  
- 📩 **Optional Notifications** (email/WhatsApp) on backup success or failure.  
- ⚙️ **Easy Configuration** in Odoo backend (no technical knowledge required).

---

## ⚙️ Installation

1. Copy the module folder **`db_auto_backup`** into your Odoo `addons` directory.
2. Restart the Odoo server:
   ```bash
   sudo systemctl restart odoo
   ```
