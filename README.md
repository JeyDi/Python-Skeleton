
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->


<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url] -->



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://https://github.com/JeyDi/Python-Skeleton">
    <img src="img/scheleton.png" alt="Logo" width="280" height="200">
  </a>

  <h3 align="center">Python Skeleton Project</h3>
  <br>
<!-- 
  <p align="center">
    project_description
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</p> -->



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
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
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

The goal of this project is to define a Python Scheleton for your every Python project.


### Built With

* [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/)
* [poetry](https://python-poetry.org/)
* [pytest](https://docs.pytest.org/en/6.2.x/)
* [vscode dev-container](https://code.visualstudio.com/docs/remote/containers)



<!-- GETTING STARTED -->
## Getting Started

If you want to use this scheleton app project you can use cookiecutter to download and use the template.

Look into the **Installation** section if you want to know how to use and install this project.

### Prerequisites

If you want to use this project with cookiecutter make sure to have this tools installed
- python (3.8 or +): better: 3.8.10
- cookiecutter
- poetry (if you want to test the example project after the download)
- docker
- docker-compose

If you don't know how to install this requirements please check this [site](pythonbiellagroup.it) or google it :) 

### Installation

Cookiecutter is a project template configurator: allows you to download and configure your project easily and in a very simple way.

First of all you have to install cookiecutter on your system.

If you want to download the project using `cookiecutter` you can in your terminal launch:

```bash

# if you are using gitlab with https
cookiecutter https://github.com/JeyDi/Python-Skeleton

# if you are using gitlab with ssh
cookiecutter git@github.com:JeyDi/Python-Skeleton.git

```

And then follow the instruction in the terminal to clone the project.

Then look the **usage** next section to understand how to use the examples.


<!-- USAGE EXAMPLES -->
## Usage

### Launch the example project

The example project is a small demo simple features but with an extensible project design folder system.

You can use this example for every project:
- data integrations
- analysis
- backend
- many others...


If you want to launch the example project, after the cookiecutter download and requirements installation please do:
1. Launch: `poetry install` to install the python libraries and dependencies
2. Launch: `poetry shell` to spawn a new python shell with the new virtualenv created by poetry
3. Launch the script: `./launch.sh` to launch the example

You can use also pip with the requirements.txt file to install the python libraries and dependencies.
If you want to use pip please consider to create a specific `virtualenv` before.

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/JeyDi/Python-Skeleton/issues) for a list of proposed features (and known issues).

If you see something bad or you want to contribute, please open an issue or a pull request.

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please feel free to clone and update the code in this repository


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- [contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username -->