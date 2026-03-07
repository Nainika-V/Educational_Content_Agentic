from core.engine import process_document, create_tutor_agent, run_agent_query
import os

if __name__ == "__main__":
    file_path = "how to install and where.txt"
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
    else:
        print("Processing document...")
        vector_db = process_document(file_path)
        
        print("Creating tutor agent...")
        agent_executor = create_tutor_agent(vector_db)
        
        chat_history = []
        
        while True:
            query = input("\nAsk a question about the document (or 'exit' to quit): ")
            if query.lower() == 'exit':
                break
                
            print("\nThinking...")
            answer = run_agent_query(agent_executor, query, chat_history)
            
            print("\n" + "="*20 + " ANSWER " + "="*20 + "\n")
            print(answer)
            
            chat_history.extend([
                ("human", query),
                ("ai", answer)
            ])
