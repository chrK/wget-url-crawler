#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, csv
import xlsxwriter


def main(argv):
    if len(argv) < 2:
        print("You need to give me a domain to crawl.")
        exit()

    domain_name = argv[1]
    os.system('wget -r %s' % argv[1])

    # Set the directory you want to start from
    root_dir = os.getcwd()
    domain_dir = os.path.join(root_dir, domain_name)

    # Get length of rootDir
    base_path_length = len(os.path.join(root_dir, domain_name))

    raw_url_list = []
    for dir_name, subdir_list, file_list in os.walk(domain_dir):

        remote_path = dir_name[base_path_length:]
        for file_name in file_list:
            # Remove get parameters
            file_name = file_name.split('?')
            raw_url_list.append(os.path.join(remote_path, file_name[0]))

    # Remove duplicates
    raw_url_list = sorted(list(set(raw_url_list)))

    url_list = []
    max_segments = 0
    for raw_url in raw_url_list:
        url = []

        # Just the complete url
        url.append(raw_url)

        # File extension is next
        filename, file_extension = os.path.splitext(raw_url)
        url.append(file_extension)

        # The url segments
        raw_url_segments = raw_url.split('/')

        # Clean empty first segments
        if raw_url_segments[0] == '':
            del raw_url_segments[0]

        segment_count = 1
        for segment in raw_url_segments:
            url.append(segment)
            if segment_count > max_segments:
                max_segments = segment_count
            segment_count += 1

        url_list.append(url)

    # Create CSV
    csv_file_name = os.path.join(root_dir, ('%s_urls.csv' % domain_name))
    with open(csv_file_name, 'wb') as csvfile:
        url_writer = csv.writer(csvfile, delimiter=';')
        for url in url_list:
            url_writer.writerow(url)

    # Create a workbook and add a worksheet.
    xlsx_name = os.path.join(root_dir, ('%s_urls.xlsx' % domain_name))
    workbook = xlsxwriter.Workbook(xlsx_name)
    worksheet = workbook.add_worksheet()

    row = 0
    col = 0

    worksheet.write(row, col,     'URL')
    worksheet.write(row, col + 1, 'File Type')
    worksheet.write(row, col + 2, 'Segments')


    for url in url_list:
        row += 1
        col = 0
        for column in url:
            worksheet.write(row, col, column.decode('utf-8'))
            col += 1

    # Some basic formatting
    worksheet.set_column('A:A', 80)

    # TODO: Convert max_segments to excel column name for max value
    worksheet.autofilter('A1:AA10000')

    workbook.close()

    print('Indexed unique urls: ' + str(len(url_list)))

if __name__ == '__main__':
    sys.exit(main(sys.argv))