"""
Tests for the attendance module.

"""


from src import attendance as a


def execute_all():
    """
    Executes all tests for the attendance module.
    :return: None
    """

    print("")
    print("------------------ ATTENDANCE TESTS -------------------")
    print("")

    test_excuse_type()


def test_excuse_type():
    """
    Verifies that when the user enters Late/Absent in the first slot,
    or omits the word or puts in something wrong, that it is handled correctly.
    :return: None
    """

    print("")
    print("test_excuse_type: Testing excuse types...")

    # TODO

    print("PASS")
