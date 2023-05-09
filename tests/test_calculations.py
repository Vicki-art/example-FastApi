import pytest
from app.calculations import add, substract, multiply, divide, BankAccount, NoMoneyOnAccount

@pytest.mark.parametrize("num1, num2, expected", [
    (3, 6, 9), 
    (7, 9, 16), 
    (7, 0, 7)
])
def test_add(num1, num2, expected): 
    print("testing add function")
    assert add(num1, num2) == expected

#def test_add2():
    #assert add(5, "as") == 7

# def test_multiply():
    # assert multiply(3, 4) == 12

def test_divide():
    assert divide(20, 5) == 4

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)
    

def test_set_bank_account_value(bank_account): 
    assert bank_account.balance == 50

def test_set_bank_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_bank_deposit(bank_account):
    bank_account.withdraw(20)
    bank_account.deposit(10)
    assert bank_account.balance == 40

def test_bank_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (400, 300, 100), (700, 200, 500), (700, 600, 100)
])
def test_bank_account(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_not_enought_money(bank_account):
    with pytest.raises(NoMoneyOnAccount):
        bank_account.withdraw(200)








    