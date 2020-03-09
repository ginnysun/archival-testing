from rake_nltk import Rake

r = Rake(language='portuguese')  # Uses stopwords for english from NLTK, and all punctuation characters.

sample_1_txt = open("sample_1/out_text.txt", "r")
text = sample_1_txt.read()
sample_1_txt.close()
print(text)
r.extract_keywords_from_text(text)

print(r.get_ranked_phrases())  # To get keyword phrases ranked highest to lowest.

