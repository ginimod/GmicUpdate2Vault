import argparse
import json
import os
import subprocess
import sys
from jinja2 import Environment, FileSystemLoader
from slugify import slugify

def get_choices(choices_raw):
    """Extrait et trie les choix qu'ils soient sous forme de dictionnaire ou de liste."""
    match choices_raw:
        case dict():
            try:
                sorted_keys = sorted(choices_raw.keys(), key=lambda x: int(x))
            except ValueError:
                sorted_keys = sorted(choices_raw.keys())
            return [choices_raw[k] for k in sorted_keys]
        case list():
            return choices_raw
        case _:
            return []

def get_parameter(param):
    """Valide et construit le dictionnaire d'un paramètre G'MIC, ou renvoie None si invalide."""
    if not isinstance(param, dict):
        return None

    p_name = param.get("name") or "Sans nom"
    p_type = param.get("type") or "unknown"

    if p_name == "Sans nom" or not p_name.strip():
        p_slug = slugify(p_type, separator="_")
    else:
        p_slug = slugify(p_name, separator="_")

    return {
        "name": p_name,
        "type": p_type,
        "text": param.get("text", ""),
        "default": param.get("default"),
        "min": param.get("min"),
        "max": param.get("max"),
        "choices": get_choices(param.get("choices", [])),
        "safe_slug": p_slug,
        "pos": param.get("pos", 0),
        "arguments": param.get("arguments", []),
    }


def get_signature(parameters):
    """Génère un dictionnaire de signature associant chaque position (pos)
        cas de value() non traité
    """
    signature = {}
    for param in parameters:
        p_type = param.get("type", "note")
        slug = param["safe_slug"]
        pos = int(param["pos"])
        match p_type:
            case "int" | "float" | "bool" | "choice":
                signature[pos] = slug

            case "point":
                signature[pos]     = f"{slug}_x"
                signature[pos + 1] = f"{slug}_y"

            case "color":
                arguments = param.get("arguments", [])
                num_args = len(arguments)
                suffixes = ["_r", "_g", "_b", "_a"] if num_args == 4 else ["_r", "_g", "_b"]
                for i, suffix in enumerate(suffixes[:num_args]):
                    signature[pos + i] = f"{slug}{suffix}"

            case "value":
                pass
    return signature


def extract_filters(data, parent_key=None):
    filters = []
    match data:
        case dict():
            if "parameters" in data or "command" in data:
                cmd = data.get("command") or parent_key or "commande_inconnue"
                cmd_clean = str(cmd).strip().lower()

                if cmd_clean not in ["_none_", "commande_inconnue", ""]:
                    filter_item = {
                        "filter_name": data.get("filter_name") or parent_key or cmd,
                        "command": cmd,
                        "parameters": [],
                        "signature": {},
                    }

                    params = data.get("parameters", [])
                    for param in params:
                        if (parsed_param := get_parameter(param)) is not None:
                            filter_item["parameters"].append(parsed_param)

                    filter_item["signature"] = get_signature(filter_item["parameters"])
                    filters.append(filter_item)

            for key, val in data.items():
                filters.extend(extract_filters(val, parent_key=key))
        case list():
            for item in data:
                filters.extend(extract_filters(item, parent_key=parent_key))
        case _:
            pass
    return filters

def main(input_gmic, json_input, output_dir, template):
    json_pivot = "out.json"

    if json_input:
        print(f"Utilisation du fichier JSON : {json_input}...", flush=True)
        json_pivot = json_input
    elif input_gmic:
        print(f"Extraction des filtres depuis {input_gmic} via G'MIC...", flush=True)
        cmd = ["gmic", "-input_text", input_gmic, "-parse_gui", "json", "-output_text", json_pivot]
        try:
            subprocess.run(cmd, check=True)
            print(f"Fichier {json_pivot} généré.\n")
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'exécution de G'MIC : {e}", file=sys.stderr)
            return
        except FileNotFoundError:
            print("Erreur : La commande 'gmic' est introuvable.", file=sys.stderr)
            return
    else:
        print("Erreur : Vous devez spécifier soit un fichier G'MIC (-i) soit un JSON (-j).", file=sys.stderr)
        return

    os.makedirs(output_dir, exist_ok=True)
    try:
        with open(json_pivot, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier JSON ({json_pivot}) : {e}", file=sys.stderr)
        return

    all_filters = extract_filters(data)

    if not all_filters:
        print("Aucun filtre valide détecté.")
        return
    print(f"→ {len(all_filters)} filtre(s) valide(s) trouvé(s).")

    success_count = 0
    for f_data in all_filters:
        try:
            markdown_content = template.render(filter=f_data)
            filename = slugify(f_data["command"], separator="_")
            file_path = os.path.join(output_dir, f"{filename}.md")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            success_count += 1
        except Exception as e:
            print(f"⚠ Erreur sur le filtre {f_data.get('command')}: {e}")

    print(f"✓ Terminé ! {success_count} fichier(s) Markdown généré(s).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convertisseur G'MIC vers Vault Obsidian")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-i", "--input", help="Fichier source texte G'MIC")
    group.add_argument("-j", "--json-input", help="Fichier JSON pré-téléchargé (ex: update400.json)")
    parser.add_argument("-o", "--output", required=True, help="Dossier de sortie Obsidian")
    args = parser.parse_args()

    template_file = "template_obsidian.md"
    env = Environment( loader=FileSystemLoader("."),trim_blocks=True,lstrip_blocks=True )
    template = env.get_template(template_file)

    main(input_gmic=args.input,json_input=args.json_input,output_dir=args.output,template=template )
