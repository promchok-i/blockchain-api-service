const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DocumentStorage", function () {
  let DocumentStorage;
  let documentStorage;
  let owner;

  beforeEach(async function () {
    DocumentStorage = await ethers.getContractFactory("DocumentStorage");
    [owner] = await ethers.getSigners();
    documentStorage = await DocumentStorage.deploy();
    await documentStorage.waitForDeployment();
  });

  describe("storeDocument", function () {
    it("Should store a new document successfully", async function () {
      const tx = await documentStorage.storeDocument(
        "doc123",
        "issuer1",
        "holderXYZ",
        "0xabc123hash",
        true
      );
      await tx.wait();

      const doc = await documentStorage.getDocument("doc123");
      expect(doc.documentId).to.equal("doc123");
      expect(doc.issuerId).to.equal("issuer1");
      expect(doc.holderId).to.equal("holderXYZ");
      expect(doc.hashedContent).to.equal("0xabc123hash");
      expect(doc.isActive).to.equal(true);
    });

    it("Should emit DocumentStored event on creation", async function () {
      await expect(
        documentStorage.storeDocument(
          "doc123",
          "issuer1",
          "holderXYZ",
          "0xabc123hash",
          true
        )
      )
        .to.emit(documentStorage, "DocumentStored")
        .withArgs("doc123", "issuer1", "holderXYZ", "0xabc123hash", true);
    });

    it("Should overwrite if document ID already exists", async function () {
      await documentStorage.storeDocument(
        "doc123",
        "issuer1",
        "holderXYZ",
        "0xabc123hash",
        true
      );

      await documentStorage.storeDocument(
        "doc123",
        "issuer2",
        "holderXYZ",
        "0xabc123hash",
        false
      );

      const doc = await documentStorage.getDocument("doc123");
      expect(doc.issuerId).to.equal("issuer2");
      expect(doc.isActive).to.equal(false);
    });
  });

  describe("getDocument", function () {
    it("Should retrieve an existing document", async function () {
      await documentStorage.storeDocument(
        "doc123",
        "issuer1",
        "holderXYZ",
        "0xabc123hash",
        true
      );

      const doc = await documentStorage.getDocument("doc123");
      expect(doc.documentId).to.equal("doc123");
    });

    it("Should fail if the document does not exist", async function () {
      await expect(documentStorage.getDocument("missingDoc")).to.be.revertedWith(
        "Document not found."
      );
    });
  });

  describe("getDocuments", function () {
    it("Should return a list of requested documents", async function () {
      await documentStorage.storeDocument("doc1", "iss1", "holder1", "hash1", true);
      await documentStorage.storeDocument("doc2", "iss2", "holder2", "hash2", false);

      const docs = await documentStorage.getDocuments(["doc1", "doc2", "doc3"]);

      expect(docs.length).to.equal(3);

      expect(docs[0].documentId).to.equal("doc1");
      expect(docs[0].issuerId).to.equal("iss1");
      expect(docs[0].isActive).to.equal(true);

      expect(docs[1].documentId).to.equal("doc2");
      expect(docs[1].issuerId).to.equal("iss2");
      expect(docs[1].isActive).to.equal(false);

      // doc3 was not stored, so the documentId string will be empty
      expect(docs[2].documentId).to.equal("");
      expect(docs[2].issuerId).to.equal("");
    });
  });
});
