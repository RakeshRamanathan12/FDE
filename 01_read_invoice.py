import csv

total = 0
above_100000 = 0
invalid = 0

with open("homework_invoices.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        total += 1

        vendor = row["vendor"]
        amount = row["amount"]
        status = row["status"]


        try:
            amount = float(amount)
            if vendor != "":
                print(f"{vendor:<20}: {amount:,.2f}" + " --> " + status)

            if amount > 100000:
                above_100000 += 1

        except ValueError:
            invalid += 1
         

print("Total invoices:", total)
print("Amount greater than 100000:", above_100000)
print("Invalid amounts:", invalid)