import wikipedia

wikipedia.set_lang("vi")
results=wikipedia.summary("Donald Trump", 3)
#for result in results:
#    print(result)
print(results)
