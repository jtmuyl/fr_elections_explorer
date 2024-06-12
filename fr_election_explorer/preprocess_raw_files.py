import re
import os
import csv
from charset_normalizer import from_path
from tqdm import tqdm


from constants import (
    RAW_ELECTION_DATA_DIR,
    PROCESSED_ELECTION_DATA_DIR,
    HEADERS_STRUCTURE,
    NATIONAL_ELECTIONS,
)


def detect_encoding(file_path: str) -> str:
    result = from_path(file_path)
    # Choose the best guess
    if result.best():
        return result.best().encoding
    return None


def detect_delimiter(file_path: str) -> str:
    with open(file_path, newline="", encoding="iso8859-15") as file:
        header = file.readline()
        sniffer = csv.Sniffer()
        delimiter = sniffer.sniff(header).delimiter
        return delimiter


def replace_comma_in_quotes(match):
    # Replace commas with semicolons in the matched string
    # Get the matched text
    matched_text = match.group(0)

    # Check if '%' is present in the matched string
    if "%" in matched_text:
        # Return the original matched text if '%' is found
        return matched_text
    else:
        # Replace spaces with underscores if '%' is not found
        return matched_text.replace(",", ";")


def explode_files():
    """
    This function takes the raw french elections data files at the voting place (bureau de vote)
    level and explode the rows into one raw per candidate per voting place, instead of the
    default structure.
    """

    # we loop on the files that were downloaded by the make download-data command
    for filepath in [
        f"{RAW_ELECTION_DATA_DIR}/{e}" for e in os.listdir(RAW_ELECTION_DATA_DIR)
    ]:
        if "europeennes_2024" not in filepath:
            pass
        exploded_output_filepath = (
            f"{PROCESSED_ELECTION_DATA_DIR}/exploded_{filepath.split('/')[-1][:-4]}.tsv"
        )

        simplified_output_filepath = f"{PROCESSED_ELECTION_DATA_DIR}/simplified_{filepath.split('/')[-1][:-4]}.tsv"

        election_type = filepath.split("/")[-1].split("_")[0]
        level = filepath.split("/")[-1].split("_")[-1][:-4]
        year = filepath.split("/")[-1].split("_")[1]

        # we create these variables to make the following code a tiny bit less verbose.
        base_columns_ref = HEADERS_STRUCTURE[level][election_type][year]["base_columns"]
        candidates_columns_ref = HEADERS_STRUCTURE[level][election_type][year][
            "candidates_columns"
        ]
        naming_fields_ref = HEADERS_STRUCTURE[level][election_type][year][
            "fields_indices_for_simplified"
        ]
        perc_exprimes_index_ref = HEADERS_STRUCTURE[level][election_type][year][
            "perc_exprimes_index"
        ]

        # we get the delimiter
        delimiter = detect_delimiter(filepath)

        # we get the encoding
        encoding_str = detect_encoding(filepath)

        print(filepath, delimiter, encoding_str)

        # we prepare headers based on the ressource file #iso8859-15
        exploded_headers = base_columns_ref + candidates_columns_ref
        with open(filepath, "r", encoding=encoding_str) as f, open(
            exploded_output_filepath, "w", encoding="utf8"
        ) as f_exploded:
            base_columns_index = len(base_columns_ref)
            chunk_size = len(candidates_columns_ref)
            f_exploded.write("\t".join(exploded_headers) + "\n")

            # skip headers and loop on rows
            next(f)
            simplified_headers_done = False
            for line in tqdm(f, desc=filepath.split("/")[-1]):
                line = line.replace("\n", "")

                # we handle things slightly differently if the delimiter is ","
                if delimiter == ",":
                    # if there are commas un the quotes, we replace them by semicolons
                    line = re.sub(r'"[^"]*"', replace_comma_in_quotes, line)

                    # in some instances, there are multiple double quotes in a given column. Don't ask me why...
                    # so we remove these as they break the parsing
                    line = re.sub(r'""', "", line)

                    # we remove the percentage signs:
                    line = re.sub(r"%", "", line)

                    # we find the columns, with or without quotes
                    parts = re.findall(r'"[^"]*"|[^,]+', line)
                    splitted = [part.strip('"') for part in parts]

                else:
                    splitted = line.split(delimiter)
                # we isolate the generic columns and change the decimal sign to .
                base_columns = [
                    e.replace(",", ".") for e in splitted[:base_columns_index]
                ]
                # we isolate the per candidate columns
                candidates_columns = splitted[base_columns_index:]
                simplified_row = list(base_columns)
                simplified_columns_names = list(base_columns_ref)

                # we iterate through the candidates chunk in the candidates columns
                for i in range(0, len(candidates_columns), chunk_size):
                    candidate_data = candidates_columns[i : i + chunk_size]
                    # if the candidates are the same nationaly, we can create a "simplified" version
                    if election_type in NATIONAL_ELECTIONS:
                        slug = "cd__" + "_".join(
                            [str(candidate_data[e]).lower() for e in naming_fields_ref]
                        ).replace(" ", "_")
                        simplified_columns_names.append(slug)
                        simplified_row.append(
                            candidate_data[perc_exprimes_index_ref].replace(",", ".")
                        )

                    # we write each candidate to a different row for the exploded file
                    exploded_row = base_columns + candidate_data
                    f_exploded.write("\t".join(exploded_row) + "\n")
                if election_type in NATIONAL_ELECTIONS:
                    if not simplified_headers_done:
                        with open(
                            simplified_output_filepath, "w", encoding="utf8"
                        ) as f_simplified:
                            f_simplified.write(
                                "\t".join([str(e) for e in simplified_columns_names])
                                + "\n"
                            )
                        simplified_headers_done = True
                    with open(
                        simplified_output_filepath, "a", encoding="utf8"
                    ) as f_simplified:
                        f_simplified.write(
                            "\t".join([str(e) for e in simplified_row]) + "\n"
                        )


if __name__ == "__main__":
    explode_files()
