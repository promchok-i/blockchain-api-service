require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config({ path: require('path').resolve(__dirname, '../.env') });

const privateKey = process.env.PRIVATE_KEY || "";
const accounts = privateKey.length >= 64 ? [privateKey.startsWith("0x") ? privateKey : "0x" + privateKey] : [];

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  networks: {
    sepolia: {
      url: process.env.ALCHEMY_URL || "",
      accounts: accounts,
    },
  },
};
