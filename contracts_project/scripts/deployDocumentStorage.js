const hre = require("hardhat");

async function main() {
  const DocumentStorage = await hre.ethers.getContractFactory("DocumentStorage");
  const documentStorage = await DocumentStorage.deploy();

  await documentStorage.waitForDeployment();
  const address = await documentStorage.getAddress();

  console.log(`DocumentStorage deployed to: ${address}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
