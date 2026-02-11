import sys


def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    input_email = sys.argv[1]

    with open('employees.tsv', 'r') as tsv_file:
        lines  = tsv_file.read().splitlines()

    for line in lines[1:]:
        name, surname, email = line.split('\t')
        if email == input_email:
            print(f"Dear {name}, welcome to our team! We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.")

if __name__ == "__main__":
    main()