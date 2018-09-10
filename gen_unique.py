import sys

def main():
    target = sys.argv[1]
    with open(target, 'r') as f:
        res = list(set(f.readlines()))
        with open('unique.txt', 'w') as fout:
            fout.write(''.join(res))

if __name__ == '__main__':
    main()