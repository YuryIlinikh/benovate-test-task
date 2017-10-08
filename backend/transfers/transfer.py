import random

from decimal import Decimal

from transfers.models import Transfer, Profile


class TransferException(Exception):
    """
    If something happened during transfering
    """
    pass


class TransferService:
    """
    Маке transfer bl class
    """
    @staticmethod
    def _check_user_balance(user_profile, send_amount):
        if user_profile.bill - send_amount < 0:
            raise TransferException('User has not enough money')

    @staticmethod
    def _load_from_profile(transfer):
        try:
            return transfer.load_from_profile()
        except Profile.DoesNotExist:
            raise TransferException('User not found')

    @staticmethod
    def _load_inn_profiles(transfer):
        inn_profiles = transfer.load_inn_profiles()
        if not inn_profiles:
            raise TransferException('Users with this INN not found')
        return inn_profiles

    @staticmethod
    def _get_lucky_inn_profile(inn_profiles):
        return random.choice(inn_profiles)

    def _apply_transfer(self, from_profile: Profile, inn_profiles, amount: Decimal):
        if not inn_profiles:
            return
        from_profile.bill -= amount
        inn_profiles_count = len(inn_profiles)
        part100 = amount * 100 // inn_profiles_count
        part = part100 / 100
        modulo = amount - part * inn_profiles_count
        for inn_profile in inn_profiles:
            if from_profile.id == inn_profile.id :
                inn_profile.bill -= amount
            inn_profile.bill += part
        if modulo:
            lucky_profile = self._get_lucky_inn_profile(inn_profiles)
            lucky_profile.bill += modulo

    @staticmethod
    def _get_transfer_model(validated_data):
        return Transfer(**validated_data)

    def make_transfer(self, validated_data):
        transfer = self._get_transfer_model(validated_data)
        # load models
        from_profile = self._load_from_profile(transfer)
        self._check_user_balance(from_profile, transfer.amount)
        inn_profiles = self._load_inn_profiles(transfer)
        self._apply_transfer(from_profile, inn_profiles, transfer.amount)
        transfer.save(from_profile, inn_profiles)
        return from_profile, inn_profiles

