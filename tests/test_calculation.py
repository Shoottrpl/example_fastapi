import pytest
from app.calculation import add, subtract, multiply, divide, BankAccount, InsufficientBalance


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(10)


@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (1, 7, 8),
    (12, 4, 16)
])
def test_add(num1, num2, result):
    print("Test start")
    assert add(num1, num2) == result


def test_subtract():
    assert subtract(5, 3) == 2


def test_multiply():
    assert multiply(5, 3) == 15


def test_divide():
    assert divide(6, 3) == 2


def test_bank_set_initial_amout(bank_account):
    assert bank_account.balance == 10


def test_bank_default_amout(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    bank_account.withdraw(5)
    assert bank_account.balance == 5


def test_deposit(bank_account):
    bank_account.deposit(5)
    assert bank_account.balance == 15


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert bank_account.balance == 11


@pytest.mark.parametrize("deposit, withdraw, result", [
    (200, 100, 100),
    (250, 125, 125),
    (300, 124, 176)
])
def test_bank_transaction(zero_bank_account, deposit, withdraw, result):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == result


def test_insufficient_balance(bank_account):
    with pytest.raises(InsufficientBalance):
        bank_account.withdraw(15)







