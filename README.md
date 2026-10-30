# Excel Option Chain - AngelOne WebSocket v2 (Python)

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![WebSocket](https://img.shields.io/badge/WebSocket-✔-green)](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)
[![HTTPS](https://img.shields.io/badge/HTTPS-Secure-orange)](https://en.wikipedia.org/wiki/HTTPS)

📈 This repository provides a **pure Python implementation** for fetching **real-time option chain data** from **AngelOne WebSocket v2** and saving it to **Excel**. 

---


## 📡 AngelOne API Endpoints Used  

### ✅ **Fetching LTP (Last Traded Price)**  
🔗 **API:** [AngelOne LTP API](https://apiconnect.angelone.in/rest/secure/angelbroking/market/v1/quote/)  

### ✅ **Fetching Instrument Tokens**  
🔗 **API:** [AngelOne OpenAPI ScripMaster](https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json/)  

### ✅ **WebSocket v2 for Live Data**  
🔗 **GitHub:** [AngelOne Smart WebSocket V2](https://github.com/angel-one/smartapi-python/blob/main/SmartApi/smartWebSocketV2.py)  

---
![Screenshot 1](assets/Screenshot%20(3473).png)

![Screenshot 2](assets/Screenshot%20(3474).png)

![Screenshot 3](assets/Screenshot%20(3475).png)
---
## 🎥 YouTube Video  
📌 Watch the complete tutorial on YouTube:  
🔗 [Click Here to Watch](https://youtu.be/JbpYethcRF4)  

---

## 🚀 Features
✅ **Live Option Chain Data Fetching** from **AngelOne WebSocket v2**  
✅ **Secure HTTPS API Integration** for additional data retrieval  
✅ **Excel File Handling** - Save and analyze data in Excel format  
✅ **Asynchronous WebSocket Implementation** for efficient processing  
✅ **Easy to Modify & Extend** for trading strategies  

---

## 🚀 What's New in v2.0.0

### 🌐 Enhanced Connectivity & Security Upgrade
* **HTTPS API Integration:** Upgraded security protocols for robust and secure data transfer alongside Angel One WebSockets (v2).
* **High-Throughput Streaming:** Seamless tick-by-tick real-time option chain data streaming with optimized latency.

### 📊 Advanced Nifty & BankNifty Weekly Range Metrics
* **Calculated Weekly Ranges:** Highly accurate weekly support and resistance range algorithms for Nifty and BankNifty, derived after extensive statistical testing.
* **Paper Trading Support:** Native structure to simulate strategies and test paper trades before executing live capital.

### 🎯 OI Percentage & Market Direction Dynamics
* **Institutional-Grade OI Tracking:** Integrated Open Interest (OI) concentration tracking logic based on key thresholds (e.g., 85%, 95% OI shifts).
* **At The Money (ATM) State Analysis:** Live indicators when OI is heavily clustered at ATM.
* **WTB / WTT Detection:** Real-time detection of Weak Towards Bottom (WTB) or Weak Towards Top (WTT) shifts in momentum and institutional pressure to identify potential breakouts or breakdowns early.

### 🛠️ Key Improvements & Fixes
* Deleted deprecated files and cleaned up legacy codebase for faster load times.

---

## 📌 Installation

Make sure you have **Python 3.12+** installed.  

```sh
git clone https://github.com/Neeraj-prajapat/excel-option-chain.git
cd excel-option-chain
pip install -r requirements.txt


---

```

---

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://buymeacoffee.com/algolyte)
