<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/megaraph/johnian-network">
    <img src="images/logo.png" alt="Logo" width="100" height="100">
  </a>

<h3 align="center"><span style="font-size: 2.5rem; font-weight: 700">Johnian Network<span></h3>
  <p align="center">
    <a href="https://johnian-network.herokuapp.com">View Demo</a>
    ·
    <a href="https://github.com/megaraph/johnian-network/issues">Report Bug</a>
    ·
    <a href="https://github.com/megaraph/johnian-network/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://johnian-network.herokuapp.com)

The Johnian Network is a simple discussion site where anyone can post comments and share images. There are boards dedicated to multiple topics, from Anime to technology, music, and movies. Johnian Network is an exclusive website only available to Johnians.

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email`, `email_client`, `project_title`, `project_description`

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Jinja](https://jinja.palletsprojects.com/en/3.0.x/)
* [Bootstrap](https://getbootstrap.com)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [SQLite](https://sqlite.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [WhiteNoise](http://whitenoise.evans.io/en/stable/)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* [Python](https://www.python.org/)
* pip

  ```sh
  python -m pip install --upgrade pip
  ```
* [Cloudinary account](https://cloudinary.com/)
* [Sendinblue account](https://www.sendinblue.com/)

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/megaraph/johnian-network.git
   ```
2. Change directory into cloned repository
   ```sh
   cd johnian-network
   ```
3. Create a virtual environment
   ```sh
   python -m venv venv
   ```
4. Activate virtual environment
   ```sh
   source venv/Scripts/Activate
   ```
5. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
6. Create .env file
   ```sh
   touch .env
   ```
7. Add necessary settings to the .env file
   ```
    TJN_DEBUG=1
    TJN_SECRET_KEY=<secret-key>
    TJN_SECURITY_PASSWORD_SALT=<security-salt>
    TJN_ADMINS=[{‘email’: <admin-email>, ‘password’: <admin-password>, ‘user_tag’: <admin-tag>, ‘profile_pic’: <admin-pic>}, ]

    CLOUDINARY_CLOUD_NAME=<cloudinary-cloud-name>
    CLOUDINARY_API_KEY=<cloudinary-api-key>
    CLOUDINARY_API_SECRET=<cloudinary-api-secret>

    TJN_SENDINBLUE_SEND_MAIL=<sendinblue-sender-mail>
    TJN_SENDINBLUE_API_KEY=<sendinblue-api-key>
    TJN_MAIL_PASSWORD=<sendinblue-mail-password>
   ```
8. In `johnian-network/website/user_list.py`, add all the emails you want to have access to the app
   ```py
   users = {
       'email': <is_teacher>,
       'email': <is_teacher>,
       'email': <is_teacher>,
   }
   ```
9. Create database
   ```sh
   python create_database.py
   ```
10. Run application 🚀
    ```sh
    python app.py
    ```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag *enhancement*.
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

thejohniannetwork@gmail.com

Project Link: [https://github.com/megaraph/johnian-network](https://github.com/megaraph/johnian-network)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/megaraph/johnian-network.svg?style=for-the-badge
[contributors-url]: https://github.com/megaraph/johnian-network/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/megaraph/johnian-network.svg?style=for-the-badge
[forks-url]: https://github.com/megaraph/johnian-network/network/members
[stars-shield]: https://img.shields.io/github/stars/megaraph/johnian-network.svg?style=for-the-badge
[stars-url]: https://github.com/megaraph/johnian-network/stargazers
[issues-shield]: https://img.shields.io/github/issues/megaraph/johnian-network.svg?style=for-the-badge
[issues-url]: https://github.com/megaraph/johnian-network/issues
[license-shield]: https://img.shields.io/github/license/megaraph/johnian-network.svg?style=for-the-badge
[license-url]: https://github.com/megaraph/johnian-network/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png