#!/usr/bin/env python3
"""mbrc-validate - check an MBRC 1.0 result record against the published schema.

Usage:  python3 mbrc-validate.py record.json [schema.json]

Reads the record, applies the schema, and prints every field that is missing,
empty, unknown or outside its permitted set. Exit status 0 when the record is
conformant, 1 when it is not, 2 when a file could not be read.

Conformance under MBRC 1.0 means: every field required for the branches the
record declares is present and non-empty. It is a self-declaration. This script
can tell you that a record is incomplete. It cannot tell you whether the values
in it are true.

No third-party packages are required. Licence CC0 1.0.
"""
import json
import os
import sys

SCHEMA_DEFAULT = "mbrc.schema.json"


def check(node, schema, path, errors):
    """Apply the subset of JSON Schema that the MBRC schema uses."""
    t = schema.get("type")
    if t == "object" and not isinstance(node, dict):
        errors.append((path, "expected an object"))
        return
    if t == "string":
        if not isinstance(node, str):
            errors.append((path, "expected a string"))
            return
        if len(node) < schema.get("minLength", 0):
            errors.append((path, "is empty"))
            return

    if "const" in schema and node != schema["const"]:
        errors.append((path, "must be %r, found %r" % (schema["const"], node)))
    if "enum" in schema and node not in schema["enum"]:
        errors.append((path, "must be one of %s, found %r" % (", ".join(map(repr, schema["enum"])), node)))

    if not isinstance(node, dict):
        return

    props = schema.get("properties", {})
    for name in schema.get("required", []):
        if name not in node:
            errors.append((path, "required field %r is missing" % name))
    if schema.get("additionalProperties") is False:
        for name in node:
            if name not in props:
                errors.append((path, "unknown field %r" % name))
    for name, sub in props.items():
        if name in node:
            check(node[name], sub, path + "/" + name if path else name, errors)

    for clause in schema.get("allOf", []):
        cond = clause.get("if")
        if cond is None:
            check(node, clause, path, errors)
            continue
        holds = all(k in node for k in cond.get("required", []))
        for k, expected in cond.get("properties", {}).items():
            if "const" in expected and node.get(k) != expected["const"]:
                holds = False
        if holds:
            check(node, clause.get("then", {}), path, errors)


def load(name):
    try:
        with open(name, encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        sys.exit("cannot read %s: %s" % (name, exc.strerror))
    except ValueError as exc:
        sys.exit("%s is not valid JSON: %s" % (name, exc))


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        sys.stdout.write(__doc__)
        return 0
    record = load(argv[1])
    schema_path = argv[2] if len(argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), SCHEMA_DEFAULT)
    schema = load(schema_path)

    errors = []
    check(record, schema, "", errors)

    declared = record.get("schema")
    if declared and declared != schema.get("properties", {}).get("schema", {}).get("const"):
        print("note: this record declares %r; validated against %s"
              % (declared, schema.get("$id", schema_path)))

    if not errors:
        print("conformant: every field required by the declared branches is present and non-empty.")
        print("this is a self-declaration; the values themselves are not checked.")
        return 0

    seen = set()
    print("not conformant - %d problem(s):" % len(errors))
    for where, what in errors:
        line = "  %s: %s" % (where or "(record)", what)
        if line not in seen:
            seen.add(line)
            print(line)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
