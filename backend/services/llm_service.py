import ollama

#AI conversation history saved as an array
conversation_history = []

def ask_llm(question: str, mode:str):

    system_prompt = ""

    #Using if else logic to select system prompt based on the given mode, may change some of the modes later

    if mode == "study":  
        system_prompt = (
            "You are a study assistant. "
            "Explain concepts clearly with examples."
        )
    elif mode == "quiz":
        system_prompt = (
            "You are a quiz generator. "
            "Create practice questions for students."
        )
    elif mode == "simplify":
        system_prompt = (
            "You simplify difficult concepts for beginners."
        )

    else:
        system_prompt = (
            "You are a helpful academic assistant."
        )

    #adding the user question to conversation history
    conversation_history.append({
        "role": "user",
        "content": question
    })

    response = ollama.chat(
        model='llama3',
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            *conversation_history #sending conversation history to the chatbot
        ]
    )

    ai_message = response['message']['content']
    
    #Adding the AI response to the convseration history as well
    conversation_history.append({
        "role": "assistant",
        "content": ai_message
    })

    return ai_message