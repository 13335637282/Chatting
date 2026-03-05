python -m black .
python -m isort .
pyside6-uic .\add_friends.ui -o .\add_friend.py
pyside6-uic .\search_users.ui -o .\search_users_ui.py