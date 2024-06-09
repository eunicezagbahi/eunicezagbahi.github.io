import datetime
from flask import Flask, render_template, request, redirect, url_for
from google.oauth2 import service_account
from googleapiclient.discovery import build
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Replace 'path_to_credentials.json' with the path to your downloaded credentials file
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SERVICE_ACCOUNT_FILE = 'path_to_credentials.json'
CALENDAR_ID = 'primary'  # Change to your wife's Google Calendar ID

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=credentials)

def check_availability(date, time):
    date_time_str = f"{date}T{time}:00"
    date_time_obj = datetime.datetime.fromisoformat(date_time_str)
    start_time = date_time_obj.isoformat() + 'Z'
    end_time = (date_time_obj + datetime.timedelta(hours=1)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_time,
        timeMax=end_time,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    return len(events) == 0

def send_email(booking_details):
    email_user = 'your_email@example.com'
    email_password = 'your_email_password'
    email_send = 'your_wife_email@example.com'

    subject = 'New Booking'

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = f"New booking details:\n\n{booking_details}"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    text = msg.as_string()
    server.sendmail(email_user, email_send, text)
    server.quit()

@app.route('/', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']
        notes = request.form['notes']

        if not check_availability(date, time):
            return "The selected time slot is not available. Please choose another time."

        booking_details = f"Name: {name}\nContact: {contact}\nService: {service}\nDate: {date}\nTime: {time}\nNotes: {notes}"
        send_email(booking_details)
        return redirect(url_for('confirmation'))

    today = datetime.date.today().isoformat()
    return render_template('booking.html', today=today)

@app.route('/confirmation')
def confirmation():
    return "Your appointment has been booked successfully!"

if __name__ == '__main__':
    app.run(debug=True)

