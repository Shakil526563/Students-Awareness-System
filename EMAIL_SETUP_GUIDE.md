# 📧 Email Setup Guide

## Issue Diagnosed
The system was not sending emails because:
1. The email backend was set to "console" mode
2. Gmail authentication was failing

## How to Fix

### 1. Generate an App Password for Gmail

If you're using Gmail with 2-factor authentication (2FA), you need to use an App Password instead of your regular password:

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to Security → App passwords
3. Select "Mail" as the app and "Other" as the device
4. Enter a name like "Student Weather Awareness System"
5. Click "Generate"
6. Copy the 16-character App Password (no spaces)

If you don't have 2FA enabled, you'll need to:
1. Enable "Less secure app access" at https://myaccount.google.com/lesssecureapps
2. Note that Google is phasing this out, so App Passwords are preferred

### 2. Update Your .env File

Open your `.env` file and make these changes:

```bash
# Set your correct Gmail address
EMAIL_HOST_USER=your.email@gmail.com

# Replace with the App Password you generated
EMAIL_HOST_PASSWORD=abcdefghijklmnop

# Make sure this is set to 'smtp' (not 'console')
EMAIL_BACKEND=smtp
```

### 3. Test Email Sending

Run the included test script:

```bash
python test_email.py
```

If everything is configured correctly, you should see a successful message and receive the test email.

### 4. Troubleshooting

If emails still don't send:

1. **Authentication Error**: Verify your App Password is correct
2. **Gmail Settings**: Check if you need to enable "Less secure app access"
3. **Firewall Issues**: Make sure port 587 is not blocked
4. **Internet Connection**: Verify you're connected to the internet
5. **Rate Limits**: Gmail has sending limits that might affect bulk emails

### 5. Using Non-Gmail Providers

If you prefer using another email provider:
1. Update `EMAIL_HOST` in `settings.py` (currently set to "smtp.gmail.com")
2. Update `EMAIL_PORT` if needed (currently 587)
3. Update the credentials in your `.env` file

## Next Steps

Once your email is working:
1. Test the full system by making a request to `/api/awareness/`
2. Monitor for any errors in the Django console
3. Check that recipients actually receive the email alerts
