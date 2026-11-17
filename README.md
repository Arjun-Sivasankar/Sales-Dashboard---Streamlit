# Sales Dashboard (Streamlit)

Interactive sales dashboard built with **Streamlit**, with a login and logout gate in front of it so the data is not simply open to anyone with the URL.

| File | What it does |
|---|---|
| `app.py` | The dashboard itself |
| `Helper Notebook.ipynb` | Data exploration that shaped the charts |
| `config.yaml` | Dashboard settings |
| `config_hashpassw.yaml` | Hashed credentials for the login gate |
| `.streamlit/config.toml` | Streamlit theme and server settings |

## Running it

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

The credentials file holds a hash rather than the password itself, but for anything beyond a personal project the login gate belongs in a real identity provider rather than in the Streamlit app.
