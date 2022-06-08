import re
import os
from argparse import ArgumentParser


def get_title(line: str) -> str:
    if "START" in line:
        return re.search(r'[A-Z]+.(.*)', line).group(1).strip()


def get_result_line(line: str):
    return re.search(r'([A-Z]+):\s+(.*)\s+\(([0-9]+.[0-9]+)', line)


def get_time(line: str) -> float:
    return float(re.search(r'([0-9]+.[0-9]+)', line).group(1))


def get_summary(file):
    summary = {
        'PASS': 0,
        'FAIL': 0,
        'SKIP': 0,
        'time': 0.0,
    }

    for _, line in enumerate(file):
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


def get_failed(file):
    failed = []

    for _, line in enumerate(file):
        res = get_result_line(line)
        if res and 'FAIL' in res.group(1):
            failed.append(res.group(2).strip())

    if failed:
        print('= Failed scenarios:')
        for f in failed:
            print('\t' + f)


def get_skipped(file):
    skipped = {}

    for i, line in enumerate(file):
        res = get_result_line(line)
        if res and 'SKIP' in res.group(1):
            skipped[res.group(2).strip()] = file[i+1].strip()

    if skipped:
        print('= Skipped scenarios:')
        for k, v in skipped.items():
            print('\t' + k + ':\n\t - ' + v)


def process_files(files, full: bool, failed: bool, skipped: bool):
    for i, f in enumerate(files):
        print(f)
        if full:
            print(open(f, "r").read())

        else:
            open_file = open(f, "r").readlines()
            get_summary(open_file)
            if failed:
                get_failed(open_file)
            if skipped:
                get_skipped(open_file)
            print('= For more details go to {}\n'.format(files[i]))


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        help="Report path and filename",
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="directory",
        help="Report directory",
    )
    parser.add_argument(
        "--failed",
        dest="failed",
        help="Print failed scenarios",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--skipped",
        dest="skipped",
        help="Print skipped scenarios",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--full",
        dest="full",
        help="Print the report file",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    files = []

    if args.filename:
        if os.path.isabs(args.filename):
            files.append(args.filename)
        else:
            files.append(os.path.abspath(os.getcwd()) + '/' + args.filename)

    if args.directory:
        for f in os.listdir(os.path.abspath(os.getcwd()) + args.directory):
            files.append(
                os.path.abspath(os.getcwd()) + args.directory + '/' + f
            )

    process_files(files, args.full, args.failed, args.skipped)


if __name__ == "__main__":
    main()
