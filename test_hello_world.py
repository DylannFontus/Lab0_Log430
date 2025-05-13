# This code defines a class named Hello
from HelloWorld import display_message

def test_display_message():
    assert display_message() == "Hello, World!"

def test_wrong_message():
    assert display_message() != ""