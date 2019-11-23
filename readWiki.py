from wiki_dump_reader import Cleaner, iterate

cleaner = Cleaner()
count =0
f = open('dumbfuck.txt','w')
for title, text in iterate('viwiki-latest-pages-articles-multistream.xml'):
    text = cleaner.clean_text(text)
    cleaned_text, links = cleaner.build_links(text)
    #print(cleaned_text)
    f.write(cleaned_text)
    count+=1
    if count>10:
        break
