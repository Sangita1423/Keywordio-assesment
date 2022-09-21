data = get_data()
data = data.rename(columns={"JMDGRPUNIT": "jmdgrpunit", "ZONEGRPUNIT": "zonegrpunit", "ExpSubCategoryDescr": "expsubcategory"})

ics = data['zonegrpunit'].drop_duplicates()
ics_choice = st.sidebar.selectbox("Select your zonegrpunit:", ics)
practices = list(data["expsubcategory"].loc[data["zonegrpunit"] == ics_choice])
practice_choice = st.sidebar.multiselect("Select practices", practices)

data.loc[(data['zonegrpunit'] == ics_choice) & (data['expsubcategory'].isin(practice_choice))]


"UnitShrtDescr": "unitshrtdescr"