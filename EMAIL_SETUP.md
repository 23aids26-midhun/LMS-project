# 🚀 Quick Setup Guide: Enable Email Notifications

## Step 1: Install Email Package

```bash
pip install -r requirements.txt
```

## Step 2: Get Gmail App Password

### If using Gmail:

1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification (if not already done)
3. Go back to Security → App passwords
4. Select Mail and Windows Computer
5. Copy the 16-character app password

### If using another email provider:

- Gmail: smtp.gmail.com:587
- Outlook: smtp-mail.outlook.com:587
- Yahoo: smtp.mail.yahoo.com:587

## Step 3: Update Configuration

Open `app.py` and find this section (around line 30):

```python
EMAIL_CONFIG = {
    'sender_email': 'your_email@gmail.com',      # ← CHANGE THIS
    'sender_password': 'your_app_password',       # ← CHANGE THIS
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

Replace with your actual credentials:

```python
EMAIL_CONFIG = {
    'sender_email': 'myemail@gmail.com',
    'sender_password': 'abcd efgh ijkl mnop',  # 16-char app password
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

## Step 4: Test the Setup

1. Start the Flask app: `python app.py`
2. Register a new student/trainer account
3. Check the email inbox for pending notification
4. If not received, check console for errors

## ✅ That's It!

The system is now ready to:

- Send pending registration emails ✉️
- Send approval emails when admin approves ✅
- Send rejection emails when admin rejects ❌

---

## 🎯 Default Behavior (Without Email Config)

If you don't set up email credentials:

- Emails will **fail silently** (no error, just won't send)
- All other features work normally
- Admin can still approve/reject users
- Users just won't get email notifications

**Recommendation**: Set up email to provide better user experience!

---

## ❓ Common Issues

**Issue**: "Emails not sending"

- ✓ Check if credentials are correct
- ✓ Verify you generated an App Password (not just your password)
- ✓ Check console for error messages

**Issue**: "SMTP Connection refused"

- ✓ Verify port 587 is not blocked on your network
- ✓ Try a different network or VPN

**Issue**: "Authentication failed"

- ✓ Double-check email address and app password
- ✓ Generate a new App Password

---

## 📱 View Waiting List

### For Institute Admins:

- Dashboard: http://localhost:5000/institute/dashboard
- Approvals: http://localhost:5000/institute/approvals

### Stats:

- Pending count shown in dashboard stat card
- Quick action buttons for faster access

---

**You're all set! 🎉**
