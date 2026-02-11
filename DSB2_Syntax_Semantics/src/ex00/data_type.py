def data_types():
    type_1 = 1
    type_2 = 'two'
    type_3 = 2.3
    type_4 = False
    type_5 = [5, 6, 7]
    type_6 = {"a": 8, "b": 9}
    type_7 = (10, 11, 12)
    type_8 = {13, 14, 15}

    variants = [type_1, type_2, type_3, type_4, type_5, type_6, type_7, type_8]
    
    types = [type(var).__name__ for var in variants]
    
    print('[' + ', '.join(types) + ']')

if __name__ == '__main__':
    data_types()