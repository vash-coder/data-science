import timeit


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
                 # list(map(lambda email: email if email.endswith('@gmail.com') else None, emails))
    return gmail_map


def main():
    emails = ['john@gmail.com',
              'james@gmail.com',
              'alice@yahoo.com',
              'anna@live.com',
              'philipp@gmail.com'] * 5

    number = 90_000_000
    time_loop = timeit.timeit(lambda: emails_loop(emails), number=number)
    time_comp = timeit.timeit(lambda: emails_comprehension(emails), number=number)
    time_map = timeit.timeit(lambda: emails_map(emails), number=number)

    results = [
        ("loop", time_loop),
        ("list comprehension", time_comp),
        ("map", time_map)
    ]

    results.sort(key=lambda x: x[1])
    fastest = results[0][0]

    print(f"it is better to use a {fastest}")
    print(" vs ".join(f"{time}" for _, time in results))


if __name__ == '__main__':
    main()