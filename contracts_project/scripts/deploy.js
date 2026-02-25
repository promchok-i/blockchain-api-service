const hre = require("hardhat");

async function main() {
  const DataStorage = await hre.ethers.getContractFactory("DataStorage");
  const dataStorage = await DataStorage.deploy();

  await dataStorage.waitForDeployment();
  const address = await dataStorage.getAddress();

  console.log(`DataStorage deployed to: ${address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
