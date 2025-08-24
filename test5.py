import maya.cmds as cmds
from typing import List


def _to_unique_long_path(name: str) -> str:
    """Resolve a node name (short or long) to a single, unique long DAG path.
    - If the short name matches multiple nodes (or an instanced node has multiple paths),
      this raises an error. In that case, pass an explicit long path to disambiguate.
    """
    if not cmds.objExists(name):
        raise ValueError(f"'{name}' does not exist.")

    matches = cmds.ls(name, long=True) or []
    # Deduplicate in case Maya returns duplicates
    matches = list(dict.fromkeys(matches))

    if len(matches) == 1:
        return matches[0]

    # Ambiguity: either short name used by multiple nodes or an instanced node with multiple DAG paths
    raise ValueError(
        f"Ambiguous name '{name}'. It resolves to multiple DAG paths:\n{matches}\n"
        "Please pass an explicit long path (e.g., '|root|grp|node') to disambiguate."
    )

def get_downstream_path(start: str, end: str, short_name: bool = True) -> List[str]:
    """Return the path (inclusive) from `start` (ancestor) down to `end` (descendant).

    - Accepts both short names and long names (with '|').
    - Internally resolves to unique **long** DAG paths and walks parents from `end` up to `start`.
    - If `return_short_names=True`, returns short names; otherwise returns long paths.

    Parameters
    ----------
    start : str
        Ancestor (or same) node name. Short or long.
    end : str
        Descendant (or same) node name. Short or long.
    return_short_names : bool, default False
        If True, convert each result to its short name.

    Raises
    ------
    ValueError
        If names don't exist, are ambiguous (multiple DAG paths), or `start` is not an ancestor of `end`.

    Examples
    --------
    >>> get_downstream_path('|root|joint2', '|root|joint2|joint8|joint9|joint10')
    ['|root|joint2', '|root|joint2|joint8', '|root|joint2|joint8|joint9', '|root|joint2|joint8|joint9|joint10']

    >>> get_downstream_path('joint2', 'joint10', return_short_names=True)
    ['joint2', 'joint8', 'joint9', 'joint10']  # assuming unique short names in the scene
    """
    # Resolve to unique long paths
    start_long = _to_unique_long_path(start)
    end_long = _to_unique_long_path(end)

    # Quick success case
    if start_long == end_long:
        return [cmds.ls(start_long, sn=True)[0]] if short_name else [start_long]

    # Build path end -> start by walking parents with fullPath=True
    chain = [end_long]
    current = end_long

    while True:
        if current == start_long:
            break
        parents = cmds.listRelatives(current, parent=True, fullPath=True) or []
        if not parents:
            # Reached root without encountering start
            raise ValueError(f"'{start}' is not an ancestor of '{end}'.")
        current = parents[0]
        chain.append(current)

    chain.reverse()

    if short_name:
        # Convert each long path to its short name (unique leaf name)
        chain = [cmds.ls(p, sn=True)[0] for p in chain]

    return chain


a = get_downstream_path("joint2", "joint12", True)

print(a)