import os
import string

import cv2
import numpy as np


def calculate_black_percentage(input_image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    # Threshold image to get rid of gray from antialiasing
    ret, gray_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
    # Count black pixels (0 intensity)
    black_pixels = np.sum(gray_image == 0)

    black_percentage = black_pixels / 641 * 100

    return black_percentage


def create_font_mappings():
    # Define image properties
    font_scale = 2
    thickness = 2
    text_color = (0, 0, 0)  # Black color
    # Define character set
    characters = list(string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation + ' ')
    # Create a dictionary to store results
    char_black_perc = {}
    # Loop through characters and calculate black percentage
    for char in characters:
        # Create a blank black image
        image_width = 300
        image_height = 300
        my_image = np.zeros((image_height, image_width, 3), np.uint8)
        my_image.fill(255)

        # Get font size for positioning
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size, _ = cv2.getTextSize(char, font, font_scale, thickness)

        # Calculate starting position for centered text
        text_x = int((image_width - text_size[0]) / 2)
        text_y = int((image_height + text_size[1]) / 2)

        # Draw the character on the image
        cv2.putText(my_image, char, (text_x, text_y), font, font_scale, text_color, thickness)

        # Calculate black pixel percentage
        black_perc = calculate_black_percentage(my_image)

        # Store result in dictionary
        char_black_perc[char] = black_perc
    # Sort the dictionary by value (ascending order)
    sorted_char_black_perc = dict(sorted(char_black_perc.items(), key=lambda item: item[1]))
    return sorted_char_black_perc


def process_image(path_to_image, target_width):
    """
  Loads an image, converts it to grayscale, and resizes it to a target width
  while preserving aspect ratio.

  Args:
      path_to_image: Path to the image file.
      target_width: Desired width of the resized image.

  Returns:
      A grayscale resized version of the image as a NumPy array.
  """
    if not is_valid_image_path(path_to_image):
        print("Invalid path!")
        return
    # Read the image in grayscale mode (0 for grayscale)
    image_to_resize = cv2.imread(path_to_image, 0)

    # Check if image read successfully
    if image_to_resize is None:
        print("Error: Could not read image from", path_to_image)
        return None

    # Get original image dimensions
    height, width = image_to_resize.shape[:2]

    # Calculate new height to maintain aspect ratio
    new_height = int(height * (target_width / width))

    # Resize the image
    resized_image = cv2.resize(image_to_resize, (target_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_image


def is_valid_image_path(path_to_image):
    """
  Checks if the provided path points to a valid image file on the filesystem.

  Args:
      path_to_image: The path to the image file.

  Returns:
      True if the path exists as a file, False otherwise.
  """

    return os.path.isfile(path_to_image)


# Example usage
image_path = "path/to/your/image.jpg"

if is_valid_image_path(image_path):
    print("Image path is valid")
else:
    print("Image path is not valid or does not exist")


def calculate_darkness(intensity):
    """
  Calculates darkness percentage for a pixel intensity value.

  Args:
      intensity: Pixel intensity value (0-255).

  Returns:
      Darkness percentage (0-100).
  """
    return (255 - intensity) / 255 * 100


def print_chars(input_image):
    height, width = image.shape[:2]
    print(height, width)
    for y in range(height):  # Iterate through columns first
        for x in range(width):  # Then iterate through rows within each column
            pixel = input_image[y, x]
            darkness = calculate_darkness(pixel)
            match = get_nearest_key(charMap, darkness)
            print(match, end='')
        print()  # Add a newline after each "line" (column)


def output_to_file(input_image, output_filename="character_image.html"):
    """
  Processes an image, calculates darkness for each pixel, and writes corresponding
  characters to an HTML file with a specified font size.

  Args:
      input_image: A NumPy array representing the image.
      output_filename: Name of the output HTML file. (default: "character_image.html")
  """

    height, width = input_image.shape[:2]

    # Create the HTML content with font size style
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Character Image</title>
  <style>
    body {{
      font-size: 8pt;
      font-family: monospace;
      line-height: 0.6;
    }}
  </style>
</head>
<body>
<plaintext>
"""

    # Loop through pixels and create character representation
    for y in range(height):
        for x in range(width):
            pixel = input_image[y, x]
            darkness = calculate_darkness(pixel)
            match = get_nearest_key(charMap, darkness)
            html_content += match

        html_content += "\n"  # Add a line break after each row

    # Close the HTML content
    html_content += "</body>\n</html>"

    # Write the HTML content to the file
    with open(output_filename, "w") as output_file:
        output_file.write(html_content)


def get_nearest_key(data_map, target_value):
    """
  Finds the key in a map with the value closest to a target value.

  Args:
      data_map: A dictionary (map) containing key-value pairs.
      target_value: The target value to find the nearest neighbor for.

  Returns:
      The key in the map with the value closest to the target value.
  """
    closest_key = min(data_map.keys(), key=lambda key: abs(data_map[key] - target_value))
    return closest_key


charMap = create_font_mappings()
image_path = input("Please input a path to an image: \n")
image = process_image(image_path, 200)
output_to_file(image)
