# 💻 KnownProgrammer

### Welcome to KnownProgrammer - a Django group project made by:

<style>

    .creators th {
        background: #393E46;
        color: white;
        text-align: center;
        font-size: 18px;
    }
    .creators td {
        text-align: center;
        color: #393E46;
        font-size: 18px;
        font-weight: bold;
    }
    .creators tr:nth-child(1) { 
        color: #27374D;
        background: #DDE6ED;

    }
    .creators tr:nth-child(2) { 
        color: #27374D;
        background: #DDE6ED;
    }
    .tech_table th {
        background: #DDE6ED;
        text-align: center;
    }
    .tech_table tr:nth-child(1) { 
        color: #F9F7F7;
        background: #393E46; 
        font-size: 18px;
    }
</style>

<div class="creators">

|          |                           Jakub Połeć                            |                                  Krystian Tworek                                   |                                     Oktawian Czakiert                                     | 
|:--------:|:----------------------------------------------------------------:|:----------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------------:|
|  GitHub  | [![GitHub](/README_images/GitHub.png)](https://github.com/jpol1) |       [![GitHub](/README_images/GitHub.png)](https://github.com/XDKrystian)        |        [![GitHub](/README_images/GitHub.png)](https://github.com/OktawianCzakiert)        
| LinkedIn |                                -                                 | [![LinkedIn](/README_images/LinkedIn.png)](https://linkedin.com/in/krystiantworek) | [![LinkedIn](/README_images/LinkedIn.png)](https://www.linkedin.com/in/oktawianczakiert/) |   

</div>

---

## Table of Contents

1. [Introduction](#-1-introduction)
2. [Technologies we use](#-2-technologies-we-use)
3. [Registration and Authentication](#-3-registration-and-authentication)
4. [Key Features](#-4-key-features)
5. [Getting started](#-5-getting-started)
6. [Usage](#-6-usage)
7. [Testing](#-7-testing)
8. [Project tree](#-8-project-tree)
9. [Quick View](#-9-quick-view)
10. [License](#-10-license)
11. [Contributing](#-11-contributing)

---

## 💥 1. Introduction

Looking for talented programmers? Look no further!  
KnownProgrammer is your one-stop solution for finding programmers
based on their experience, programming languages,
frameworks, ratings, and wage.

---

## 🕹 2. Technologies we use

<div class="tech_table">

| <img src="/README_images/Python.png" alt="Python" style="width:45px; height: 45px"/> | <img src="/README_images/Django.png" alt="Django" style="width:45px; height: 45px"/> | <img src="/README_images/Sqlite.svg" alt="SQLite" style="width:70px; height: 80x"/> | <img src="/README_images/Docker.png" alt="Docker" style="width:50px; height: 50px"/> | <img src="/README_images/Cloudinary.svg" alt="Cloudinary" style="width:50px; height: 50px"/> 
|:------------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------:|:------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------:|
|                                        Python                                        |                                        Django                                        |                                       SQLite                                        |                                        Docker                                        |                                          Cloudinary                                          

</div>
---

## 🔐 3. Registration and Authentication

KnownProgrammer ensures secure registration and authentication processes for all users.  
During the registration process, users are required to confirm their email address by clicking on the activation link
sent to the provided email.  
All passwords are hashed.

---

## 🔑 4. Key Features

- Search for programmers based on their experience level: junior, mid, or senior.
- Filter programmers by programming languages and frameworks they're proficient in.
- View programmers ratings to make informed decisions or rate them by yourself to help the others.
- Detailed profiles showcasing programmer's skills, experience, portfolio and wage.
- Add your own programmer profile, become a part of our community and let others find YOU.
- Two-way communication with other users via e-mail or built-in messages service.
- Secure authentication and authorization mechanisms.

---

## 🧾 5. Getting started

This guide will walk you through the steps required to set up and run the KnownProgrammer application.  
You can choose to set up the application manually or use Docker for containerization.

### 5.1. Prerequisites

Before you begin, make sure you have the following installed on your system:

- Git
- Python 3.11 or later
- pip (Python package manager)
- Docker (for Docker setup)
- You should be acquainted with these websites: docker.com, cloudinary.com.

### 5.2. Clone the Repository

Clone the KnownProgrammer repository to your local machine using the following command:

```bash
git clone https://github.com/grupaASDA/ZnanyProgramista
```

### 5.3. Set Up Environment Variables

You need to set up environment variables for the Django settings, Cloudinary API, and email service. This can be
done by creating a `.env` file in the root directory of the project (the same as we created envtemplate.txt) and
populating it with the necessary values:

```bash
# DJANGO SETTINGS
SECRET_KEY=
DEBUG=

# CLOUDINARY CREDENTIALS
CLOUD_NAME=
API_KEY=
API_SECRET=
DEFAULT_AVATAR=

# EMAIL SERVICE
EMAIL_BACKEND =
EMAIL_HOST =
EMAIL_PORT =
EMAIL_USE_TLS =
EMAIL_HOST_USER =
EMAIL_HOST_PASSWORD =

```

We encourage you to create your own Cloudinary profile and use it (it's free), but if you only want to take a quick look
at the project be welcomed to use our credentials for testing purposes.

```bash
# CLOUDINARY CREDENTIALS
CLOUD_NAME=dbpcaze0b
API_KEY=787543327423312
API_SECRET=G01odhZiyUhap46yn6zKcSkae3I
DEFAULT_AVATAR=https://res.cloudinary.com/dbpcaze0b/image/upload/v1711977624/avatars/kuehdldiq5ffkhzxg9ov.png
```

Link to template: [envtemplate.txt](knownProgrammer/knownProgrammer/envtemplate.txt)

> ⚠️
> Ensure to keep your `.env` file secure and never commit it to the repository to protect sensitive information.

### 5.4. Now you have two convenient options and one manual:

### 🐳 5.4.1. Docker Setup

#### Build the Docker Image and run the Container

You can run the KnownProgrammer application using Docker.  
Ensure that you are in `/ZnanyProgramista/knownProgrammer` directory before runing below command.

```bash
docker-compose up --build 
```

This command builds a Docker image named `knownProgrammer` based on the instructions in the `Dockerfile`
and `docker-compose.yaml`.  
Runs all commands to create database and populate it with data contained in `initial_db.json` fixture.  
Once the image is built, it will run automatically, making the application accessible at `http://0.0.0.0:8000/`.

### Ⓜ️ 5.4.2. Using Makefile

If you are working on Linux or MacOs you have already installed `make`,  
but if you are working on Windows you have to install it first or use manual option (see point 5.4.3).

Ensure that you are in `/ZnanyProgramista/knownProgrammer` directory before runing below command.

By executing this command you will create database, populate it with data contained in `initial_db.json` fixture and
run the apllication.

```bash
make all
```

The application will be accessible at `http://localhost:8000`

### 🤚 5.4.3. By hand

If you want to avoid using Docker and Makefile you can choose below approach to setup the project.

#### Install Dependencies

Navigate to the cloned repository's directory and install the required dependencies:

```bash
pip install -r requirements.txt

```

#### Create database and populate it with fixture

Ensure that you are in `/ZnanyProgramista/knownProgrammer` directory before runing below commands:

```bash
python manage.py makemigrations accounts communication programmers
python manage.py migrate
python manage.py loaddata initial_db.json
```

#### Run the Application

```bash
python manage.py runserver
```

The application will be accessible at `http://localhost:8000`

### 5.5. Conclusion

You can now access the KnownProgrammer application either through your local setup at
`http://localhost:8000` or through Docker at `http://0.0.0.0:8000/`.  
Enjoy using our service!

---

## 💡 6. Usage

- Register an account and confirm your e-mail to get full functionality access.
- Explore programmers site, rate them, contact them.
- Utilize Cloudinary for your avatar update.
- Create your own programmer profile to showcase your proficiency in different languages and frameworks.
- You can also use our testing accounts which are:
    - login: `admin@admin.com` , password: `admin`
    - login: `admin2@admin.com` , password: `admin`
    - login: `admin3@admin.com` , password: `admin`

---

## 🔬 7. Testing

```bash
Name                                                                Stmts   Miss  Cover   Missing
-------------------------------------------------------------------------------------------------
accounts/__init__.py                                                    0      0   100%
accounts/admin.py                                                       3      0   100%
accounts/apps.py                                                        4      0   100%
accounts/forms.py                                                      29      0   100%
accounts/managers.py                                                   20      9    55%   15, 26-34
accounts/migrations/0001_initial.py                                     6      0   100%
accounts/migrations/__init__.py                                         0      0   100%
accounts/models.py                                                     18      0   100%
accounts/templates/__init__.py                                          0      0   100%
accounts/tests.py                                                     124      0   100%
accounts/tokens.py                                                     10      1    90%   9
accounts/urls_accounts.py                                               5      0   100%
accounts/views/function_based_views.py                                160     69    57%   18-33, 51, 106-118, 120-134, 137-152, 155-170, 193-203, 218-230, 234, 237
accounts/views/generic_views.py                                         6      0   100%
communication/__init__.py                                               0      0   100%
communication/admin.py                                                  1      0   100%
communication/apps.py                                                   4      0   100%
communication/forms.py                                                  6      0   100%
communication/migrations/0001_initial.py                                7      0   100%
communication/migrations/__init__.py                                    0      0   100%
communication/models.py                                                 8      0   100%
communication/tests.py                                                213      0   100%
communication/urls_communication.py                                     3      0   100%
communication/views.py                                                120     15    88%   20, 27, 44, 61-67, 77-84, 91, 93, 106-113, 123-131
knownProgrammer/__init__.py                                             0      0   100%
knownProgrammer/asgi.py                                                 4      4     0%   10-16
knownProgrammer/settings.py                                            31      0   100%
knownProgrammer/urls.py                                                 4      0   100%
knownProgrammer/wsgi.py                                                 4      4     0%   10-16
manage.py                                                              11      2    82%   11-12
programmers/__init__.py                                                 0      0   100%
programmers/admin.py                                                    3      0   100%
programmers/apps.py                                                     4      0   100%
programmers/filters.py                                                  9      0   100%
programmers/forms.py                                                   24      1    96%   16
programmers/migrations/0001_initial.py                                  8      0   100%
programmers/migrations/0002_alter_programmerprofile_experience.py       4      0   100%
programmers/migrations/0003_alter_programmerprofile_experience.py       4      0   100%
programmers/migrations/0004_alter_programmerprofile_experience.py       4      0   100%
programmers/migrations/0005_alter_programmerprofile_experience.py       4      0   100%
programmers/migrations/0006_alter_programmerprofile_experience.py       4      0   100%
programmers/migrations/0007_alter_programmerprofile_experience.py       4      0   100%
programmers/migrations/0008_alter_programmerprofile_experience.py       4      0   100%
programmers/migrations/__init__.py                                      0      0   100%
programmers/models.py                                                  40      5    88%   59, 68, 80-81, 90
programmers/services/__init__.py                                        0      0   100%
programmers/services/cloudinary.py                                     15      0   100%
programmers/templatetags/__init__.py                                    1      0   100%
programmers/templatetags/stars.py                                      20      1    95%   9
programmers/tests.py                                                  469      0   100%
programmers/urls_programmers.py                                         3      0   100%
programmers/views.py                                                  216     10    95%   37, 40, 43, 46, 49, 52, 55, 72, 283-284
-------------------------------------------------------------------------------------------------
TOTAL                                                                1641    121    93%


```

---

## 🌳 8. Project Tree

```bash
ZnanyProgramista
├── README.md
└── knownProgrammer
    ├── Dockerfile
    ├── Makefile
    ├── accounts
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── managers.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── static
    │   │   ├── css
    │   │   │   ├── popup.css
    │   │   │   └── style.css
    │   │   ├── images
    │   │   │   ├── background.jpg
    │   │   │   ├── default_avatar.png
    │   │   │   ├── logo1.jpg
    │   │   │   ├── star-empty.png
    │   │   │   ├── star-full.png
    │   │   │   └── star-half.png
    │   │   └── js
    │   │       └── popup.js
    │   ├── templates
    │   │   ├── __init__.py
    │   │   └── accounts
    │   │       ├── about_us.html
    │   │       ├── account_delete_confirm.html
    │   │       ├── base.html
    │   │       ├── change_new_email_message.html
    │   │       ├── change_old_email_message.html
    │   │       ├── change_password.html
    │   │       ├── changed_password.html
    │   │       ├── data_privacy.html
    │   │       ├── home_page.html
    │   │       ├── login.html
    │   │       ├── password_reset_complete.html
    │   │       ├── password_reset_confirm.html
    │   │       ├── password_reset_done.html
    │   │       ├── register_user.html
    │   │       ├── reset_password.html
    │   │       ├── template_activate_account.html
    │   │       └── user_update_form.html
    │   ├── tests.py
    │   ├── tokens.py
    │   ├── urls_accounts.py
    │   └── views
    │       ├── function_based_views.py
    │       └── generic_views.py
    ├── communication
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── templates
    │   │   └── communication
    │   │       ├── message.html
    │   │       ├── my_messages_person_list.html
    │   │       ├── my_messages_with_correspondent.html
    │   │       ├── replay_message.html
    │   │       └── send_message.html
    │   ├── tests.py
    │   ├── urls_communication.py
    │   └── views.py
    ├── docker-compose.yaml
    ├── knownProgrammer
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── envtemplate.txt
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── mydatabase
    ├── programmers
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── filters.py
    │   ├── fixtures
    │   │   └── initial_db.json
    │   ├── forms.py
    │   ├── migrations
    │   │   ├── 0001_initial.py
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── services
    │   │   ├── __init__.py
    │   │   ├── cloudinary.py
    │   │   └── ratings_generator.py
    │   ├── templates
    │   │   └── programmers
    │   │       ├── my_profile.html
    │   │       ├── programmer_avatar_update.html
    │   │       ├── programmer_create_model_form.html
    │   │       ├── programmer_delete_confirm.html
    │   │       ├── programmer_detail.html
    │   │       ├── programmer_update_model_form.html
    │   │       ├── programmers_list.html
    │   │       └── rate_programmer.html
    │   ├── templatetags
    │   │   ├── __init__.py
    │   │   └── stars.py
    │   ├── tests.py
    │   ├── urls_programmers.py
    │   └── views.py
    ├── project_tree.txt
    └── requirements.txt


```

---

## 📷 9. Quick View

Below you find some screenshots from our app.

### About us

![About_us](/README_images/About_us.png)

### Programmers list:

![Programmers_list](/README_images/Programmers_list.png)

### Programmers list filtered:

![Programmers_list_filtered](/README_images/Programmers_list_filtered.png)

### Programmer detail:

![Programmer_detail](/README_images/Programmer_detail.png)

### Rating programmer:

![Rating_programmer](/README_images/Rating_programmer.png)

### Sending message to programmer:

![Sending_message_to_programmer](/README_images/Sending_message_to_programmer.png)

### My profile:

![My_profile](/README_images/My_profile.png)

### Register:

![Register](/README_images/Register.png)

### Login:

![Login](/README_images/Login.png)

### Password reset:

![Password_reset](/README_images/Password_reset.png)


---

## 📄 10. License

This project is licensed under the MIT License.

---

## 🤝 11. Contributing

Contributions are welcome! Please follow the Commonly Recognized
Contribution Guidelines

---

🔥 Thank you for choosing KnownProgrammer!   
We highly invite you to test it!

---
[Return to Table of Contenst](#table-of-contents)