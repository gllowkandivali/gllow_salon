from flask import Flask, render_template, request, redirect
import urllib.parse
import mysql.connector
import smtplib
from email.mime.text import MIMEText

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = "gllow_salon_secret_2026"

# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host="metro.proxy.rlwy.net",
        user="root",
        password="AYSlCiFitVZbCLupJVvPbODqkfzQwWkT",
        database="railway",
        port=37012
    )

# ---------------- EMAIL CONFIG ----------------
SENDER_EMAIL = "Gllowkandivali@gmail.com"
APP_PASSWORD = "cnzl qnaq xnwg rbzv"

def send_email(to, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = to

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print("Email error:", e)

# ---------------- HOME ----------------
offers = [
    {"title": "50% OFF Facial ✨", "desc": "Limited time offer"},
    {"title": "Hair Spa @ ₹299 💇‍♀️", "desc": "Weekend Special"},
    {"title": "Free Eyebrow with Facial 💅", "desc": "Combo Offer"}
]

@app.route("/")
def home():
    return render_template("index.html", offers=offers)

# ---------------- PAGES ----------------
@app.route("/booking")
def booking():
    return render_template("booking.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/courses")
def courses():
    return render_template("courses.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/register")
def register():
    return render_template("register.html")

# ---------------- BOOKING ----------------
@app.route("/submit", methods=["POST"])
def submit():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        service = request.form.get("services")
        date = request.form.get("date")
        time = request.form.get("time")

        if not service:
            service = "Not selected"

        print("DEBUG:", name, phone, email, service, date, time)

        # -------- SAVE TO DATABASE --------
        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO bookings (name, phone, email, service, date, time) VALUES (%s,%s,%s,%s,%s,%s)",
            (name, phone, email if email else None, service, date, time)
        )

        db.commit()
        cursor.close()
        db.close()

        # -------- EMAIL --------
        try:
            is_bridal = "Bridal" in service

            if email:
                if is_bridal:
                    user_msg = f"""
Hi {name},

✨ Bridal Booking Confirmed 👰✨

Service: {service}
Date: {date}
Time: {time}

Our team will contact you for full bridal consultation 💖

Thank you for choosing Gllow Salon ✨
"""
                else:
                    user_msg = f"""
Hi {name},

Your appointment is confirmed 💖

Service: {service}
Date: {date}
Time: {time}

Thank you for choosing Gllow Salon ✨
"""

                send_email(email, "Appointment Confirmed 💅", user_msg)

            # Owner email
            owner_msg = f"""
🔥 New Booking Alert

Name: {name}
Phone: {phone}
Service: {service}
Date: {date}
Time: {time}
"""
            send_email(SENDER_EMAIL, "New Booking 🚨", owner_msg)

        except Exception as mail_error:
            print("Email failed:", mail_error)

        # -------- WHATSAPP --------
        message = f"""
Hi Gllow Salon 💖

✨ New Booking Request ✨

Service: {service}
Date: {date}
Time: {time}

Customer:
{name}
📞 {phone}

💄 Bridal & Makeup bookings available 👰
"""

        whatsapp_url = "https://wa.me/919819545630?text=" + urllib.parse.quote(message)

        return redirect(whatsapp_url)

    except Exception as e:
        print("ERROR:", e)
        return f"Error: {str(e)}"

# ---------------- CONTACT ----------------
@app.route("/contact_submit", methods=["POST"])
def contact_submit():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        message = request.form.get("message")

        msg = f"""
New Contact Message 💬

Name: {name}
Phone: {phone}
Email: {email}

Message:
{message}
"""
        send_email(SENDER_EMAIL, "New Contact Form 📩", msg)

        return "Message Sent Successfully 💖"

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- REGISTER ----------------
@app.route("/register_submit", methods=["POST"])
def register_submit():
    try:
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        course = request.form.get("course")
        batch = request.form.get("batch")

        if email:
            user_msg = f"""
Hi {name},

You are successfully registered 🎓

Course: {course}
Batch: {batch}

We will contact you soon 💖
"""
            send_email(email, "Course Registration Confirmed 🎓", user_msg)

        owner_msg = f"""
New Student Registration 🔥

Name: {name}
Phone: {phone}
Course: {course}
Batch: {batch}
"""
        send_email(SENDER_EMAIL, "New Student 🚨", owner_msg)

        return "Registration Successful 🎓"

    except Exception as e:
        return f"Error: {str(e)}"

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)