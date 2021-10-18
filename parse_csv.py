import csv
from pathlib import Path


def process_durham_csv(fn: Path):
    """Process CSV from durham timetabling.

    Expects first row to be header, seminar to be in activity column.

    Prints orgtbl output.
    """
    students = {}

    with fn.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            students[row["Student"]] = dict(
                email=row["Email"], seminar=row["Activity"].split("/")[-1].strip()
            )

    def orgtbl_out(name, email, header=False):
        print(f"|{name:<40}|{email:<40}|")
        if header:
            print("|", "-" * 40, "+", "-" * 40, "|", sep="")

    for sem in set(x["seminar"] for x in students.values()):
        print("*** Seminar", sem, "\n")
        orgtbl_out("Name", "Email", True)
        records = ((k, v["email"]) for k, v in students.items() if v["seminar"] == sem)
        for name, email in records:
            orgtbl_out(name, email)

        print("\n")


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("IN", type=Path)
    args = parser.parse_args()
    process_durham_csv(args.IN)
