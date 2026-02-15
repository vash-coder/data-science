import timeit
import sys


def emails_loop(emails):
    gmail_list = []
    for email in emails:
        if email.endswith('@gmail.com'):
            gmail_list.append(email)
    return gmail_list


def emails_comprehension(emails):
    return [email for email in emails if email.endswith('@gmail.com')]


def emails_map(emails):
    gmail_map = [email
                 for email in map(lambda email: email if email.endswith('@gmail.com') else None, emails)
                 if email is not None]
    return gmail_map


def emails_filter(emails):
    return [filter(lambda email: email.endswith('@gmail.com'), emails)]


FUNCTIONS = {
    'loop': emails_loop,
    'list_comprehension': emails_comprehension,
    'map': emails_map,
    'filter': emails_filter,
}


EMAILS = ['john@gmail.com',
          'james@gmail.com',
          'alice@yahoo.com',
          'anna@live.com',
          'philipp@gmail.com'] * 5


def main():
    if len(sys.argv) != 3:
        raise Exception("Incorrect number of arguments")

    function_name = sys.argv[1]
    try:
        number = int(sys.argv[2])
    except ValueError:
        raise Exception("Incorrect number of arguments")

    if function_name not in FUNCTIONS:
        raise Exception(f"Function {function_name} does not exist")

    function = FUNCTIONS[function_name]

    time = timeit.timeit(lambda: function(EMAILS), number=number)
    print(time)


if __name__ == '__main__':
    main()