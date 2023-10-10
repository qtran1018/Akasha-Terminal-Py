import tiktoken

def getTokenCount(query: str) -> int:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    #maybe don't need to assign to var, just return the length
    num_tokens = len(encoding.encode(query))

    print("Tokenizer, number of tokens: " + str(num_tokens))

    return num_tokens