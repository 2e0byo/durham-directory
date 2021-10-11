import requests
from getpass import getpass
from bs4 import BeautifulSoup


class Query:
    def __init__(self, username: str = None, password: str = None, **_):
        self.username = username or input("Username: ")
        self.password = password or getpass("Password: ")

    def __call__(self, oname: str = None, surname: str = None, type_="any", **_):
        """Query durham's directory for email matches for the user in question."""
        if not any((oname, surname)):
            raise ValueError("At least one of oname or surname must be provided.")
        type_ = type_ or "any"
        if type_ not in ["any", "staff", "student"]:
            raise ValueError("type_ must be one of 'any', 'staff', 'student' or unset.")
        args = dict(
            mode="finda",
            ss={"staff": "s", "student": "u", "any": None}[type_],
            on=oname,
            sn=surname,
        )
        URL = "https://www.dur.ac.uk/directory/password"
        resp = requests.get(URL, params=args, auth=(self.username, self.password))

        soup = BeautifulSoup(resp.text, features="lxml")
        results = soup.find("table", id="directoryresults")
        keys, *rows = results.find_all("tr")
        keys = [x.text for x in keys.find_all("th")]
        return [dict(zip(keys, (x.text for x in row.find_all("td")))) for row in rows]


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--surname", help="Surname")
    parser.add_argument("--oname", help="Other name[s] or initial[s]")
    parser.add_argument("--user", dest="username", help="Username for login.")
    parser.add_argument("--password", help="Password for login.")
    parser.add_argument(
        "--type", dest="type_", help="Student, Staff or Any (default is any)"
    )
    args = parser.parse_args()
    query = Query(**args.__dict__)
    resp = query(**args.__dict__)
    if resp:
        widths = {"Name": 25, "Department": 30, "Job/Role": 40, "Telephone": 8}
        headers = resp[0].keys()
        print(" ".join(f"{k:<{widths.get(k, 30)}}" for k in headers))
        print("-" * sum(widths.values()), end="")
        print("-" * 30 * (len(headers) - len(widths)), end="")
        print("-" * len(headers))

        for row in resp:
            for k, v in row.items():
                width = widths.get(k, 30)
                print(f"{v[:width]:<{width}} ", end="")
            print()
    else:
        print("No results found...")
