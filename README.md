# Moriarty
Automatic test solver that does not require an Internet connection. Graphical interface is available

[![Python Version](https://img.shields.io/badge/python-3.9%2B-brightgreen?logo=python)](https://www.python.org/)
![version](https://img.shields.io/badge/version-1.0-green)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


# 🚀Quick Start
Go to [release page](https://github.com/FatalX2080/Moriarty/releases) and download last stable release (apk/source). Enjoy using it;)

# 🖥️Instalation 
### Poertry 
```
git clone https://github.com/FatalX2080/Moriarty.git
poetry shell
poetry install
cd src
flet run main.py
```
### Pypi
```
git clone https://github.com/FatalX2080/Moriarty.git
python3 -m venv .venv
source /.venv/bin/activate
pip install requirements.txt
cd src
python3 main.py
``` 
# 🌴 Project Tree
```
Moriarty
├── LICENSE
├── pyproject.toml
├── README.md
├── requirements.txt
└── src
    ├── assets
    │   ├── icon.png
    │   └── splash_android.png
    ├── config.py
    ├── gui
    │   ├── descriptions.py
    │   ├── factory.py
    │   ├── __init__.py
    │   ├── navigate.py
    │   ├── pages
    │   │   ├── base.py
    │   │   ├── page0.py
    │   │   ├── page10.py
    │   │   ├── page11.py
    │   │   ├── page12.py
    │   │   ├── page1.py
    │   │   ├── page2.py
    │   │   ├── page3.py
    │   │   ├── page4.py
    │   │   ├── page5.py
    │   │   ├── page6.py
    │   │   ├── page7.py
    │   │   ├── page8.py
    │   │   └── page9.py
    │   └── ui.py
    ├── __init__.py
    ├── main.py
    └── tests
        ├── __init__.py
        ├── test10.py
        ├── test11.py
        ├── test12.py
        ├── test1.py
        ├── test2.py
        ├── test3.py
        ├── test4.py
        ├── test5.py
        ├── test6.py
        ├── test7.py
        ├── test8.py
        ├── test9.py
        └── test.py
```

# 🌟 Features
| Feature          | Status  | Notes                        |
|------------------|:-------:|------------------------------|
| Test 5 (_v1_)    | ❄️      | Difficult / unrealizable     |
| Test 5 (_v2_)    | ✅      | Based on test 4              |
| Test 6           | ✅      |Use test 5 v2 as core         |
| Cross-platform   | ✅      | Flet (GUI)                   |

# 📆 Roadmap
* ~~[1st release](https://github.com/FatalX2080/Moriarty/releases/tag/v1.0) release~~
* ~~Сreating a base class of checks~~
* Responsive design according to the theme
* Unit tests for solving problems
* Facilitate existing tests
* Debugging found errors
* Archiving

# ❓ FAQ
* Q: How much does it cost? A: It is absolutely free
* Q: Is there any way I can help the project? A: Sure, you can fork it, when modification will be done, make new pull request
* Q: Is there a guarantee that the answers are correct? A: NO! You mustn't let your guard down.
* Q: How many tests have already been completed? A: 12/13
* Q: A white screen with text popped up abruptly. A: The engine is written in python, so it's almost normal. You have entered data that the program could not process.
* Q: Can I build the app myself? A: Of course, study the flet [documentation](https://flet.dev/docs/publish/) for this.
* Q: ios? A: no
Automatic test solver that does not require an Internet connection. Graphical interface is available