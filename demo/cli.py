"""Run with: python -m demo.cli"""
from .matching import Address, Account, match_account, choose_service_category


def main():
    accounts = [
        Account("DEMO-001", Address("улица Лесная", "48А", flat="1")),
        Account("DEMO-002", Address("Лесная", "48 А", flat="")),
    ]
    for source in (Address("ул. Лесная", "48А", flat="Кв. 1"),
                   Address("ул Лесная", "48А"),
                   Address("Лесная", "48А", flat="99")):
        print(f"{source!r} -> {match_account(source, accounts)}")
    print("Manual service rule:", choose_service_category("Пени", {"Пени": "Не выгружать"}, {}))


if __name__ == "__main__":
    main()
