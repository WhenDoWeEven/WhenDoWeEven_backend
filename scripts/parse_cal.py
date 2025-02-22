import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python parse_cal.py <filename>")
        return

    filename = sys.argv[1]
    print(f"The file name passed as argument is: {filename}")

if __name__ == "__main__":
    main()