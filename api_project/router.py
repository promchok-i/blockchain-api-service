from fastapi import APIRouter, HTTPException
from schemas import DocumentInput, DocumentQueryInput
from constants import PRIVATE_KEY, w3, contract

router = APIRouter()


@router.post("/document")
async def create_document(payload: DocumentInput):
    if not contract or not w3:
        raise HTTPException(status_code=500, detail="Web3/Contract not initialized")
    if not PRIVATE_KEY:
        raise HTTPException(status_code=500, detail="Private key missing")

    try:
        account = w3.eth.account.from_key(PRIVATE_KEY)
        nonce = w3.eth.get_transaction_count(account.address)

        tx = contract.functions.storeDocument(
            payload.document_id,
            payload.issuer_id,
            payload.holder_id,
            payload.hashed_content,
            payload.is_active
        ).build_transaction({
            'chainId': w3.eth.chain_id,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
        })

        # Estimate gas manually or rely on build_transaction's auto-estimate depending on provider
        gas_estimate = contract.functions.storeDocument(
            payload.document_id,
            payload.issuer_id,
            payload.holder_id,
            payload.hashed_content,
            payload.is_active
        ).estimate_gas({'from': account.address})

        tx['gas'] = gas_estimate

        signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)

        return {
            "message": "Document created successfully",
            "transaction_hash": w3.to_hex(tx_hash),
            "status": tx_receipt.status,
            "data": payload,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/document/{document_id}")
async def get_document(document_id: str):
    if not contract:
        raise HTTPException(status_code=500, detail="Web3/Contract not initialized")

    try:
        result = contract.functions.getDocument(document_id).call()
        doc_id, iss_id, holder_id, hash_content, is_active = result
        
        return {
            "message": "Document retrieved successfully",
            "data": {
                "document_id": doc_id,
                "issuer_id": iss_id,
                "holder_id": holder_id,
                "hashed_content": hash_content,
                "is_active": is_active
            }
        }
    except Exception as e:
        if "Document not found" in str(e):
            raise HTTPException(status_code=404, detail="Document not found")
        raise HTTPException(status_code=500, detail=f"Failed to fetch: {str(e)}")

@router.post("/documents/query")
async def get_documents_by_ids(query: DocumentQueryInput):
    if not contract:
        raise HTTPException(status_code=500, detail="Web3/Contract not initialized")

    try:
        results = contract.functions.getDocuments(query.document_ids).call()
        
        documents = []
        for result in results:
            doc_id, iss_id, holder_id, hash_content, is_active = result
            
            # Check if valid document
            if len(doc_id) > 0:
                documents.append({
                    "document_id": doc_id,
                    "issuer_id": iss_id,
                    "holder_id": holder_id,
                    "hashed_content": hash_content,
                    "is_active": is_active
                })
        
        return {
            "message": "Documents retrieved successfully",
            "documents": documents
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")
