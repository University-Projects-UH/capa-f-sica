
def read_file(filename):
    return open(filename, 'r'); #Read script.txt

script_file = read_file('script.txt');
lines_array = script_file.read().split('\n');

for line in lines_array:
    print(line);
