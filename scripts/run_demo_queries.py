import requests


def main():
    queries = [
        "What is GraphRAG and why is graph expansion useful?",
        "How are images used in the retrieval pipeline?",
        "What happens before second-hop graph retrieval?",
    ]
    for q in queries:
        resp = requests.post(
            "http://localhost:8000/query",
            json={
                "question": q,
                "top_k_text": 5,
                "top_k_image": 2,
                "graph_hops": 1,
                "use_multimodal": True,
            },
            timeout=60,
        )
        print("QUESTION:", q)
        print(resp.json())
        print("-" * 80)


if __name__ == "__main__":
    main()
