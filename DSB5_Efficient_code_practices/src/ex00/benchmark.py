import timeit


def emails_loop(emails):
    gmail_list = []
    for email in emails:
        if email.endswith('@gmail.com'):
            gmail_list.append(email)
    return gmail_list


def emails_comprehension(emails):
    return [email for email in emails if email.endswith('@gmail.com')]


def main():
    emails = ['john@gmail.com',
              'james@gmail.com',
              'alice@yahoo.com',
              'anna@live.com',
              'philipp@gmail.com'] * 5

    number = 90_000_000
    time_loop = timeit.timeit(lambda: emails_loop(emails), number=number)
    time_comp = timeit.timeit(lambda: emails_comprehension(emails), number=number)

    if time_loop >= time_comp:
        print('It is better to use a list comprehension')
        print(f"{time_comp} vs {time_loop}")
    else:
        print('It is better to use a loop')
        print(f"{time_loop} vs {time_comp}")


if __name__ == '__main__':
    main()