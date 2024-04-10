# RePoE

Repository of Path of Exile resources for tool developers.

Contains data about stats, mods, base items, gems and more. See the `data`
folder for those files and the `docs` folder for their documentation.

## How to set this up

Make sure you're running python version >=3.11

```
git clone git@github.com:Liberatorist/RePoE.git
cd RePoE
git clone git@github.com:Project-Path-of-Exile-Wiki/PyPoE.git
python3 -m venv .venv
source .venv/bin/activate
cd PyPoE
poetry install
cd ..
pip install -e .
```

## How to run this

```
python3 RePoE/run_parser.py all -f {POE_PATH}
```

where {POE_PATH} is the path where the PoE ggpk file is located
For me working in WSL this is POE_PATH="/mnt/c/Program Files (x86)/Grinding Gear Games/Path of Exile"

## How upload this to pypi

After running the parser, change the version in setup.py and run

```
python3 -m build
python3 -m twine upload dist/*
```

and enter pypi api-key when prompted

## Files

The [RePoE/data](RePoE/data) folder contains the generated data in Json format. Each file has a
formatted and a compact version. The formatted versions complement their descriptions
in the [RePoE/docs](RePoE/docs) folder.

Note that the file formats are not final, they may change at any time, e.g. when the format
of files in the GGPK changes.

The following data is currently available:

- `stat_translations.json`: Maps stat ids together with their values to human-readable
  text. This is the text that appears on items in-game.
- `stats.json`: Describes stat ids. Defines whether they are local and whether they
  are aliased depending on main-hand or off-hand.
- `mods.json`: Describes mod ids. Defines which items they can appear on and what
  stats with what values they have.
- `crafting_bench_options.json`: Describes master crafting options. Defines which
  masters can craft them at which level on which items.
- `npc_master.json`: Describes the master's signature mods and on which items they
  can appear.
- `gems.json`: Describes skill gems and skill gem effects only provided by mods.
- `gem_tags.json`: Simple object that contains all gem tags with their internal id as
  keys and their translation as value.
- `base_items.json`: Describes base item types. Contains information applicable to
  all item types, e.g. inventory size, item class and tags, as well as attribute
  requirements and properties.
- `tags.json`: Lists all possible item tags. These are the tags used in `base_items.json` and
  `mods.json`.
- `item_classes.json`: Defines the item class ids and the tags added to items when they are
  Shaper/Elder items.
- `essences.json`: Describes essences. Defines the mods they spawn on items of the different
  item classes and general information like level and tier.
- `default_monster_stats.json`: Describes the stat base values of monsters at specific levels.
- `characters.json`: Describes the stat base values of the different player character classes.
- `flavour.json`: Table containing the flavour text used throughout the game.
- `fossils.json`: Describes fossils. Defines the mods they spawn, the tags they affect, and
  auxillary effects of the fossils.
- `mod_types.json`: Describes the types of mods with sell price information and the tags
  relevant for fossil crafting.
- `cluster_jewels.json`: Describes how cluster jewels can be generated and how they influence the passive tree.
- `cluster_jewel_notables.json`: Lists the notable and keystone passive skills that can appear on cluster jewels.
- `cost_types.json`: Defines the resource cost types used in `gems.json`.
- `active_skill_types.json` List the active skill types used in `gems.json`.

## Credits

- [Grinding Gear Games](http://www.grindinggear.com/) for
  [Path of Exile](https://www.pathofexile.com/). The contents of all `data` files
  obviously belong to them.
- [OmegaK2](https://github.com/OmegaK2/) for [PyPoE](https://github.com/OmegaK2/PyPoE).
- [brather1ng](https://github.com/brather1ng) for the original [RePoE](https://github.com/brather1ng/RePoE) and their [PyPoE Fork](https://github.com/brather1ng/PyPoE)
- Everyone at the [PoE Wiki Fork of PyPoE](https://github.com/Project-Path-of-Exile-Wiki/PyPoE) which is used in this project
- [ltogniolli](https://github.com/ltogniolli) for the [RePoE Fork](https://github.com/ltogniolli/RePoE) this is based on
