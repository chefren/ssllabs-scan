from __future__ import print_function
import csv
import sys

from ssllabsscan.report_template import REPORT_HTML
from ssllabsscan.ssllabs_client import SSLLabsClient, SUMMARY_COL_NAMES


SUMMARY_CSV = "summary.csv"
SUMMARY_HTML = "summary.html"
VAR_TITLE = "{{VAR_TITLE}}"
VAR_DATA = "{{VAR_DATA}}"
DEFAULT_TITLE = "SSL Labs Analysis Summary Report"


def output_summary_html(input_csv, output_html):
    print("Creating {} ...".format(output_html))

    data = ""
    with open(input_csv, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row[0].startswith("#"):
                data += "<tr><th>{}</th></tr>".format('</th><th>'.join(row))
            else:
                data += '<tr class="{}"><td>{}</td></tr>'.format(row[1][:1], '</td><td>'.join(row))

    # Replace the target string
    content = REPORT_HTML
    content = content.replace(VAR_TITLE, DEFAULT_TITLE)
    content = content.replace(VAR_DATA, data)

    # Write the file out again
    with open(output_html, 'w') as file:
        file.write(content)


def process(
        server_list_file, check_progress_interval_secs=30,
        summary_csv=SUMMARY_CSV, summary_html=SUMMARY_HTML
):
    ret = 0
    # read from input file
    with open(server_list_file) as f:
        content = f.readlines()
    servers = [x.strip() for x in content]

    with open(SUMMARY_CSV, 'w') as outfile:
        # write column names to file
        outfile.write("#{}\n".format(",".join(str(s) for s in SUMMARY_COL_NAMES)))

    for server in servers:
        try:
            print("Start analyzing {} ...".format(server))
            SSLLabsClient(check_progress_interval_secs).analyze(server, summary_csv)
        except Exception as e:
            print(e)
            ret = 1

    output_summary_html(summary_csv, summary_html)
    return ret


def main():
    """
    Entry point of the app.
    """
    if len(sys.argv) != 2:
        print("{} [SERVER_LIST_FILE]".format(sys.argv[0]))
        return 1
    return process(server_list_file=sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
