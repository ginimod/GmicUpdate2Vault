python dump_to_obsidian.py -i update402.gmic -o ./Gmic_Vault


---
tags: [gmic, filter]
command: fx_circle_transform
---

# Filtre G'MIC : fx_circle_transform

## Structure de la commande
```text
fx_circle_transform:
    center_x = $1
    center_y = $2
    radius_x = $3
    radius_y = $4
    x_scale = $5
    y_scale = $6
    symmetry = $7
    interpolation = $8
    boundary = $9
    preview_reference_circle = $10
```

# Définition des variables
(Note) : <span color="#EE5500">Description:</span> Warps the image according to a circle shape. 
* **`Center (%)`** (point) : position = 0,0
* **`Radius`** (point) : position = 0,0
* **`X-Scale`** (float) : défaut = **-2**  (-16,16)
* **`Y-Scale`** (float) : défaut = **-2**  (-16,16)
* **`Symmetry`** (choice) : choix possibles => None, Inside, Outside
* **`Interpolation`** (choice) : choix possibles => Nearest Neighbor, Linear
* **`Boundary`** (choice) : choix possibles => Transparent, Nearest, Periodic, Mirror
* **`Preview Reference Circle`** (bool) : par défaut = Faux (0)
(Note) : Author: <a href="https://tinyurl.com/3d9w4j3s">David Tschumperlé</a>.      Latest Update: 2013/01/08.
