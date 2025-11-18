import json

def forward_chaining(selected_gejala, rules):
    """
    Exact-match forward chaining.
    """
    if not selected_gejala:
        return None

    selected_set = set(selected_gejala)

    for rule in rules:
        req = set(rule.get("if", []))
        if selected_set == req:
            return rule.get("then")
    return None
