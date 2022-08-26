from yellowbrick.text import TSNEVisualizer
from distinctipy import get_colors, get_hex

def plot_clusters(data, column, return_data = False):  
    # Use distinctipy's get_colors and get_hex
    # to get a list of distinct colors automatically
    groupings = data[column]
    colors = get_colors(len(set(groupings)), pastel_factor = 0.2)
    color_hex = [get_hex(x) for x in colors]
    X = data.filter(regex='st_emb_.*')
    
    # TSNE will project the 768-dimensions down to 2 for visualization
    # The projection might look messy as who knows what hyperplanes/spheres are
    # actually separating the clusters.
    tsne = TSNEVisualizer(random_state = 0, colors = color_hex, 
                          alpha = 0.8)
    column_name = column.title()
    tsne.fit(X, [f"{column_name} Cluster: {k:02d}" for k in groupings])
    tsne.show()

    if return_data:
        out = data.copy(deep = True)
        out["groupings"] = groupings
        return out