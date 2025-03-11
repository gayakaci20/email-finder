# **Email Finder**  

A **Python tool** for **generating** and **validating** email address formats based on names. It supports **multiple email styles** and provides both **CLI and GUI interfaces**.  

---

## **✨ Features**  

✔️ **Multiple email format options:**  
   - `firstname.lastname` → **john.doe@domain.com**  
   - `f.lastname` → **j.doe@domain.com**  
   - `firstname.l` → **john.d@domain.com**  
   - `firstnamelastname` → **johndoe@domain.com**  
   - `flastname` → **jdoe@domain.com**  
   - `lastname.firstname` → **doe.john@domain.com**  
   - `l.firstname` → **d.john@domain.com**  
   - `initials` → **jd@domain.com**  

✔️ **Email validation & deliverability checking**  
✔️ **Batch processing** for multiple names  
✔️ **Handles special characters & accents**  
✔️ **Supports both CLI and GUI**  

---

## **⚙️ Installation**  

1️⃣ **Clone the repository** or download the source code.  
2️⃣ **Create and activate a virtual environment** (recommended):  
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```  
3️⃣ **Install required dependencies:**  
```bash
pip install email-validator
```  

---

## **🚀 Usage**  

### **📌 Command-Line Interface (CLI)**  

Run the tool via CLI:  
```bash
python email-formatter1.py
```  
Follow the prompts to:  
1️⃣ **Enter names** (one per line, press **Enter** twice to finish)  
2️⃣ **Specify the email domain**  
3️⃣ **Choose an email format or validation option**  

### **🖥️ Graphical User Interface (GUI)**  

Run the GUI version:  
```bash
python email_formatter_gui.py
```  
The GUI provides a user-friendly interface with the **same features** as the CLI.  

---

## **🎯 Email Format Options**  

1️⃣ **firstname.lastname** → **john.doe@domain.com**  
2️⃣ **f.lastname** → **j.doe@domain.com**  
3️⃣ **firstname.l** → **john.d@domain.com**  
4️⃣ **firstnamelastname** → **johndoe@domain.com**  
5️⃣ **flastname** → **jdoe@domain.com**  
6️⃣ **lastname.firstname** → **doe.john@domain.com**  
7️⃣ **l.firstname** → **d.john@domain.com**  
8️⃣ **initials** → **jd@domain.com**  

---

## **✅ Email Validation**  

🔹 **Checks for:**  
✔️ Proper **email formatting**  
✔️ **Domain validity**  
✔️ **Deliverability** (if validation option is enabled)  

---

## **🛠️ Special Features**  

✔️ **Handles multi-word names** → Uses the first and last word  
✔️ **Removes special characters & accents**  
✔️ **Converts text to lowercase**  
✔️ **Tests all possible formats** to find valid emails  
✔️ **Batch processing** → Process multiple names at once  

---

## **🤝 Contributing**  

💡 **Contributions are welcome!** Feel free to submit a **Pull Request**.  

---

## **📜 License**  

This project is **open-source** under the **MIT License**. 🚀