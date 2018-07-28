#Summary

Process OSM data with python 3. This project is mainly motivated by [openstreetmap](https://github.com/johnyf/openstreetmap).

# Dependencies

- [scipy](https://www.scipy.org/), [numpy](http://www.numpy.org/)
- [networkx](https://networkx.github.io/)

# Install
You can install [osmRoad](https://pypi.org/project/osmRoad/) via `pip`.

```shell
pip install osmRoad
```

# Usage

```
from osm import parser
from osm import road
```
## parser
- `load_parse_osm`: return `bounds`, `nodes`, `ways`
- `load_parse_osmxy`: different from above, return `nodes` with coodinates

## road
- `extract_connectivity`: return the adjecent matrix `lil_matrix` (without weights)
- `extract_adj`: return the adjecent list (without weights)
- `extract_edges`: return the edges (without weights)
- `build_graph`: return a `graph` in `networkx` (with weights)

# Example

```
parsed_osm = parser.load_parse_osmxy(r"osm/Beijing.osm")
r = road.build_graph(parsed_osm)
print(nx.dijkstra_path(r, 296314321, 296314277))
```

```
parsed_osm = parser.load_parse_osm(r"osm/Beijing.osm")
m = road.extract_adj(parsed_osm)
```