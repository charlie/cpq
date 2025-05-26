import csv
from decimal import Decimal
import re

def tariff_tier(name):
    if name in ["Double Gold", "EV - Double Gold"] or name.startswith("UW Fixed Saver"):
        return 3
    elif name in ["Gold", "EV - Gold"] or name.startswith("UW Fixed"):
        return 2
    elif name in ["Value", "EV - Value"]:
        return 1
    else:
        raise Exception(f"Unable to determine tariff tier for {name}")


def tariff_family(name):
    if name in ["Value", "Gold", "Double Gold"]:
        return "Variable"
    elif name.startswith("EV -"):
        return "EV"
    elif name.startswith("UW Fixed"):
        return "Fixed"
    else:
        raise Exception(f"Unable to determine tariff family for {name}")


def tariff_name_sortable(name):
    # todo this sorting "solution" will break when we reach UW Fixed 100
    single_digit_fixed_r = [re.compile(r"^(UW Fixed )(\d)$"), re.compile(r"^(UW Fixed Saver )(\d)$")]
    if name in ["Value", "Gold", "Double Gold"] or name.startswith("EV -"):
        return name
    for rx in single_digit_fixed_r:
        match = rx.match(name)
        if match is not None:
            return f"{match.group(1)} 0{match.group(2)}"
    return name

staff_discount = Decimal("0.9")
shareholder_discount = Decimal("0.95")

with (open("tariffs.csv") as csvfile):
    reader = csv.reader(csvfile)
    for row in reader:
        family = tariff_family(row[0])
        tier = tariff_tier(row[0])
        name = tariff_name_sortable(row[0])
        if row[0][0:2] == "EV":
            peak_rate = Decimal(row[4])
            off_peak_rate = Decimal(row[5])
            staff_unit_rates = f"{peak_rate * staff_discount}|{off_peak_rate * staff_discount}"
            shareholder_unit_rates = f"{peak_rate * shareholder_discount}|{off_peak_rate * shareholder_discount}"
            print(f"{family},{tier},{name},{row[1]},{row[2]},standard,e7,{row[3]},{peak_rate}|{off_peak_rate}")
            print(f"{family},{tier},{name},{row[1]},{row[2]},staff,e7,{row[3]},{staff_unit_rates}")
            print(f"{family},{tier},{name},{row[1]},{row[2]},shareholder,e7,{row[3]},{shareholder_unit_rates}")
        else:
            gd_rate = Decimal(row[6])
            peak_rate = Decimal(row[8])
            off_peak_rate = Decimal(row[8])
            staff_gd_unit_rate = gd_rate * staff_discount
            staff_e7_unit_rates = f"{peak_rate * staff_discount}|{off_peak_rate * staff_discount}"
            shareholder_gd_unit_rate = gd_rate * shareholder_discount
            shareholder_e7_unit_rates = f"{peak_rate * shareholder_discount}|{off_peak_rate * shareholder_discount}"
            print(f"{family},{tier},{name},{row[1]},{row[2]},standard,gd,{row[5]},{row[6]}")
            print(f"{family},{tier},{name},{row[1]},{row[2]},standard,e7,{row[7]},{row[8]}|{row[9]}")
            print(f"{family},{tier},{name},{row[1]},{row[2]},staff,gd,{row[5]},{staff_gd_unit_rate}")
            print(f"{family},{tier},{name},{row[1]},{row[2]},staff,e7,{row[7]},{staff_e7_unit_rates}")
            print(f"{family},{tier},{name},{row[1]},{row[2]},shareholder,gd,{row[5]},{shareholder_gd_unit_rate}")
            print(f"{family},{tier},{name},{row[1]},{row[2]},shareholder,e7,{row[7]},{shareholder_e7_unit_rates}")
