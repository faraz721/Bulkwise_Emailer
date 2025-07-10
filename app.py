import os
import csv
import smtplib
import ssl
import time
from flask import Flask, render_template, request, flash, redirect, url_for, session
from werkzeug.utils import secure_filename
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'bulkwise123'  # Required for session handling

UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE_MB = 30
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/preview', methods=['POST'])
def preview():
    session.clear()

    # Collect form data
    sender_email = request.form.get('sender_email')
    sender_password = request.form.get('sender_password')
    subject = request.form.get('subject')
    message_template = request.form.get('message')

    session['sender_email'] = sender_email
    session['sender_password'] = sender_password
    session['subject'] = subject
    session['message_template'] = message_template

    # Handle attachment
    attachment = request.files.get('attachment')
    attachment_name = "None"
    if attachment and attachment.filename:
        size_mb = len(attachment.read()) / (1024 * 1024)
        attachment.seek(0)
        if size_mb > MAX_FILE_SIZE_MB:
            flash(f"File too large. Max allowed size is {MAX_FILE_SIZE_MB} MB.")
            return redirect(url_for('index'))
        filename = secure_filename(attachment.filename)
        attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        attachment.save(attachment_path)
        attachment_name = filename
        session['attachment'] = attachment_name

    # Collect recipients
    recipients_dict = {}

    # From manual text
    recipient_text = request.form.get('recipient_emails')
    if recipient_text:
        for email in recipient_text.split(','):
            email_clean = email.strip()
            if email_clean:
                recipients_dict[email_clean] = {"name": "Dear", "email": email_clean}

    # From uploaded CSV
    email_file = request.files.get('email_file')
    if email_file and email_file.filename.endswith('.csv'):
        csv_data = email_file.stream.read().decode("utf-8").splitlines()
        reader = csv.DictReader(csv_data)
        for row in reader:
            name = row.get("Name", "").strip()
            email = row.get("Email", "").strip()
            if email and email not in recipients_dict:
                recipients_dict[email] = {"name": name or "Dear", "email": email}

    if not recipients_dict:
        flash("Please enter at least one email (textbox or CSV).")
        return redirect(url_for('index'))

    session['recipients'] = list(recipients_dict.values())

    return render_template(
        'preview.html',
        sender=sender_email,
        subject=subject,
        message=message_template,
        recipients=recipients_dict.values(),
        attachment=attachment_name
    )

@app.route('/send', methods=['POST'])
def send():
    sender_email = session.get('sender_email')
    sender_password = session.get('sender_password')
    subject = session.get('subject')
    message_template = session.get('message_template')
    attachment_name = session.get('attachment')
    recipients = session.get('recipients', [])

    attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], attachment_name) if attachment_name and attachment_name != "None" else None

    results = []

    try:
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
        server.login(sender_email, sender_password)

        for contact in recipients:
            name = contact["name"]
            recipient = contact["email"]
            personalized_msg = message_template.replace("{{name}}", name)

            msg = EmailMessage()
            msg["From"] = f"Ahmed Faraz Malik <{sender_email}>"
            msg["To"] = recipient
            msg["Subject"] = subject
            msg["Reply-To"] = sender_email

            msg.set_content(personalized_msg)
            html_content = f"""
            <html>
              <body>
                <p>{personalized_msg.replace('\n', '<br>')}</p>
              </body>
            </html>
            """
            msg.add_alternative(html_content, subtype='html')

            # Add attachment if exists
            if attachment_path:
                with open(attachment_path, "rb") as f:
                    file_data = f.read()
                    file_name = os.path.basename(attachment_path)
                    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

            try:
                server.send_message(msg)
                results.append(f"Sent to {recipient} ({name})")
            except Exception as e:
                results.append(f"Failed to send to {recipient} ({name}): {str(e)}")

            time.sleep(1)

        server.quit()

    except Exception as e:
        results.append(f"Error logging into email server: {str(e)}")

    return render_template(
        'result.html',
        sender=sender_email,
        recipients=[r['email'] for r in recipients],
        subject=subject,
        message=message_template,
        attachment=attachment_name,
        results=results
    )

# For deployment (Render, etc.)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
