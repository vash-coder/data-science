import sys


def call_center(clients, recipients):
    c_set = set(clients)
    r_set = set(recipients)
    return c_set.difference(r_set)


def potential_clients(clients, participants):
    c_set = set(clients)
    p_set = set(participants)
    return p_set.difference(c_set)


def loyalty_program(clients, participants):
    c_set = set(clients)
    p_set = set(participants)
    return c_set.difference(p_set)


def work_task(task):
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    if task == 'call_center':
        email_set = call_center(clients, recipients)
    elif task == 'potential_clients':
        email_set = potential_clients(clients, participants)
    elif task == 'loyalty_program':
        email_set = loyalty_program(clients, participants)
    else:
        raise Exception('Unknown task')

    return list(email_set)


def main():
    if len(sys.argv) != 2:
        sys.exit(1)
    print(work_task(sys.argv[1]))


if __name__ == '__main__':
    main()