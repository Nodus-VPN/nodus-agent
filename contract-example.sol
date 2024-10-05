// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CustomBalanceTopUp {

    // Структура для хранения информации о пользователе
    struct User {
        address userAddress;  // Адрес пользователя
        uint256 balance;      // Баланс пользователя
        uint256 blockNumber;  // Номер блока (может быть фиктивным)
    }

    // Массив для хранения всех адресов пользователей
    address[] private userList;

    // Маппинг для хранения данных о пользователях по их адресу
    mapping(address => User) public users;

    // Событие для уведомления о пополнении баланса
    event BalanceToppedUp(address indexed user, uint256 amount, uint256 customBlockNumber);

    // Функция для пополнения баланса указанного пользователя
    function topUpBalance(address _user, uint256 _amount, uint256 _blockNumber) public {
        // Если это новое пополнение для пользователя, добавляем его в массив
        if (users[_user].userAddress == address(0)) {
            userList.push(_user); // Сохраняем адрес нового пользователя
        }

        // Обновляем данные пользователя
        users[_user] = User({
            userAddress: _user,
            balance: users[_user].balance + _amount,  // Увеличиваем баланс на переданную сумму
            blockNumber: _blockNumber  // Записываем фиктивный номер блока
        });

        // Генерируем событие для отслеживания
        emit BalanceToppedUp(_user, _amount, _blockNumber);
    }

    // Функция для получения информации обо всех пользователях
    function getAllUserInfo() public view returns (address[] memory, uint256[] memory, uint256[] memory) {
        uint256 userCount = userList.length;

        address[] memory addresses = new address[](userCount);
        uint256[] memory balances = new uint256[](userCount);
        uint256[] memory blockNumbers = new uint256[](userCount);

        for (uint256 i = 0; i < userCount; i++) {
            address userAddress = userList[i];
            User memory userData = users[userAddress];

            addresses[i] = userData.userAddress;
            balances[i] = userData.balance;
            blockNumbers[i] = userData.blockNumber;
        }

        return (addresses, balances, blockNumbers);
    }

    // Функция для получения баланса контракта
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
    }

    // Функция для вывода средств (только для владельца контракта)
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function withdraw(uint256 amount) public onlyOwner {
        require(amount <= address(this).balance, "Insufficient balance");
        payable(owner).transfer(amount);
    }
}