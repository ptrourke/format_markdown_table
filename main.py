import argparse
import re

header_alignment_pattern = re.compile(r'^[|:-]+$')
left_alignment_pattern = re.compile(r':-+$')
right_alignment_pattern = re.compile(r'-+:$')
center_alignment_pattern = re.compile(r':-+:$')


def make_header(row):
    table_header = {}
    row = row.strip().strip("|")
    row_values = row.split("|")
    for row_value in row_values:
        table_header[row_value] = {
            "length": len(row_value),
            "alignment": "left"
        }
    return table_header


def get_column_name(table_header, column_num):
    column_names = list(table_header)
    column_name = column_names[column_num]
    return column_name


def get_column_length(table_header, column_name):
    return table_header[column_name]["length"]


def update_column_length(table_header, column_name, value):
    table_header[column_name]["length"] = value
    return table_header


def make_table_row(row, table_header):
    row_columns = []
    row_values = row.strip("|").split("|")
    for column_num, column in enumerate(row_values):
        column_name = get_column_name(table_header, column_num)
        if len(column) > get_column_length(table_header, column_name):
            table_header = update_column_length(table_header, column_name, len(column))
        row_columns.append(column)
    return row_columns, table_header


def make_header_alignment(row, table_header):
    row_values = row.strip("|").split("|")
    for column_num, column in enumerate(row_values):
        column_name = get_column_name(table_header, column_num)
        if left_alignment_pattern.match(column):
            table_header[column_name]["alignment"] = "left"
        elif right_alignment_pattern.match(column):
            table_header[column_name]["alignment"] = "right"
        elif center_alignment_pattern.match(column):
            table_header[column_name]["alignment"] = "center"
        else:
            table_header[column_name]["alignment"] = "left"
    return table_header


def get_column_details(table_header, column_num=None, column_name=None):
    if not column_name:
        if not isinstance(column_num, int):
            raise Exception("Must have column name or column number!")
        column_name = get_column_name(table_header, column_num)
    column_details = table_header[column_name]
    return column_details["length"], column_details["alignment"]


def output_row(next_row, table_header):
    output_row_list = []
    column_count_table = len(list(table_header.keys()))
    column_count_row = len(next_row)
    for column_num, column in enumerate(next_row):
        length, alignment = get_column_details(
            table_header,
            column_num
        )
        if alignment == "right":
            column_value = f' {column:>{length}} '
        elif alignment == "center":
            column_value = f' {column:^{length}} '
        else:
            column_value = f' {column:<{length}} '
        output_row_list.append(column_value)
    if column_count_row < column_count_table:
        for column_num in range(column_count_row, column_count_table):
            length, alignment = get_column_details(
                table_header,
                column_num
            )
            column = ""
            if alignment == "right":
                column_value = f' {column:>{length}} '
            elif alignment == "center":
                column_value = f' {column:^{length}} '
            else:
                column_value = f' {column:<{length}} '
            output_row_list.append(column_value)
    output_row = "|".join(output_row_list)
    output_row = f"| {output_row} |"
    return output_row


def output_header_lines(table_header):
    output_line_list = []
    for key in list(table_header):
        length, alignment = get_column_details(
            table_header,
            column_name=key
        )
        column_output = "-" * (length+2)
        if alignment in ["center", "right"]:
            column_output = column_output[:-1] + ":"
        if alignment == "center":
            column_output = column_output[1:] + ":"
        output_line_list.append(column_output)
    output_line = "|".join(output_line_list)
    output_line = f"| {output_line} |"
    return output_line


def parse_table(table_input):
    header_rows = []
    table_output_list = []
    table_header = {}
    if isinstance(table_input, list):
        table_input = "\n".join(table_input)
    table_input = table_input.splitlines()
    row_count = len(table_input)
    for row_num, row in enumerate(table_input):
        if row_num == 0:
            table_header = make_header(row)
            continue
        if header_alignment_pattern.match(row):
            header_rows.append(row_num)
            table_header = make_header_alignment(row, table_header)
            continue
        row_output, table_header = make_table_row(
            row,
            table_header
        )
        table_output_list.append(row_output)
    return table_output_list, table_header, header_rows, row_count


def build_table(row_output, table_header, header_rows, row_count):
    table_output = []
    for row_num in range(row_count):
        if row_num in header_rows:
            table_output.append(output_header_lines(table_header))
        elif row_num == 0:
            next_row = list(table_header.keys())
            table_output.append(output_row(next_row, table_header))
        else:
            next_row = row_output.pop(0)
            table_output.append(output_row(next_row, table_header))
    return table_output


def print_table(table_output):
    for table_row in table_output:
        print(table_row)

def main(args):
    table_input = args.table
    table_output_list, table_header, header_rows, row_count = parse_table(
        table_input
    )
    table_output_list = build_table(
        table_output_list,
        table_header,
        header_rows,
        row_count
    )
    print_table(table_output_list)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("table", nargs="*")
    args = argument_parser.parse_args()
    if not args:
        argument_parser.print_help()
    else:
        main(args)
