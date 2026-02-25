const { expect } = require("chai");

describe("DataStorage", function () {
  let dataStorage;

  beforeEach(async function () {
    const DataStorage = await ethers.getContractFactory("DataStorage");
    dataStorage = await DataStorage.deploy();
  });

  it("Should set and get data correctly", async function () {
    // Initial data should be empty
    expect(await dataStorage.getData()).to.equal("");

    // Set new data
    const tx = await dataStorage.setData("Hello Web3");
    await tx.wait();

    // Verify new data
    expect(await dataStorage.getData()).to.equal("Hello Web3");
  });

  it("Should emit DataStored event on setData", async function () {
    await expect(dataStorage.setData("Test Event"))
      .to.emit(dataStorage, "DataStored")
      .withArgs("Test Event");
  });
});
