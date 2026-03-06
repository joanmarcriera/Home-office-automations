#!/usr/bin/env python3
"""Validate data/model-account-pool.json routing and account policy."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ALLOWED_OWNER_SCOPES = {"work", "personal", "household"}
ALLOWED_TIERS = {"free", "paid"}
ENV_NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


def fail(errors: list[str]) -> int:
    print("Model account policy validation failed:\n")
    for err in errors:
        print(f"- {err}")
    return 1


def load_policy(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Policy root must be an object.")
    return data


def validate(policy: dict) -> list[str]:
    errors: list[str] = []

    required_top = {
        "version",
        "last_updated",
        "defaults",
        "providers",
        "accounts",
        "routing_profiles",
        "rotation",
        "guardrails",
    }
    missing_top = sorted(required_top - set(policy.keys()))
    if missing_top:
        errors.append(f"Missing top-level keys: {', '.join(missing_top)}")
        return errors

    if not isinstance(policy["version"], int) or policy["version"] < 1:
        errors.append("`version` must be an integer >= 1.")

    try:
        dt.date.fromisoformat(str(policy["last_updated"]))
    except ValueError:
        errors.append("`last_updated` must be ISO date YYYY-MM-DD.")

    providers = policy["providers"]
    accounts = policy["accounts"]
    routing_profiles = policy["routing_profiles"]
    rotation = policy["rotation"]
    guardrails = policy["guardrails"]

    if not isinstance(providers, list) or not providers:
        errors.append("`providers` must be a non-empty list.")
        return errors
    if not isinstance(accounts, list) or not accounts:
        errors.append("`accounts` must be a non-empty list.")
        return errors
    if not isinstance(routing_profiles, dict) or not routing_profiles:
        errors.append("`routing_profiles` must be a non-empty mapping.")
        return errors

    provider_ids: set[str] = set()
    for idx, provider in enumerate(providers):
        if not isinstance(provider, dict):
            errors.append(f"providers[{idx}] must be a mapping.")
            continue
        pid = provider.get("id")
        if not isinstance(pid, str) or not pid:
            errors.append(f"providers[{idx}].id must be a non-empty string.")
            continue
        if pid in provider_ids:
            errors.append(f"Duplicate provider id: {pid}")
        provider_ids.add(pid)

    account_ids: set[str] = set()
    account_by_id: dict[str, dict] = {}
    for idx, account in enumerate(accounts):
        if not isinstance(account, dict):
            errors.append(f"accounts[{idx}] must be a mapping.")
            continue
        aid = account.get("id")
        if not isinstance(aid, str) or not aid:
            errors.append(f"accounts[{idx}].id must be a non-empty string.")
            continue
        if "@" in aid:
            errors.append(f"accounts[{idx}].id must not contain '@' (avoid personal identifiers).")
        if aid in account_ids:
            errors.append(f"Duplicate account id: {aid}")
        account_ids.add(aid)
        account_by_id[aid] = account

        provider = account.get("provider")
        if provider not in provider_ids:
            errors.append(f"accounts[{idx}] provider `{provider}` not found in providers list.")

        owner_scope = account.get("owner_scope")
        if owner_scope not in ALLOWED_OWNER_SCOPES:
            errors.append(
                f"accounts[{idx}].owner_scope must be one of {sorted(ALLOWED_OWNER_SCOPES)}."
            )

        tier = account.get("tier")
        if tier not in ALLOWED_TIERS:
            errors.append(f"accounts[{idx}].tier must be one of {sorted(ALLOWED_TIERS)}.")

        cred_env = account.get("credential_env")
        if not isinstance(cred_env, str) or not ENV_NAME_RE.match(cred_env):
            errors.append(f"accounts[{idx}].credential_env must be an uppercase env-var name.")

        if not isinstance(account.get("enabled"), bool):
            errors.append(f"accounts[{idx}].enabled must be boolean.")

    for profile_name, profile in routing_profiles.items():
        if not isinstance(profile, dict):
            errors.append(f"routing_profiles.{profile_name} must be a mapping.")
            continue
        routes = profile.get("routes")
        if not isinstance(routes, list) or not routes:
            errors.append(f"routing_profiles.{profile_name}.routes must be a non-empty list.")
            continue

        total_weight = 0
        profile_has_free = False
        for ridx, route in enumerate(routes):
            if not isinstance(route, dict):
                errors.append(f"routing_profiles.{profile_name}.routes[{ridx}] must be a mapping.")
                continue
            provider = route.get("provider")
            if provider not in provider_ids:
                errors.append(
                    f"routing_profiles.{profile_name}.routes[{ridx}] provider `{provider}` is unknown."
                )

            weight = route.get("weight")
            if not isinstance(weight, int) or weight <= 0:
                errors.append(
                    f"routing_profiles.{profile_name}.routes[{ridx}].weight must be positive integer."
                )
            else:
                total_weight += weight

            pool = route.get("account_pool")
            if not isinstance(pool, list) or not pool:
                errors.append(
                    f"routing_profiles.{profile_name}.routes[{ridx}].account_pool must be non-empty list."
                )
                continue

            for aid in pool:
                if aid not in account_by_id:
                    errors.append(
                        f"routing_profiles.{profile_name}.routes[{ridx}] references unknown account `{aid}`."
                    )
                    continue
                account = account_by_id[aid]
                if account.get("provider") != provider:
                    errors.append(
                        f"routing_profiles.{profile_name}.routes[{ridx}] account `{aid}` provider mismatch."
                    )
                if account.get("tier") == "free":
                    profile_has_free = True

            models = route.get("model_preferences")
            if not isinstance(models, list) or not models or not all(
                isinstance(m, str) and m.strip() for m in models
            ):
                errors.append(
                    f"routing_profiles.{profile_name}.routes[{ridx}].model_preferences must be non-empty list of strings."
                )

        if total_weight != 100:
            errors.append(
                f"routing_profiles.{profile_name} route weights must sum to 100 (found {total_weight})."
            )
        if not profile_has_free:
            errors.append(
                f"routing_profiles.{profile_name} must include at least one free-tier account route."
            )

    if not isinstance(rotation, dict):
        errors.append("`rotation` must be a mapping.")
    else:
        pools = rotation.get("provider_pools")
        if not isinstance(pools, dict) or not pools:
            errors.append("rotation.provider_pools must be a non-empty mapping.")
        else:
            for provider, cfg in pools.items():
                if provider not in provider_ids:
                    errors.append(f"rotation.provider_pools contains unknown provider `{provider}`.")
                    continue
                if not isinstance(cfg, dict):
                    errors.append(f"rotation.provider_pools.{provider} must be a mapping.")
                    continue
                order = cfg.get("order")
                if not isinstance(order, list) or not order:
                    errors.append(f"rotation.provider_pools.{provider}.order must be non-empty list.")
                    continue
                for aid in order:
                    if aid not in account_by_id:
                        errors.append(
                            f"rotation.provider_pools.{provider}.order references unknown account `{aid}`."
                        )
                        continue
                    if account_by_id[aid].get("provider") != provider:
                        errors.append(
                            f"rotation.provider_pools.{provider}.order account `{aid}` provider mismatch."
                        )

    if not isinstance(guardrails, dict):
        errors.append("`guardrails` must be a mapping.")
    else:
        spend = guardrails.get("max_total_daily_spend_usd")
        if not isinstance(spend, (int, float)) or spend < 0:
            errors.append("guardrails.max_total_daily_spend_usd must be a non-negative number.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate model account routing policy JSON.")
    parser.add_argument(
        "policy_path",
        nargs="?",
        default="data/model-account-pool.json",
        help="Path to policy JSON file.",
    )
    args = parser.parse_args()

    path = Path(args.policy_path)
    if not path.exists():
        print(f"Policy file not found: {path}")
        return 1

    try:
        policy = load_policy(path)
    except Exception as exc:
        print(f"Failed to load JSON policy: {exc}")
        return 1

    errors = validate(policy)
    if errors:
        return fail(errors)

    account_count = len(policy.get("accounts", []))
    profile_count = len(policy.get("routing_profiles", {}))
    print(
        f"Model account policy validation passed ({account_count} account(s), "
        f"{profile_count} routing profile(s))."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
