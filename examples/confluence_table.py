from pytablewriter import ConfluenceWikiTableWriter


def main() -> None:
    writer = ConfluenceWikiTableWriter(
        headers=["Name", "Count", "Notes"],
        value_matrix=[["Alice", 2, "a|b"], ["雪", 3, "first\nsecond"]],
    )
    writer.write_table()


if __name__ == "__main__":
    main()
