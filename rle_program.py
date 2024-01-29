# file that provides the images
import console_gfx as gfx
ConsoleGfx = gfx.ConsoleGfx

def to_hex_string(data):  # RLE or raw data to hexadecimals
    hex_string = ""
    for value in data:
        hex_value = hex(value)
        hex_string += hex_value[2:]

    return hex_string
def count_runs(flat_data):  # returns 'runs', when the same number is listed repeatedly
    runs = 1
    consecutive = 0
    for i in range(len(flat_data) - 1):
        if flat_data[i] != flat_data[i + 1]:
            runs += 1
        else:
            consecutive += 1
        if consecutive == 15:
            runs += 1
            consecutive = 0
    return runs
def encode_rle(flat_data):  # returns the runs from before but followed by the number in the run
    encoded_data = []
    count = 0
    before_value = flat_data[0]

    for value in flat_data:
        if count == 15:
            encoded_data.append(count)
            encoded_data.append(before_value)
            count = 1
            before_value = value
        elif value == before_value:
            count += 1
        else:
            encoded_data.append(count)
            encoded_data.append(before_value)
            count = 1
            before_value = value

    encoded_data.append(count)
    encoded_data.append(before_value)

    return encoded_data
def decode_rle(rle_data):  # inverse of encode_rle, elongates the encoded rle
    decoded_data = []
    for i in range(len(rle_data)):
        if i % 2 == 0:
            repeat = rle_data[i]
        if i % 2 != 0:
            value = rle_data[i]
            for _ in range(repeat):
                decoded_data.append(value)
    return decoded_data
def string_to_data(data_string):  # converts the string to a list with base 16
    value = [int(hex_char, 16) for hex_char in data_string]
    return value
def to_rle_string(rle_data):  # rle data turns into run length and run value (hexadecimal) with delimiter ':'
    rle_string = ""
    hex_mapping = 'abcdef'

    for i in range(0, len(rle_data), 2):
        rle_string += str(rle_data[i])

        if rle_data[i + 1] >= 10:
            rle_string += hex_mapping[rle_data[i + 1] - 10]
        else:
            rle_string += str(rle_data[i + 1])

        rle_string += ":"

    return rle_string[:-1]
def string_to_rle(rle_string):  # inverse of to_rle_string, turns string rle data back into a list
    rle_data = []
    rle_elements = rle_string.split(':')
    for element in rle_elements:
        rle_data.append(int(element[:-1]))
        rle_data.append(int(element[-1], 16))
    return rle_data

def main():  # menu, with color options shown
    print("Welcome to the RLE image encoder!")
    print("Displaying Spectrum Image:")
    ConsoleGfx.display_image(ConsoleGfx.test_rainbow)

    menu_display = True
    while menu_display:
        print("RLE Menu")
        print("--------")
        print("0. Exit")
        print("1. Load File")
        print("2. Load Test Image")
        print("3. Read RLE String")
        print("4. Read RLE Hex String")
        print("5. Read Data Hex String")
        print("6. Display Image")
        print("7. Display RLE String")
        print("8. Display Hex RLE Data")
        print("9. Display Hex Flat Data\n")

        menu_option = input("Select a Menu Option: ")
        if menu_option == "0":
            menu_display = False
        if menu_option == "1":
            filename = input("Enter name of file to load: ")
            image_data = ConsoleGfx.load_file(filename)
        if menu_option == "2":
            image_data = ConsoleGfx.test_image
            print("Test image data loaded.")
        if menu_option == "3":
            rle_string_input = input("Enter an RLE string to be decoded: ")
            image_data = decode_rle(string_to_rle(rle_string_input))
        if menu_option == "4":
            hex_string_input = input("Enter the hex string holding RLE data: ")
            image_data = decode_rle(string_to_data(hex_string_input))
        if menu_option == "5":
            flat_string_input = input("Enter the hex string holding flat data: ")
            image_data = string_to_data(flat_string_input)
        if menu_option == "6":
            print("Displaying image...")
            ConsoleGfx.display_image(image_data)
        if menu_option == "7":
            print("RLE representation:", to_rle_string(encode_rle(image_data)))
        if menu_option == "8":
            rle_data = encode_rle(image_data)
            print("RLE hex values:", to_hex_string(rle_data))
        if menu_option == "9":
            print("Flat hex values:", to_hex_string(image_data))

if __name__ == "__main__":
    main()

