import pytest


'''
Test 1:
Testing that all usernames sent to database will be
successfully converted to lowercase so that each one
is unique. e.g. "JasoN21" will be the same as "jason21"
'''


def test_username():
    username = "JeSsE"
    assert username.lower() == "jesse"


'''
Test 2:
Testing that the cooking and preparation times that were
submitted as strings to the database, can be successfully
converted back to integers to display the total on the
card reveals on the "All Recipes" page
'''


def test_total_time():
    prep_time = "2"
    cooking_time = "15"
    total_time = int(prep_time) + int(cooking_time)
    assert total_time == 17


'''
Test 3:
Testing that the app iterates through the recipe_method
list which was inputted by the user on the new_recipe form.
This iteration will store the data as an object so that the
key-value pairs can be unpacked on the `Full Recipe` page.
'''


def test_recipe_method_iteration():
    method_obj = {}
    method = ["First step", "Second step", "Third step"]
    for element in method:
        method_step = method.index(element) + 1
        method_obj[str(method_step)] = str(element)
    assert method_obj == {
        "1": "First step",
        "2": "Second step",
        "3": "Third step"
        }
