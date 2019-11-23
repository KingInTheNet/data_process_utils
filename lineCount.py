def blocks(files, size=65536):
    while True:
        b = files.read(size)
        if not b: break
        yield b

with open("viwiki-latest-pages-articles-multistream.xml.bz2", "r",encoding="utf-8",errors='ignore') as f:
    print (sum(bl.count("\n") for bl in blocks(f)))
