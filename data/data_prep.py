import pandas as pd

raw_df = pd.read_csv("key-crop-yields.csv")
df = raw_df.copy()
df.columns = df.columns.str.extract(r"(\w*\b)", expand=False)
df = df.rename(columns={"Entity": "Country"})
df = df[df.Code.str.len().eq(3)]  # Countries only, no aggregations

country_code_meta = pd.read_csv(
    "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.csv"
)
country_code_meta = country_code_meta.rename(
    columns={
        "alpha-3": "Code",
        "region": "Region",
        "sub-region": "SubRegion",
    }
)[["Code", "Region", "SubRegion"]]

df = df.merge(country_code_meta, on="Code", how="left")
df = df.melt(
    id_vars=["Country", "Code", "Year", "Region", "SubRegion"],
    var_name="Crop",
    value_name="Yield",
)
df = df.sort_values(["Country", "Crop", "Year"])

co2_df = (
    pd.read_csv("owid-co2-data.csv")
    .rename(
        columns={
            "iso_code": "Code",
            "year": "Year",
            "population": "Population",
            "gdp": "GDP",
        }
    )
    .dropna(subset="Population")
)


df = df.merge(
    co2_df[["Code", "Year", "Population", "GDP"]], on=["Code", "Year"], how="left"
)
df.Population = df.Population.astype("Int64")
df["GDPPC"] = df.GDP / df.Population

df = df[
    [
        "Region",
        "SubRegion",
        "Country",
        "Crop",
        "Year",
        "Yield",
        "Population",
        "GDPPC",
    ]
]
# df.to_csv("crop-data.csv", index=False)
