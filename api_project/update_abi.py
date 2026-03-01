import json
import os

def update_abi():
    # Define paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    artifact_path = os.path.join(
        base_dir, 
        'contracts_project', 
        'artifacts', 
        'contracts', 
        'DocumentStorage.sol', 
        'DocumentStorage.json'
    )
    dest_path = os.path.join(
        base_dir, 
        'api_project', 
        'contract_abi.json'
    )

    try:
        # Load the compiled contract artifact
        with open(artifact_path, 'r') as f:
            artifact = json.load(f)
        
        # Extract the ABI and write it to the API directory
        with open(dest_path, 'w') as f:
            json.dump(artifact['abi'], f, indent=2)

        print(f"Successfully updated ABI in: {dest_path}")
    except FileNotFoundError:
        print(f"Error: Could not find artifact at {artifact_path}.")
        print("Make sure you have compiled the smart contract using Hardhat first.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_abi()
