from agent import UniversalAdvocate

def main():
    advocate = UniversalAdvocate()

    print("--- Test Case 1: Travel (Delta Airlines) - Formal Request ---")
    result1 = advocate.run_agent(
        company="Delta Airlines", 
        amount=800.0, 
        issue="My flight was delayed by 5 hours.",
        user_name="John Doe",
        user_email="john.doe@example.com",
        user_address="123 Maple Street, Springfield, IL 62704",
        purchase_date="2025-11-15",
        ref_number="DL-987654321",
        payment_method="Visa ending in 1234"
    )
    print("\n[USER REPLY]:")
    print(result1['user_reply'])
    print("\n[LEGAL LETTER]:")
    print(result1['letter'])
    print("\n" + "="*30 + "\n")

    print("--- Test Case 2: Retail (Amazon) - Formal Request ---")
    result2 = advocate.run_agent(
        company="Amazon", 
        amount=100.0, 
        issue="The item I bought is defective.",
        user_name="Jane Smith",
        user_email="jane.smith@example.com",
        user_address="456 Oak Avenue, Metropolis, NY 10012",
        purchase_date="2025-11-20",
        ref_number="AMZ-11223344",
        payment_method="MasterCard ending in 5678"
    )
    print("\n[USER REPLY]:")
    print(result2['user_reply'])
    print("\n[LEGAL LETTER]:")
    print(result2['letter'])
    print("\n" + "="*30 + "\n")

if __name__ == "__main__":
    main()
