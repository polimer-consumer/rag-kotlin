## How to run

### Arguments

- `--query`: 
  - Question about the API.
  - **Type**: `str`
  - **Default**: "What does invoke do?"
  
- `--top_k`: 
  - Number of top contexts to retrieve from the index.
  - `int`
  - **Default**: 30

- `--index_path`: 
  - Path to the FAISS index file containing the data.
  - `str`
  - **Required**

### Example

To run the script and ask a specific question, you can use the following command:

```bash
python run_answer.py --query "What is ticker and how its behavior is controlled in Kotlin?" --top_k 50 --index_path data/faiss_index.index
```
