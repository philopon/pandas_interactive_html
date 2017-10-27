import pandas
from rdkit import Chem
from rdkit.Chem import Draw

import pandas_interactive_html

# register to_interactive_html method to pandas DataFrame
pandas_interactive_html.register()


df = pandas.DataFrame(
    [
        [m.GetProp("_Name"), m]
        for m in Chem.SDMolSupplier("mol.sdf")
    ],
    columns=["name", "mol"],
)


df.to_interactive_html("mol.html", image_columns={"mol"}, converter={"mol": Draw.MolToImage})
