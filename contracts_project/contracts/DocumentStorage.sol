// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DocumentStorage {
    struct Document {
        string documentId;
        string issuerId;
        string holderId;
        string hashedContent;
        bool isActive;
    }

    mapping(string => Document) private documents;

    event DocumentStored(
        string indexed documentId, 
        string issuerId, 
        string holderId, 
        string hashedContent, 
        bool isActive
    );

    // 1. store document data in blockchain
    function storeDocument(
        string memory _documentId, 
        string memory _issuerId,
        string memory _holderId,
        string memory _hashedContent,
        bool _isActive
    ) public {
        documents[_documentId] = Document({
            documentId: _documentId,
            issuerId: _issuerId,
            holderId: _holderId,
            hashedContent: _hashedContent,
            isActive: _isActive
        });

        emit DocumentStored(_documentId, _issuerId, _holderId, _hashedContent, _isActive);
    }

    // 2. read data in blockchain by document id
    function getDocument(string memory _documentId) public view returns (
        string memory documentId,
        string memory issuerId,
        string memory holderId,
        string memory hashedContent,
        bool isActive
    ) {
        Document memory doc = documents[_documentId];
        require(bytes(doc.documentId).length != 0, "Document not found.");
        return (
            doc.documentId,
            doc.issuerId,
            doc.holderId,
            doc.hashedContent,
            doc.isActive
        );
    }

    // 3. read data in blockchain by list of document ids
    function getDocuments(string[] memory _documentIds) public view returns (Document[] memory) {
        Document[] memory result = new Document[](_documentIds.length);
        
        for (uint i = 0; i < _documentIds.length; i++) {
            if (bytes(documents[_documentIds[i]].documentId).length != 0) {
                result[i] = documents[_documentIds[i]];
            } else {
                // Return an empty Document struct manually
                result[i] = Document({
                    documentId: "",
                    issuerId: "",
                    holderId: "",
                    hashedContent: "",
                    isActive: false
                });
            }
        }
        
        return result;
    }
}
