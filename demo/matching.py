"""Independent illustrative address and service-mapping algorithms.

No DBF reader, private 1C code, or real customer data is included.
"""
from dataclasses import dataclass
import re
import unicodedata


def compact(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).upper().replace("Ё", "Е")
    return re.sub(r"[^0-9A-ZА-Я]", "", text)


def street_key(value: str) -> str:
    text = unicodedata.normalize("NFKC", (value or "")).upper().replace("Ё", "Е")
    text = re.sub(r"\b(УЛИЦА|УЛ|ПРОСПЕКТ|ПР-Т)\b\.?", "", text)
    return compact(text)


def flat_key(value: object) -> str:
    text = str(value or "").strip()
    if not text:
        return ""  # A whole-building account, NOT an unspecified apartment.
    text = re.sub(r"(?i)^\s*(КВАРТИРА|КВ)\s*\.?\s*", "", text)
    return compact(text)


@dataclass(frozen=True)
class Address:
    street: str
    house: str
    building: str = ""
    flat: str = ""

    def key(self) -> tuple[str, str, str, str]:
        return (street_key(self.street), compact(self.house), compact(self.building), flat_key(self.flat))


@dataclass(frozen=True)
class Account:
    code: str
    address: Address


@dataclass(frozen=True)
class Lookup:
    status: str  # found | missing | ambiguous
    code: str | None = None
    candidates: tuple[str, ...] = ()


def match_account(source: Address, accounts: list[Account]) -> Lookup:
    matched = sorted({a.code for a in accounts if a.address.key() == source.key()})
    if len(matched) == 1:
        return Lookup("found", matched[0], tuple(matched))
    if not matched:
        return Lookup("missing")
    return Lookup("ambiguous", candidates=tuple(matched))


def choose_service_category(service: str, manual: dict[str, str], defaults: dict[str, str]) -> str | None:
    """Manual mapping (including 'Не выгружать') always overrides a default."""
    key = compact(service)
    normalized_manual = {compact(k): v for k, v in manual.items()}
    normalized_defaults = {compact(k): v for k, v in defaults.items()}
    return normalized_manual.get(key, normalized_defaults.get(key))
