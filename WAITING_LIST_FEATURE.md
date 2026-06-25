# Waiting List / User Approval System - Complete Implementation Guide

## Overview

The LMS now has a complete **User Approval / Waiting List System** that ensures only approved students and trainers can login and use the platform. Institutes have full control over who gets access to their educational resources.

---

## ✨ Features Implemented

### 1. **Registration with Pending Status**

- When students or trainers register, their account status is set to `pending`
- Their account is inactive (`is_active = 0`) until approved by the institute
- Both users receive an **automated email** confirming their registration is pending

### 2. **Enhanced Login Messages**

- **Pending Users**:
  - Message: "⏳ Your registration request is pending approval by the selected institution. We will notify you and send a confirmation email once the institute reviews your request. Typical approval time: 24-48 hours."
- **Rejected Users**:
  - Message: "❌ Your registration request has been rejected by the institution. You can try registering with a different institution or contact support for more information."

### 3. **Admin Approval Dashboard**

- Institute admins can view pending registrations at `/institute/approvals`
- Shows separate tabs for Students and Trainers
- Displays user details: name, email, phone, education level, specialization, experience
- Shows registration timestamp
- User's message to admin is displayed

### 4. **Approval & Rejection Actions**

- **Approve**: Activates the user, sends approval email, updates notifications
- **Reject**: Deactivates the user, sends rejection email with optional reason

### 5. **Email Notifications**

Three types of automated emails are sent:

#### a) **Pending Notification Email** (on registration)

- Subject: "Registration Pending - We'll Notify You Soon"
- Informs user their request is received and pending
- Shows typical approval timeline (24-48 hours)
- Provides next steps

#### b) **Approval Email** (when approved by admin)

- Subject: "✅ Your Registration Has Been Approved!"
- Informs user they can now login
- Direct login link provided
- Celebratory tone

#### c) **Rejection Email** (when rejected by admin)

- Subject: "Registration Request - Status Update"
- Informs user of rejection
- Includes rejection reason if provided by admin
- Suggests next steps

### 6. **Dashboard Stats**

- Institute dashboard shows count of pending approvals
- "Pending Approvals" stat card with quick action link
- Visual notification badge showing number of pending requests

---

## 🔧 Technical Implementation

### Database Schema

The existing `users` table already includes approval fields:

```sql
approval_status ENUM('pending', 'approved', 'rejected') DEFAULT 'approved'
approval_message TEXT
is_active TINYINT(1) DEFAULT 1
```

### User Flow Diagram

```
┌─────────────────┐
│  User Registers │
│  (Student/      │
│   Trainer)      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Account Created             │
│ - approval_status: pending  │
│ - is_active: 0              │
│ Email sent to user          │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│  Institute Admin Reviews    │
│  on /institute/approvals    │
└────────┬────────┬───────────┘
         │        │
    ┌────▼──┐  ┌──▼────┐
    │Approve│  │Reject │
    └────┬──┘  └──┬────┘
         │       │
         ▼       ▼
    ✅ Approved ❌ Rejected
    (Can Login) (Cannot Login)
```

### Key Routes

| Route                          | Method   | Purpose                        |
| ------------------------------ | -------- | ------------------------------ |
| `/register`                    | GET/POST | User registration              |
| `/login`                       | GET/POST | User login with approval check |
| `/institute/approvals`         | GET      | View pending requests          |
| `/institute/approve/<user_id>` | POST     | Approve a user                 |
| `/institute/reject/<user_id>`  | POST     | Reject a user                  |

### Email Configuration

Update the `EMAIL_CONFIG` in `app.py`:

```python
EMAIL_CONFIG = {
    'sender_email': 'your_email@gmail.com',      # Your Gmail
    'sender_password': 'your_app_password',       # Gmail App Password
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

#### How to Set Up Gmail:

1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password (16 characters)
3. Update the `EMAIL_CONFIG` with your email and app password

---

## 🔐 User Approval States

### State: **Pending**

- **User Can**: Only register and see pending message on login
- **User Cannot**: Login or access any platform features
- **Duration**: 24-48 hours (typical)
- **Notification**: Gets email updates

### State: **Approved**

- **User Can**: Login and access all features
- **is_active**: 1 (active)
- **Notification**: Gets approval email with login link

### State: **Rejected**

- **User Can**: Only see rejection message and try registering again
- **User Cannot**: Login or access any platform features
- **Notification**: Gets rejection email with reason

---

## 📊 Admin Dashboard Features

### Quick Stats Box

```
⏳ Pending Approvals: 5
[Review Now Button]
```

### Approvals Page (/institute/approvals)

**Students Tab:**

- List of pending student registrations
- Filter by education level
- Approve/Reject with optional reason

**Trainers Tab:**

- List of pending trainer registrations
- Filter by specialization and experience
- Approve/Reject with optional reason

---

## 🎯 Usage Instructions

### For Users (Students/Trainers):

1. **Register**: Fill the registration form for your role
2. **Confirmation**: Receive pending notification email
3. **Wait**: Institute admin reviews (typically 24-48 hours)
4. **Approval**: Receive approval email with login link
5. **Login**: Use email and password to access platform

### For Admins (Institutes):

1. **Review**: Go to Dashboard → "Review Now" or /institute/approvals
2. **Evaluate**: Review pending requests
3. **Decide**: Click "Approve & Activate" or enter reason and "Reject"
4. **Done**: User gets email notification automatically

---

## 📧 Email Template Examples

### Pending Registration Email

```
🎓 EduVerse LMS
═════════════════════════════════
Hi John,

Thank you for registering with Institute Name! Your registration
request has been received and is now pending approval.

✓ The administrator will review your request
✓ You'll receive an email notification once approved
✓ Once approved, you can log in and access all courses

Typical approval time: 24-48 hours
═════════════════════════════════
```

### Approval Email

```
🎉 Great News!
Hi John,

Your registration request for Institute Name has been APPROVED! ✅
You can now log in to EduVerse LMS and start exploring courses.

[Login Now Button]
═════════════════════════════════
```

### Rejection Email

```
Registration Update
Hi John,

Thank you for your interest in Institute Name.
Unfortunately, your registration request has been REJECTED ❌

You can try registering again in the future or contact another institute.
═════════════════════════════════
```

---

## 🚀 Testing the Feature

### Test Scenario 1: Registration and Pending Status

```
1. Register as a new student/trainer
2. Verify pending email is sent
3. Try to login → should see pending message
4. Verify is_active = 0 in database
```

### Test Scenario 2: Approval Flow

```
1. Login as institute admin
2. Go to /institute/approvals
3. Click "Approve & Activate" on a pending user
4. Verify approval email sent
5. Try to login as approved user → should work
6. Verify is_active = 1 in database
```

### Test Scenario 3: Rejection Flow

```
1. Login as institute admin
2. Go to /institute/approvals
3. Enter rejection reason
4. Click "Reject"
5. Verify rejection email sent with reason
6. Try to login as rejected user → should see rejection message
```

---

## 📋 File Changes Summary

### Modified Files:

1. **app.py**
   - Added email imports and configuration
   - Added email helper functions
   - Updated registration to send pending email
   - Enhanced login messages
   - Updated approve/reject routes to send emails

2. **requirements.txt**
   - Added Flask-Mail==0.9.1

3. **templates/institute/approvals.html**
   - Added rejection reason input field
   - Both students and trainers sections updated

### Database:

- No schema changes needed (approval fields already exist)

---

## ⚙️ Configuration Checklist

- [ ] Update EMAIL_CONFIG in app.py with your Gmail credentials
- [ ] Install Flask-Mail: `pip install Flask-Mail`
- [ ] Enable 2FA on Gmail account
- [ ] Generate Gmail App Password
- [ ] Test email sending with a test account
- [ ] Verify rejection reason field displays properly
- [ ] Check that pending notification emails are sent on registration

---

## 🐛 Troubleshooting

### Emails Not Sending?

- Verify EMAIL_CONFIG credentials are correct
- Check Gmail "Less secure app access" setting (or use App Password)
- Check spam folder for test emails
- View console output for email error messages

### Pending Users Can't See Pending Message?

- Clear browser cache
- Verify user.approval_status is set to 'pending' in database
- Check that is_active is 0

### Approval Button Not Working?

- Verify institute admin is logged in
- Check that user belongs to the institute
- Look for SQL errors in console

---

## 🔄 Next Steps (Optional Enhancements)

1. Add bulk approval feature
2. Add expiration timer (auto-reject after 30 days)
3. Send reminder emails to pending users after 24 hours
4. Add approval history/audit log
5. Add notification preferences for users
6. Implement SMS notifications (via Twilio)
7. Add approval workflow customization per institute

---

## 📞 Support

For issues with the waiting list system:

1. Check WAITING_LIST_FEATURE.md (this file)
2. Review application logs
3. Verify email configuration
4. Check database for user approval_status
5. Test with a fresh registration

---

**Implementation Date**: 2024
**Feature Status**: ✅ Complete and Ready
**Last Updated**: 2024-06-23
