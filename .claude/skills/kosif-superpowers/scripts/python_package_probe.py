#!/usr/bin/env python3
"""Read-only Python distribution presence probe.

No imports of selected packages, downloads, installs, network calls, device access,
secrets or arbitrary imports. Metadata presence != functional readiness.
"""
import argparse
from importlib import metadata
import json
import re
import sys

NAME_RE=re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")


def probe(packages):
    if len(packages)>50:
        raise ValueError("maximum 50 packages")
    records=[]
    seen=set()
    for name in packages:
        if not NAME_RE.fullmatch(name):
            raise ValueError("invalid distribution name")
        normalized=re.sub(r"[-_.]+","-",name).lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        try:
            version=metadata.version(name)
            status="distribution_metadata_found"
        except metadata.PackageNotFoundError:
            version=None
            status="not_found_in_environment"
        records.append({
            "distribution":name,
            "status":status,
            "version":version,
            "import_tested":False,
            "execution_tested":False,
            "ready_for_production":False
        })
    return {"python_version":sys.version.split()[0], "packages":records,
            "reference":"https://github.com/vinta/awesome-python",
            "scope":"current_environment_only_no_install_no_network"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("packages",nargs="+")
    a=parser.parse_args()
    try:
        print(json.dumps(probe(a.packages),ensure_ascii=False,indent=2))
    except ValueError as err:
        parser.error(str(err))


if __name__=="__main__":
    main()
