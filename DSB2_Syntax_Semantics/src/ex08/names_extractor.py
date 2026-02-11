import sys

def get_name(email: str):
    name, rest = email.split('.', 1)
    surname = rest.split('@')[0]
    return name.capitalize(), surname.capitalize()

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, 'r') as file:
        emails = file.read().splitlines()

    with open('employees.tsv', 'w') as tsv_file:
        tsv_file.write("Name\tSurname\tE-mail\n")
        for email in emails:
            if not email.strip():
                continue
            name, surname = get_name(email)
            tsv_file.write(f"{name}\t{surname}\t{email}\n")

if __name__ == "__main__":
    main()
