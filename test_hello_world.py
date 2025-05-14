# This code defines a class named Hello
from helloworld import display_message


def test_display_message():
    assert display_message() == "Hello, World!"


def test_wrong_message():
    assert display_message() != ""
