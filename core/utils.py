# Description: Utility functions for the core app
def generate_answer_util(user_input, system_message, delimiter, generation_model, related_docs, client):
    documents = [doc.document for doc in related_docs] if related_docs != None else [""]
    content = "\n".join(documents)
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
        {"role": "assistant",
         "content": f"Relevant information: \n {content} \n"}
    ]
    response = client.chat.completions.create(
        model=generation_model,
        messages=messages
    )

    return response.choices[0].message.content