# GmicUpdate 2 Obsidian Vault

python dump_to_obsidian.py -i update.gmic -o ./vault_gmic

ou 

wget https://gmic.eu/update400.json

python script.py -j update400.json -o ./vault_gmic


# Exemple pour le filtre : fx_circle_transform

## définition Json
```json
    {
      "name": "Circle Transform", "lang": "en", "command": "fx_circle_transform", "command_preview": "fx_circle_transform_preview", "parameters": [
      { "type": "note", "text": "<span color=\"#EE5500\">Description:</span> Warps the image according to a circle shape. " },
      { "type": "separator" },
      { "type": "point", "name": "Center (%)", "position": "50,50", "pos": "1" },
      { "type": "point", "name": "Radius", "position": "75,50", "pos": "3" },
      { "type": "float", "name": "X-Scale", "default": "-2", "min": "-16", "max": "16", "pos": "5" },
      { "type": "float", "name": "Y-Scale", "default": "-2", "min": "-16", "max": "16", "pos": "6" },
      { "type": "choice", "name": "Symmetry", "default": "0", "pos": "7", "choices": { "0": "None", "1": "Inside", "2": "Outside" } },
      { "type": "choice", "name": "Interpolation", "default": "1", "pos": "8", "choices": { "0": "Nearest Neighbor", "1": "Linear" } },
      { "type": "choice", "name": "Boundary", "default": "3", "pos": "9", "choices": { "0": "Transparent", "1": "Nearest", "2": "Periodic", "3": "Mirror" } },
      { "type": "bool", "name": "Preview Reference Circle", "default": "1", "pos": "10" },
      { "type": "separator" },
      { "type": "note", "text": "Author: <a href=\"https://tinyurl.com/3d9w4j3s\">David Tschumperlé</a>.      Latest Update: 2013/01/08." }
      ]
    }
```

## fiche Obsidian

### Structure de la commande
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

### Définition des variables
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

# Note
- le type value() en parametre n'est pas encore traité 
