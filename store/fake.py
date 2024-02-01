"""
    Module name :- fake
"""

import random
from datetime import date, timedelta


class Fake:
    """
    Fake class.
    """

    alphabets = [
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
    ]

    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

    def create_emails(self):
        """
        Create random emails.
        """
        emails = set()

        while len(emails) < 50000:
            email = "".join(random.choices(self.alphabets, k=6)) + "@gmail.com"
            emails.add(email)

        return emails

    def create_names(self):
        """
        Create random names.
        """
        return ["".join(random.choices(self.alphabets, k=10)) for _ in range(50000)]

    def create_phone_numbers(self):
        """
        Create random phone numbers.
        """
        return ["".join(random.choices(self.numbers, k=10)) for _ in range(50000)]

    def create_addresses(self):
        """
        Create random addresses.
        """
        return ["".join(random.choices(self.alphabets, k=50)) for _ in range(50000)]

    def create_websites(self):
        """
        Create random websites.
        """
        return [
            "".join(random.choices(self.alphabets, k=8)) + ".com" for _ in range(50000)
        ]

    def create_titles(self):
        """
        Create random titles.
        """
        return ["".join(random.choices(self.alphabets, k=20)) for _ in range(50000)]

    def create_dates(self):
        """
        Create random dates.
        """
        return [date.today() - timedelta(days=x) for x in range(200)]

    def create_usernames(self):
        """
        Create random usernames.
        """
        usernames = set()

        while len(usernames) < 50000:
            username = "".join(random.choices(self.alphabets, k=6)) + "".join(
                random.choices(self.numbers, k=3)
            )
            usernames.add(username)

        return usernames
