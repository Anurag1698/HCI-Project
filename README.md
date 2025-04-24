# 📚 StudyRoom – Human-Computer Interaction Project

**StudyRoom** is a web-based platform developed as part of a Human-Computer Interaction (HCI) course project. It aims to provide an intuitive and user-friendly interface for students to manage their study sessions, track progress, and collaborate with peers.

---

## 🧠 Project Overview

The primary goal of StudyRoom is to enhance the learning experience by integrating HCI principles into a digital study environment. Key features include:

- **Session Management**: Create, join, and manage study sessions.
- **Progress Tracking**: Monitor study hours and topics covered.
- **Collaboration Tools**: Chat and share resources with study group members.
- **User Profiles**: Customize profiles and set study goals.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally:

### Prerequisites

- **Python 3.10.4**: Ensure Python is installed on your system. [Download Python](https://www.python.org/downloads/release/python-3104/)

### Installation

#### Clone the Repository

```bash
git clone https://github.com/Anurag1698/HCI-Project.git
cd HCI-Project
```

#### Create a Virtual Environment

```bash
python -m venv myenv
```

#### Activate the Virtual Environment

- On **Windows**:
  ```bash
  myenv\Scripts\activate
  ```

- On **macOS/Linux**:
  ```bash
  source myenv/bin/activate
  ```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

#### Apply Migrations

```bash
python manage.py migrate
```

#### Run the Development Server

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

---

## 🛠️ Technologies Used

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Version Control**: Git

---

## 📁 Project Structure

- `StudyRoom/`: Main application directory.
- `templates/`: HTML templates for rendering views.
- `static/assets/`: Static files like CSS, JavaScript, and images.
- `media/`: Uploaded media files.
- `requirements.txt`: Python dependencies.
- `manage.py`: Django's command-line utility.

---

## 👥 Contributors

- **Anurag** – [Anurag1698](https://github.com/Anurag1698)
