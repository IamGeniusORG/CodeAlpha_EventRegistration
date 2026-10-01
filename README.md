# EventMaster - Event Registration System

A full-stack event management and registration web application built with **Django** and **Tailwind CSS**. This project was developed as part of the CodeAlpha Backend Development Internship.

## 🚀 Features

* **Event Management:** Admins can create, edit, and delete events (including dates, locations, and seat capacities).
* **Image Uploads:** Events support image banners for a rich, modern UI.
* **User Authentication:** Secure user registration, login, and logout flows using Django's built-in authentication system.
* **Smart Registration System:** 
  * Users can register for events.
  * Prevents double-booking (a user cannot register for the same event twice).
  * Enforces capacity limits (users cannot register if the event is full).
* **Personal Dashboard:** Authenticated users have a private dashboard to view and cancel their upcoming event registrations.
* **Modern UI:** fully responsive, clean, and modern user interface styled with Tailwind CSS.

## 🛠️ Tech Stack

* **Backend:** Python, Django 5.x
* **Database:** SQLite (default)
* **Frontend:** Django Templates, Tailwind CSS (via CDN)
* **Image Processing:** Pillow

## ⚙️ Local Setup & Installation

Follow these steps to run the project locally on your machine.

**1. Clone the repository**
```bash
git clone https://github.com/YOUR-USERNAME/CodeAlpha_EventRegistration.git
cd CodeAlpha_EventRegistration
```

**2. Create and activate a virtual environment**
*For Windows:*
```powershell
python -m venv venv
.\venv\Scripts\activate
```
*For macOS/Linux:*
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run database migrations**
```bash
python manage.py migrate
```

**5. Create a Superuser (Admin account)**
```bash
python manage.py createsuperuser
```
*(Follow the prompts to set up an admin username and password)*

**6. Start the development server**
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`. You can access the admin panel at `http://127.0.0.1:8000/admin/`.

## 🧪 Testing

The project includes automated tests to verify the core business logic (registration limits, duplicate prevention, and route protection).

To run the tests:
```bash
python manage.py test
```

## 📄 License

This project is open-source and available under the MIT License.
