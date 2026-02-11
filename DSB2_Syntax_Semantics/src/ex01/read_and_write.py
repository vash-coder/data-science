def csv_to_tsv():
    input_file = "../../datasets/ds.csv"
    output_file = "ds.tsv"

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            outfile.write(line.replace('","', '"\t"'))

if __name__ == '__main__':
    csv_to_tsv()