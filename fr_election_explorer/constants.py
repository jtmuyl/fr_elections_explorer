ELECTION_DATA_DIR = "data/election_data"
RAW_ELECTION_DATA_DIR = f"{ELECTION_DATA_DIR}/raw"
PROCESSED_ELECTION_DATA_DIR = f"{ELECTION_DATA_DIR}/processed"

NATIONAL_ELECTIONS = ["presidentielle", "europeennes"]

HEADERS_STRUCTURE = {
    "burvot": {
        "presidentielle": {
            "base_columns": [
                "code_departement",
                "lib_departement",
                "code_circonscription",
                "lib_circonscription",
                "code_commune",
                "lib_commune",
                "code_bvote",
                "inscrits",
                "abstentions",
                "perc_abstention",
                "votants",
                "perc_participation",
                "blancs",
                "blancs_perc_inscrits",
                "blancs_perc_votants",
                "nuls",
                "nuls_perc_inscrits",
                "nuls_perc_votants",
                "exprimes",
                "exprimes_perc_inscrits",
                "exprimes_perc_votants",
            ],
            "candidates_columns": [
                "num_panneau",
                "sexe",
                "nom",
                "prenom",
                "count_voix",
                "perc_inscrits",
                "perc_exprimes",
            ],
            "fields_indices_for_simplified": [3,2]
        },
        "legislatives": {
            "base_columns": [
                "code_departement",
                "lib_departement",
                "code_circonscription",
                "lib_circonscription",
                "code_commune",
                "lib_commune",
                "code_bvote",
                "inscrits",
                "abstentions",
                "perc_abstention",
                "votants",
                "perc_participation",
                "blancs",
                "blancs_perc_inscrits",
                "blancs_perc_votants",
                "nuls",
                "nuls_perc_inscrits",
                "nuls_perc_votants",
                "exprimes",
                "exprimes_perc_inscrits",
                "exprimes_perc_votants",
            ],
            "candidates_columns": [
                "num_panneau",
                "sexe",
                "nom",
                "prenom",
                "nuance",
                "count_voix",
                "perc_inscrits",
                "perc_exprimes",
            ],
            "fields_indices_for_simplified": []
        },
        "europeennes": {
            "base_columns": [
                "code_departement",
                "lib_departement",
                "code_commune",
                "lib_commune",
                "code_bvote",
                "inscrits",
                "abstentions",
                "perc_abstention",
                "votants",
                "perc_participation",
                "blancs",
                "blancs_perc_inscrits",
                "blancs_perc_votants",
                "nuls",
                "nuls_perc_inscrits",
                "nuls_perc_votants",
                "exprimes",
                "exprimes_perc_inscrits",
                "exprimes_perc_votants",
            ],
            "candidates_columns": [
                "num_panneau",
                "lib_liste",
                "lib_liste_etendu",
                "tete_de_liste",
                "count_voix",
                "perc_inscrits",
                "perc_exprimes",
            ],
            "fields_indices_for_simplified": [1]
        },
    }
}
