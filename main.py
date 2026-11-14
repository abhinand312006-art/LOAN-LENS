
# ==========================================
#              LOANLENS
#       EMI AND LOAN COMPARISON SYSTEM
# ==========================================

# Function to accept a valid positive number
def get_positive_number(message):
    while True:
        try:
            value = float(input(message))

            if value <= 0:
                print("Please enter a number greater than zero.")
            else:
                return value

        except ValueError:
            print("Invalid input! Please enter a number.")


# Function to accept a valid interest rate
def get_interest_rate(message):
    while True:
        try:
            rate = float(input(message))

            if rate < 0 or rate > 50:
                print("Interest rate must be between 0 and 50.")
            else:
                return rate

        except ValueError:
            print("Invalid input! Enter a valid interest rate.")


# Function to accept a positive whole number
def get_positive_integer(message):
    while True:
        try:
            value = int(input(message))

            if value <= 0:
                print("Enter a number greater than zero.")
            else:
                return value

        except ValueError:
            print("Please enter a valid whole number.")


# ==========================================
#             EMI CALCULATOR
# ==========================================

def calculate_emi(P, R, N):

    if R == 0:
        return round(P / N, 2)

    emi = (P * R * (1 + R) ** N) / ((1 + R) ** N - 1)

    return round(emi, 2)


# ==========================================
#          AMORTISATION SCHEDULE
# ==========================================

def generate_schedule(P, annual_rate, N):

    R = annual_rate / (12 * 100)

    emi = calculate_emi(P, R, N)

    balance = round(P, 2)
    total_interest = 0
    schedule = []

    for month in range(1, N + 1):

        if balance <= 0:
            break

        interest = round(balance * R, 2)

        actual_emi = min(emi, round(balance + interest, 2))

        principal = round(actual_emi - interest, 2)

        if principal > balance:
            principal = balance

        balance = round(balance - principal, 2)

        total_interest += interest

        schedule.append([
            month,
            actual_emi,
            interest,
            principal,
            balance
        ])

    total_interest = round(total_interest, 2)

    return emi, schedule, total_interest


# Function to display amortisation schedule
def display_schedule(schedule):

    print("\nAMORTISATION SCHEDULE")
    print("-" * 75)

    print(
        f"{'Month':<10}"
        f"{'EMI':<13}"
        f"{'Interest':<13}"
        f"{'Principal':<13}"
        f"{'Balance':<13}"
    )

    print("-" * 75)

    for row in schedule:

        print(
            f"{row[0]:<10}"
            f"{row[1]:<13.2f}"
            f"{row[2]:<13.2f}"
            f"{row[3]:<13.2f}"
            f"{row[4]:<13.2f}"
        )

    print("-" * 75)


# ==========================================
#             EMI CALCULATOR MENU
# ==========================================

def emi_calculator():

    print("\nENTER LOAN DETAILS")

    P = get_positive_number("Enter loan amount: Rs. ")

    rate = get_interest_rate("Enter annual interest rate (%): ")

    N = get_positive_integer("Enter loan tenure in months: ")

    emi, schedule, total_interest = generate_schedule(P, rate, N)

    print("\nLOAN SUMMARY")
    print("-" * 40)

    print("Loan Amount: Rs.", round(P, 2))
    print("Annual Interest Rate:", rate, "%")
    print("Loan Tenure:", N, "months")
    print("Monthly EMI: Rs.", emi)
    print("Total Interest: Rs.", total_interest)
    print("Total Repayment: Rs.", round(P + total_interest, 2))

    display_schedule(schedule)


# ==========================================
#          LOAN COMPARISON ENGINE
# ==========================================

def compare_loans():

    print("\nLOAN COMPARISON")

    P = get_positive_number("Enter loan amount: Rs. ")

    N = get_positive_integer("Enter loan tenure in months: ")

    number_of_banks = get_positive_integer(
        "Enter number of bank offers (2 or 3): "
    )

    while number_of_banks > 3:
        print("You can compare a maximum of 3 banks.")
        number_of_banks = get_positive_integer(
            "Enter number of bank offers (2 or 3): "
        )

    offers = []

    for i in range(number_of_banks):

        print("\nBANK", i + 1)

        bank_name = input("Enter bank name: ").strip()

        if bank_name == "":
            bank_name = "Bank " + str(i + 1)

        rate = get_interest_rate("Enter annual interest rate (%): ")

        emi, schedule, total_interest = generate_schedule(P, rate, N)

        offers.append([
            bank_name,
            rate,
            emi,
            total_interest
        ])

    print("\nCOMPARISON RESULTS")
    print("-" * 65)

    for offer in offers:

        print("\nBank:", offer[0])
        print("Interest Rate:", offer[1], "%")
        print("Monthly EMI: Rs.", offer[2])
        print("Total Interest: Rs.", offer[3])

    best_offer = min(offers, key=lambda offer: offer[3])

    print("\nBEST LOAN OFFER")
    print("-" * 40)

    print("Bank Name:", best_offer[0])
    print("Interest Rate:", best_offer[1], "%")
    print("Lowest Total Interest: Rs.", best_offer[3])


# ==========================================
#             PREPAYMENT FEATURE
# ==========================================

def prepayment_calculator():

    print("\nONE-TIME LOAN PREPAYMENT")

    P = get_positive_number("Enter loan amount: Rs. ")

    rate = get_interest_rate("Enter annual interest rate (%): ")

    N = get_positive_integer("Enter loan tenure in months: ")

    emi, original_schedule, original_interest = generate_schedule(
        P, rate, N
    )

    print("\nYour original monthly EMI is Rs.", emi)

    print("\nOriginal loan tenure:", len(original_schedule), "months")

    print("\nWhen will you make the prepayment?")

    prepayment_month = get_positive_integer(
        "Enter the month number after which you will prepay: "
    )

    if prepayment_month >= len(original_schedule):
        print("Invalid month! Choose a month before the loan ends.")
        return

    outstanding_balance = original_schedule[prepayment_month - 1][4]

    print("Outstanding balance after this month: Rs.", outstanding_balance)

    prepayment = get_positive_number(
        "Enter one-time prepayment amount: Rs. "
    )

    if prepayment > outstanding_balance:
        print("Prepayment cannot exceed the outstanding balance.")
        return

    # Apply the prepayment after the selected EMI

    balance = outstanding_balance - prepayment

    total_interest = sum(
        row[2] for row in original_schedule[:prepayment_month]
    )

    month = prepayment_month

    print("\nPREPAYMENT SCHEDULE")
    print("-" * 60)

    print("Month\tInterest\tPrepayment\tBalance")

    print(
        prepayment_month,
        "\t",
        original_schedule[prepayment_month - 1][2],
        "\t",
        round(prepayment, 2),
        "\t",
        round(balance, 2)
    )

    while balance > 0:

        month += 1

        interest = round(balance * (rate / (12 * 100)), 2)

        actual_emi = min(emi, round(balance + interest, 2))

        principal = round(actual_emi - interest, 2)

        if principal > balance:
            principal = balance

        balance = round(balance - principal, 2)

        total_interest += interest

        print(
            month,
            "\t",
            interest,
            "\t",
            0,
            "\t",
            balance
        )

    total_interest = round(total_interest, 2)

    print("-" * 60)

    print("\nPREPAYMENT SUMMARY")

    print("Original Loan Tenure:", len(original_schedule), "months")

    print("New Loan Tenure:", month, "months")

    print("Months Saved:", len(original_schedule) - month)

    print("Original Total Interest: Rs.", original_interest)

    print("Interest After Prepayment: Rs.", total_interest)

    print(
        "Interest Saved: Rs.",
        round(original_interest - total_interest, 2)
    )


# ==========================================
#                 MAIN MENU
# ==========================================

def main():

    while True:

        print("\n====================================")
        print("          WELCOME TO LOANLENS")
        print("      EMI AND COMPARISON SYSTEM")
        print("====================================")

        print("1. Calculate EMI and View Schedule")
        print("2. Compare Bank Loan Offers")
        print("3. Calculate One-Time Prepayment")
        print("4. Exit")

        print("====================================")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":

            emi_calculator()

        elif choice == "2":

            compare_loans()

        elif choice == "3":

            prepayment_calculator()

        elif choice == "4":

            print("\nThank you for using LoanLens!")
            break

        else:

            print("Invalid choice! Please select between 1 and 4.")


# Start the application

main()
