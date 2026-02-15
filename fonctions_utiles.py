import pandas as pd

def unique_species_per_department(df):
    result = (
        df.groupby("departement", observed=True)["species"]
          .nunique()
          .reset_index(name="unique_species_count")
    )

    species_dict = dict(zip(result['departement'], result['unique_species_count']))

    return species_dict