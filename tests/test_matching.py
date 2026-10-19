import unittest
from demo.matching import Address, Account, match_account, choose_service_category


class MatchingTests(unittest.TestCase):
    def setUp(self):
        self.accounts = [
            Account("D-001", Address("ул. Лесная", "48А", flat="1")),
            Account("D-002", Address("Лесная", "48 А", flat="")),
            Account("D-003", Address("Лесная", "48 А", flat="2")),
        ]

    def test_normalized_street_house_and_flat(self):
        self.assertEqual(match_account(Address("улица ЛЕСНАЯ", "48 А", flat="Кв.1"), self.accounts).code, "D-001")

    def test_without_flat_does_not_select_some_apartment(self):
        self.assertEqual(match_account(Address("Лесная", "48А"), self.accounts).code, "D-002")

    def test_missing(self):
        self.assertEqual(match_account(Address("Лесная", "48А", flat="7"), self.accounts).status, "missing")

    def test_ambiguous(self):
        all_accounts = self.accounts + [Account("D-004", Address("Лесная", "48А", flat="1"))]
        result = match_account(Address("Лесная", "48А", flat="1"), all_accounts)
        self.assertEqual((result.status, result.candidates), ("ambiguous", ("D-001", "D-004")))

    def test_manual_overrides_default_and_can_be_changed(self):
        defaults = {"Холодное водоснабжение": "CATEGORY-A"}
        manual = {"Холодное водоснабжение": "Не выгружать"}
        self.assertEqual(choose_service_category("ХОЛОДНОЕ водоснабжение", manual, defaults), "Не выгружать")
        manual["Холодное водоснабжение"] = "CATEGORY-B"
        self.assertEqual(choose_service_category("Холодное водоснабжение", manual, defaults), "CATEGORY-B")


if __name__ == "__main__":
    unittest.main()
