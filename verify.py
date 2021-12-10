from pathlib import Path
from csv import DictReader, DictWriter
from durham_directory import QueryOne, QueryError
from argparse import ArgumentParser


def robust_query(name, surname):
    try:
        return query(oname=name, surname=surname)
    except QueryError:
        try:
            res = query(surname=surname)
            if res:
                return res
        except QueryError:
            pass
        return query(oname=name)


def verify(record):
    print("Verifying", record["Name"], record["Surname"])
    try:
        email = robust_query(record["Name"], record["Surname"])["Email"]
        if email != record["Email"]:
            record["new_email"] = email
    except QueryError as e:
        print("Unable to match:", e)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("CSVFILE", type=Path, help="CSV of records.")
    parser.add_argument("--out", type=Path, help="Outfile (optional).")
    args = parser.parse_args()
    with args.CSVFILE.open() as f:
        data = list(DictReader(f))
    query = QueryOne()

    for record in data:
        verify(record)

    for record in data:
        if record.get("new_email"):
            print(
                f"Incorrect email for {record['Name']} {record['Surname']}"
                f"corrected from {record['Email']} to {record['new_email']}"
            )
    if args.out:
        with args.out.open("w") as f:
            writer = DictWriter(f, fieldnames=data[0].keys())
            for record in data:
                record["Email"] = record.get("new_email", record["Email"])
                try:
                    del record["new_email"]
                except KeyError:
                    pass
            writer.writerow(record)
