import os
import pdfplumber
import re


def parse_line(tariff_name, payment_method, line):
    parts = line.split()
    region = f"{parts[0]}"
    i = 1
    while not parts[i].replace('.', '', 1).isdigit() and i < len(parts)-1:
        region += f" {parts[i]}"
        i += 1
    values = parts[i:]
    return f"{tariff_name},{payment_method},{region}," + ",".join(values)


def extract_tariff_lines(tariff_name, pdf_path):
    region_r = re.compile(r"\d\d \w+")
    output_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        payment_method = "DD"
        for page in pdf.pages:
            lines = page.extract_text().split("\n")
            for line in lines:
                if region_r.match(line):
                    output_lines.append(parse_line(tariff_name, payment_method, line))
            payment_method = "CC"
    return output_lines


prefix = "TILs/residential/credit"
for filename in os.listdir(prefix):
    tariff = filename[0:len(filename) - 4]
    # Run the extraction and print the results
    path = prefix + "/" + filename
    for tariff_line in extract_tariff_lines(tariff, path):
        print(tariff_line)

