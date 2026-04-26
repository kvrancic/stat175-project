# Legacy `networkrepository.com` zips

These were the team's first download from
[networkrepository.com/socfb.php](https://networkrepository.com/socfb.php).
That mirror provides only the adjacency in Matrix Market `.mtx` format —
**without** the Facebook100 node attributes (dorm, year, major, gender,
status, high school).

The cost function `c_e = sigmoid(<x_u, x_v>)` and the GNN policy both need
those attributes, so we abandoned this mirror in favor of the canonical
Oxford `.mat` files at
[archive.org/details/oxford-2005-facebook-matrix](https://archive.org/details/oxford-2005-facebook-matrix).
That archive is now downloaded and extracted automatically by
`scripts/01_download_data.py` into `data/raw/`.

Kept under `data/legacy_networkrepository/` only as a record of provenance;
nothing in the pipeline reads from it.
