from decimal import Decimal
from django.test import TestCase
from mock.mock import MagicMock, patch

from transfers.models import Profile, Transfer
from transfers.transfer import TransferService, TransferException


class TransferServiceTestCase(TestCase):
    def setUp(self):
        pass

    def _assert__check_user_balance_rase(self, bill, amount):
        service = TransferService()
        user_profile = Profile(bill=bill)
        with self.assertRaises(TransferException, msg='Exception not raised :(') as cm:
            service._check_user_balance(user_profile, amount)
        self.assertEquals('User has not enough money', str(cm.exception))

    def test__check_user_balance_should_raise_exception_if_not_enough_money(self):
        self._assert__check_user_balance_rase(9, 10)

    def test__check_user_balance_should_raise_exception_if_bill_negative(self):
        self._assert__check_user_balance_rase(-1, 0)

    def test__check_user_balance_should_raise_exception_if_not_enough_money_and_zero_bill(self):
        self._assert__check_user_balance_rase(0, 0.01)

    def _assert__check_user_balance_not_rase(self, bill, amount):
        service = TransferService()
        user_profile = Profile(bill=bill)
        try:
            service._check_user_balance(user_profile, amount)
        except TransferException as e:
            self.fail("_check_user_balance() raised {} {} unexpectedly!".format(type(e), str(e)))

    def test__check_user_balance_should_not_raise_exception_if_enough_money(self):
        self._assert__check_user_balance_not_rase(10, 2)

    def test__check_user_balance_should_not_raise_exception_if_sums_equal(self):
        self._assert__check_user_balance_not_rase(0.01, 0.01)

    def test__check_user_balance_should_not_raise_exception_if_zero_bill_and_amount(self):
        self._assert__check_user_balance_not_rase(0, 0)

    def _assert__apply_transfer(self, exp_from_bill: Decimal, from_bill: Decimal, exp_bills: [], inn_bills: [],
                                amount: Decimal, exp_modulo: bool, from_profile_id=100500):
        service = TransferService()

        user_profile = Profile(bill=from_bill, id=from_profile_id)
        inn_profiles = [Profile(bill=bill, id=i+1) for i, bill in enumerate(inn_bills)]

        service._get_lucky_inn_profile = MagicMock(return_value=inn_profiles[1] if inn_profiles else [])
        service._apply_transfer(user_profile, inn_profiles, amount)

        if exp_modulo:
            service._get_lucky_inn_profile.assert_called_with(inn_profiles)
        else:
            service._get_lucky_inn_profile.assert_not_called()

        self.assertEquals(exp_from_bill, user_profile.bill)
        res_inn_bills = [inn_profile.bill for inn_profile in inn_profiles]
        self.assertEquals(exp_bills, res_inn_bills)

    def test__apply_transfer_should_devide_amount_between_inn_profiles_equal_parts(self):
        exp_from_bill = Decimal(3)
        from_bill = Decimal(12)
        exp_bills = [Decimal(4), Decimal(5), Decimal(6)]
        inn_bills = [Decimal(1), Decimal(2), Decimal(3)]
        amount = Decimal(9)
        exp_modulo = False
        self._assert__apply_transfer(exp_from_bill, from_bill, exp_bills, inn_bills, amount, exp_modulo)

    def test__apply_transfer_should_devide_amount_between_inn_profiles_equal_parts_and_modulo_to_luky(self):
        exp_from_bill = Decimal(2)
        from_bill = Decimal(12)
        exp_bills = [Decimal('4.33'), Decimal('5.34'), Decimal('6.33')]
        inn_bills = [Decimal(1), Decimal(2), Decimal(3)]
        amount = Decimal(10)
        exp_modulo = True
        self._assert__apply_transfer(exp_from_bill, from_bill, exp_bills, inn_bills, amount, exp_modulo)

    def test__apply_transfer_should_not_do_anything_with_zero_amount(self):
        exp_from_bill = Decimal(12)
        from_bill = Decimal(12)
        exp_bills = [Decimal('1'), Decimal('2'), Decimal('3')]
        inn_bills = [Decimal(1), Decimal(2), Decimal(3)]
        amount = Decimal(0)
        exp_modulo = False
        self._assert__apply_transfer(exp_from_bill, from_bill, exp_bills, inn_bills, amount, exp_modulo)

    def test__apply_transfer_should_not_do_anything_with_empty_inn_profiles(self):
        exp_from_bill = Decimal(12)
        from_bill = Decimal(12)
        exp_bills = []
        inn_bills = []
        amount = Decimal(0)
        exp_modulo = False
        self._assert__apply_transfer(exp_from_bill, from_bill, exp_bills, inn_bills, amount, exp_modulo)

    def test__apply_transfer_should_not_duplicate_bill_to_self(self):
        exp_from_bill = Decimal(3)
        from_bill = Decimal(12)
        from_bill_id = 2
        exp_bills = [Decimal(4), Decimal(6), Decimal(6)]
        inn_bills = [Decimal(1), Decimal(12), Decimal(3)]
        amount = Decimal(9)
        exp_modulo = False
        self._assert__apply_transfer(exp_from_bill, from_bill, exp_bills, inn_bills, amount, exp_modulo, from_bill_id)

    def test_make_transfer(self):
        validated_data = {'from_user_id': 1, 'to_inn': '123', 'amount': Decimal(10)}
        transfer = Transfer(**validated_data)
        from_profile = Profile(id=1, user_id=1, bill=15)
        inn_bills = [Decimal(1), Decimal(2), Decimal(3)]
        inn_profiles = [Profile(bill=bill, id=i + 1) for i, bill in enumerate(inn_bills)]

        service = TransferService()
        service._get_transfer_model = MagicMock(return_value=transfer)
        service._load_from_profile = MagicMock(return_value=from_profile)
        service._check_user_balance = MagicMock(return_value=None)
        service._load_inn_profiles = MagicMock(return_value=inn_profiles)
        service._apply_transfer = MagicMock(return_value=None)
        transfer.save = MagicMock(return_value=None)

        service.make_transfer(validated_data)

        service._get_transfer_model.assert_called_with(validated_data)
        service._load_from_profile.assert_called_with(transfer)
        service._check_user_balance.assert_called_with(from_profile, transfer.amount)
        service._load_inn_profiles.assert_called_with(transfer)
        service._apply_transfer.assert_called_with(from_profile, inn_profiles, transfer.amount)
        transfer.save.assert_called_with(from_profile, inn_profiles)

