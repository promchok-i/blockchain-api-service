// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract DataStorage {
    string private data;

    event DataStored(string newData);

    // Write data to the blockchain
    function setData(string memory _data) public {
        data = _data;
        emit DataStored(_data);
    }

    // Read data from the blockchain
    function getData() public view returns (string memory) {
        return data;
    }
}
