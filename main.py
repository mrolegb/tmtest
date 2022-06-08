import re
from argparse import ArgumentParser

info_line = r'([A-Z]+):\s+(.*)\s+\(([0-9]+.[0-9]+)'


def get_title(line: str) -> str:
    if "START" in line:
        return re.search(r'[A-Z]+.(.*)', line).group(1).strip()


def get_result_line(line: str):
    return re.search(r'([A-Z]+):\s+(.*)\s+\(([0-9]+.[0-9]+)', line)


def get_time(line: str) -> float:
    return float(re.search(r'([0-9]+.[0-9]+)', line).group(1))


def get_summary(file):
    summary = {'PASS': 0, 'FAIL': 0, 'SKIP': 0, 'time': 0.0}

    for i, line in enumerate(file):
        if 'title' not in summary:
            summary['title'] = get_title(line)

        res = get_result_line(line)
        if res:
            summary[res.group(1)] += 1
            summary['time'] += float(res.group(3))

    print(
        '= Report summary for "{}"'
        .format(summary['title'])
    )
    print(
        '= Passed: {}, Failed: {}, Skipped: {}, Time spent: {}'
        .format(
            summary['PASS'],
            summary['FAIL'],
            summary['SKIP'],
            summary['time']
        )
    )


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        help="Report path and filename",
        required=True
    )
    parser.add_argument(
        "--full",
        dest="full",
        help="Print the report file",
        action="store_true",
        default=False
    )
    args = parser.parse_args()

    f = open(args.filename, "r")

    if args.full:
        print(f.read())
        return

    get_summary(f)
    print('= For more details go to {}'.format(args.filename))


if __name__ == "__main__":
    main()
