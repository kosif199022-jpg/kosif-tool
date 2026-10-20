#!/usr/bin/env python3
"""KOSIF deterministic capacity sizing sketch, inspired by system-design-primer.

All inputs are caller assumptions. This does not benchmark a production system,
and it does not include indexes, caching, backups, compression or network costs.
"""
import argparse
from decimal import Decimal, InvalidOperation, ROUND_CEILING
import json


def dec(value, *, positive=True):
    try:
        x=Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("invalid decimal input") from exc
    if not x.is_finite() or (positive and x <= 0) or (not positive and x < 0):
        raise ValueError("non-finite or out-of-range input")
    return x


def ceil(value):
    return int(value.to_integral_value(rounding=ROUND_CEILING))


def size_system(daily_requests, peak_factor, payload_bytes, retention_days,
                replica_rps, target_utilization, copies=1):
    calls=dec(daily_requests)
    peak=dec(peak_factor)
    payload=dec(payload_bytes)
    retention=dec(retention_days)
    capacity=dec(replica_rps)
    utilization=dec(target_utilization)
    # Parse copies as a decimal first so "1.5" or "two" get the same clear
    # message instead of int()'s raw "invalid literal" text.
    try:
        copies_dec=dec(copies)
    except ValueError:
        raise ValueError("copies must be a positive integer") from None
    if copies_dec != copies_dec.to_integral_value():
        raise ValueError("copies must be a positive integer")
    ncopy=int(copies_dec)
    if peak < 1 or utilization > 1:
        raise ValueError("peak factor >=1, 0<utilization<=1, copies positive integer")
    average_rps=calls/Decimal(86400)
    peak_rps=average_rps*peak
    replicas=ceil(peak_rps/(capacity*utilization))
    logical_bytes=ceil(calls*payload*retention)
    retained_bytes=logical_bytes*ncopy
    return {
        "status":"deterministic_estimate_not_load_test",
        "inputs":{"daily_requests":str(calls),"peak_factor":str(peak),
                  "payload_bytes":str(payload),"retention_days":str(retention),
                  "replica_rps":str(capacity),"target_utilization":str(utilization),"copies":ncopy},
        "average_rps":str(average_rps.quantize(Decimal("0.000001"))),
        "peak_rps":str(peak_rps.quantize(Decimal("0.000001"))),
        "peak_rps_ceiling":ceil(peak_rps),
        "minimum_replicas":replicas,
        "logical_storage_bytes":logical_bytes,
        "retained_storage_bytes":retained_bytes,
        "storage_gib":str((Decimal(retained_bytes)/Decimal(1024**3)).quantize(Decimal("0.001"))),
        "assumptions":"per-request retained byte amount, linear peak factor, static per-replica sustained throughput",
        "exclusions":["database indexes","caching","log overhead","backups","compression",
                      "bursty traffic shape","network","CDN","failover headroom","regional placement"],
        "executed_benchmark":False,
        "source_reference":"https://github.com/donnemartin/system-design-primer"
    }


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--daily-requests", required=True)
    p.add_argument("--peak-factor", required=True)
    p.add_argument("--payload-bytes", required=True)
    p.add_argument("--retention-days", required=True)
    p.add_argument("--replica-rps", required=True)
    p.add_argument("--target-utilization", required=True)
    p.add_argument("--copies",default="1")
    a=p.parse_args()
    try:
        data=size_system(a.daily_requests,a.peak_factor,a.payload_bytes,
                         a.retention_days,a.replica_rps,a.target_utilization,a.copies)
        print(json.dumps(data,ensure_ascii=False,indent=2))
    except ValueError as exc:
        p.error(str(exc))


if __name__=="__main__":
    main()
