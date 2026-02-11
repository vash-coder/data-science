def main():
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]

    dictionary = {}
    for key, value in list_of_tuples:
        dictionary.setdefault(key, []).append(value)

    sorted_dictionary = sorted(dictionary.items(), key=lambda x: (-int(x[1][0]), x[0]))
    for key, value in sorted_dictionary:
        print(key)

if __name__ == '__main__':
    main()