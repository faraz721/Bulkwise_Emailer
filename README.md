# bulkwise-emailer
> **Overview**
BulkWise Emailer is a web-based tool that helps you send emails to many people at once. You can either upload a CSV file with names and emails or type email addresses manually. You can write one email message and personalize it for each person using their name. You can also attach a file (like a PDF report), preview your message, and then send it. This tool is simple, clean, and works on mobile, tablet, and desktop.
Features

- Send bulk emails through your Gmail account
- Supports both manual and CSV-based email input
- Option to personalize each email using names (e.g., Dear Ali)
- File attachment support (up to 30MB)
- Responsive design that works on all devices
- Email preview before sending
- Summary of successful and failed deliveries
- Confirmation sound after sending

**Project Structure**

Bulkwise_Emailer/
├── app.py
├── requirements.txt
├── static/
│   ├── style.css
│   └── success.mp3
├── templates/
│   ├── index.html
│   ├── preview.html
│   └── result.html
├── uploads/
└── README.md

**How to Use This Tool**

1. Clone the Project
git clone https://github.com/yourusername/Bulkwise_Emailer.git
cd Bulkwise_Emailer
2. Install Python Requirements
Flask and Werkzeug
pip install Flask Werkzeug
3. Run the Project
python app.py
Then open your browser and visit: http://127.0.0.1:5000

**How to Fill the Form**

Sender Email: Your Gmail address (e.g., yourname@gmail.com)
App Password: Gmail App Password (Direct link: https://myaccount.google.com/apppasswords). Choose App: 'Mail', and Device: 'Other (Custom name)' → Enter: BulkWise. Click 'Generate'. Copy the 16-character code shown. Use this in the app.
Recipient Emails: Optional, comma-separated emails
Upload CSV: Optional, CSV with columns Name and Email
Subject: Your email subject
Message: Use {{name}} for personalization
Attachment: Optional file upload

**CSV Format Example**

Use this format for uploading recipients via CSV:
Name,Email
Ali,ali@gmail.com
Sara,sara@gmail.com

**Developer**
Ahmed Faraz Malik
