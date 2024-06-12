import os
from tqdm import tqdm

from constants import (
    RAW_ELECTION_DATA_DIR,
    PROCESSED_ELECTION_DATA_DIR,
    HEADERS_STRUCTURE,
    NATIONAL_ELECTIONS,
)


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
        exploded_output_filepath = (
            f"{PROCESSED_ELECTION_DATA_DIR}/exploded_{filepath.split('/')[-1][:-4]}.tsv"
        )

        simplified_output_filepath = f"{PROCESSED_ELECTION_DATA_DIR}/simplified_{filepath.split('/')[-1][:-4]}.tsv"

        election_type = filepath.split("/")[-1].split("_")[0]
        level = filepath.split("/")[-1].split("_")[-1][:-4]

        # we prepare headers based on
        exploded_headers = (
            HEADERS_STRUCTURE[level][election_type]["base_columns"]
            + HEADERS_STRUCTURE[level][election_type]["candidates_columns"]
        )
        with open(filepath, "r", encoding="iso8859-15") as f, open(
            exploded_output_filepath, "w", encoding="utf8"
        ) as f_exploded:
            base_columns_index = len(
                HEADERS_STRUCTURE[level][election_type]["base_columns"]
            )
            chunk_size = len(
                HEADERS_STRUCTURE[level][election_type]["candidates_columns"]
            )
            f_exploded.write("\t".join(exploded_headers) + "\n")

            # skip headers and loop on rows
            next(f)
            simplified_headers_done = False
            for line in tqdm(f):
                splitted = line.replace("\n", "").split(";")
                # we isolate the generic columns and change the decimal sign to .
                base_columns = [
                    e.replace(",", ".") for e in splitted[:base_columns_index]
                ]
                # we isolate the per candidate columns
                candidates_columns = splitted[base_columns_index:]
                simplified_row = list(base_columns)
                simplified_columns_names = list(
                    HEADERS_STRUCTURE[level][election_type]["base_columns"]
                )
                # we iterate through the candidates chunk in the candidates columns
                for i in range(0, len(candidates_columns), chunk_size):
                    candidate_data = candidates_columns[i : i + chunk_size]
                    # if the candidates are the same nationaly, we can create a "simplified" version
                    if election_type in NATIONAL_ELECTIONS:
                        slug = "cd" + "__"+"_".join(
                            [
                                str(candidate_data[e]).lower()
                                for e in HEADERS_STRUCTURE[level][election_type][
                                    "fields_indices_for_simplified"
                                ]
                            ]
                        ).replace(" ", "_")
                        simplified_columns_names.append(slug)
                        simplified_row.append(candidate_data[-1].replace(",", "."))

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
