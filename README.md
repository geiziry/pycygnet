# PyCygNet

PyCygNet is a Python project designed to simplify and enhance working with the CygNet COM API and perform data analytics on CygNet data. By passing in the CygNet site and domain, it initializes a number of CygNet clients such as `ddsclient`, `facclient`, and `pntclient`, which are pre-connected to services and ready to use as per the CygNet COM API documentation. Additionally, PyCygNet offers advanced capabilities for executing SQL queries using ODBC, returning results in Polars DataFrames, and integrating AI/ML workflows into CygNet via a complementary COM server.

---

## Features
- **CygNet Client Initialization**: Automatically connects and initializes multiple CygNet clients (`ddsclient`, `facclient`, `pntclient`).
- **Notebook-Friendly SQL Analytics**: Run SQL queries with results returned as Polars DataFrames for easy data analysis.
- **Python Task Scheduling**: Integrate Python AI/ML workflows directly into CygNet through its scheduler using a complementary COM server.

---

## Installation
This project uses [Rye](https://github.com/mitsuhiko/rye) to manage dependencies. Follow these steps to set up the project:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pycygnet.git
   cd pycygnet
   ```

2. Install Rye (if not already installed):
   ```bash
   curl -sSf https://rye-up.com/install.sh | sh
   ```

3. Use Rye to create and manage the virtual environment and dependencies:
   ```bash
   rye sync
   ```

4. Verify the installation by running one of the provided scripts:
   ```bash
   rye run esp
   ```

---

## Usage
### Example 1: Initializing Clients
```python
from pycygnet import Site

site = "YourSite"
domain = "YourDomain"

cygnet = Site(site, domain)
dds_client = cygnet.dds_client
fac_client = cygnet.fac_client
```

### Example 2: Running SQL Queries
```python
import polars as pl
from pycygnet import run_sql_query

query = "SELECT * FROM YourTable"
result = site.odbc_nav.run_sql_query(query)
print(result)
```

### Example 3: Scheduling Python Tasks in CygNet
Register your Python scripts with the CygNet scheduler:
```bash
rye run regcom
```
Unregister the COM server:
```bash
rye run unregcom
```

---

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature/bugfix.
3. Submit a pull request with a detailed explanation of your changes.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Contact
For questions or support, contact:
**Mahmoud Elgeiziry**  
Email: mahmoud.geiziry@gmail.com
