import os

#specify the path of the source and target file

source_file = os.path.join("C:/Users/leilu/OneDrive/Prog/Dictionnaires/W40K/", "scraped_pages.txt")
target_file = os.path.join("C:/Users/leilu/OneDrive/Prog/Dictionnaires/W40K/", "scraped_pages_fixed.txt")


# read the content of the source file and store it in a list variable
with open(source_file, "r", encoding="utf-8") as source:
    text = source.readlines()


# create an empty list to store the corrected lines
lines = []

# iterate through each line in the source file content
for line in text:
    
    # create an empty variable to store the extracted content
    extracted_content = ""
    
    # iterate through each character in the line
    for char in line:
        
        if char == ">":
            # if the current character is a greater than (>) sign, we stop extracting content.
            extracted_content += char
            lines.append(extracted_content + "\n")
            break
        else:
            # if the current character is not a greater than (>) sign, continue to extract the content.
            extracted_content += char
            
# write the corrected lines to the target file
with open(target_file, "w", encoding="utf-8") as target:
    target.writelines(lines)
