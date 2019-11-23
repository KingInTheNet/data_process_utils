import bz2
import csv
import re
import sys
import time
from datetime import timedelta
from functools import partial
from xml.etree import ElementTree
import pandas
import click

PAGES_CSV_FILENAME = "pages.csv"
LINKS_CSV_FILENAME = "links.csv"
PROGRESS_N = 100

LINK_RE = re.compile(r"\[\[(?:[^|\]]*\|)?([^\]]+)\]\]")


def strip_tag_name(element):
    t = element.tag
    idx = t.rfind("}")
    return t[idx + 1 :] if idx != -1 else t


def parse_links(text):
    links = set()
    for m in LINK_RE.finditer(text):
        link_text = m.group(1)
        if ":" not in link_text:
            links.add(link_text.strip())
    return links

def get_info():
    print(0)

def parse_pages(wiki_xml_f, pages_f, links_f):
    """
    Parse Wikipedia XML dump into two files:
        - `pages_fp`: Neo4j Node import CSV ["title:ID", "id"]
        - `links_fp`: Intermediary CSV of links [":START_ID", "END_TITLE"]
    """
    pages_writer = csv.writer(pages_f)
    links_writer = csv.writer(links_f)
    pages_writer.writerow(["title:ID", "id"])
    links_writer.writerow([":START_ID", ":END_ID"])
    f = open("dumbass.txt","w")

    page_count = link_count = 0

    title = ""
    _id = -1
    links = set()
    in_revision = False
    
    for event, element in ElementTree.iterparse(wiki_xml_f, events=("start", "end")):
        tname = strip_tag_name(element)
        #print(tname)
        print(element.find('leader'))
        if event == "start":
            if tname == "page":
                #print(element.text)
                title = ""
                _id = -1
                in_revision = False
                links = set()
            if tname == "revision":
                #print(element.text)
                in_revision = True
        else:
            if tname == "title":
                title = element.text.strip()
                #print(element.text.strip())
            elif tname == "id" and not in_revision:
                _id = element.text
            elif tname == "text":
                if element.text:
                    f.write(element.text)
                    f.write("\n")
                    links = parse_links(element.text)
                    link_count += len(links)
            elif tname == "page":
                pages_writer.writerow([title, _id])
                links_writer.writerows([title, l] for l in links if l != title)
                page_count += 1

                if page_count > 1 and page_count % PROGRESS_N == 0:
                    print(f"Pages processed: {page_count}")
                    print(f"Links found: {link_count}")
                    break
                if page_count>100:
                    break
                element.clear()
    return page_count, link_count


def is_bz2(filename):
    try:
        with bz2.BZ2File(filename, "r") as f:
            f.read(1)
            return True
    except OSError:
        pass
    return False


@click.command()
@click.argument(
    "wiki-xml-infile", required=False, default=sys.stdin, type=click.Path(exists=True)
)
@click.option(
    "-p",
    "--pages-outfile",
    default=PAGES_CSV_FILENAME,
    type=click.File(mode="w"),
    help="Node (Pages) CSV output file",
    show_default=True,
)
# @click.option(
#     "-l",
#     "--links-outfile",
#     default=LINKS_CSV_FILENAME,
#     type=click.File(mode="w"),
#     help="Relationships (Links) CSV output file",
#     show_default=True,
# )
def main(wiki_xml_infile, pages_outfile, links_outfile):
    """
    Parse Wikipedia pages-articles-multistream.xml[.bz2] dump into two Neo4j import CSV files:
        Node (Page) import, headers=["title:ID", "id"]
        Relationships (Links) import, headers=[":START_ID", ":END_ID"]
    Reads from stdin by default, pass [WIKI_XML_INFILE] to read from file.
    """

    _open = partial(bz2.open, mode="rt") if is_bz2(wiki_xml_infile) else open

    start = time.time()
    with _open(wiki_xml_infile) as f:
        page_count, link_count = parse_pages(f, pages_outfile, links_outfile)
    end = time.time()

    click.secho(f"Processing complete", fg="green")
    click.echo(f"Time: {timedelta(seconds=end - start)}")
    click.echo(
        f"Pages: {click.style(str(page_count), fg='red')} -> {pages_outfile.name}"
    )
    click.echo(
        f"Links: {click.style(str(link_count), fg='red')} -> {links_outfile.name}"
    )
    click.echo(f"Import CSVs into Neo4j:")
    click.secho(
        (
            f"neo4j-admin import --nodes:Page {pages_outfile.name} \\ \n"
            f"\t--relationships:LINKS_TO {links_outfile.name} \\ \n"
            "\t--ignore-duplicate-nodes --ignore-missing-nodes --multiline-fields"
        ),
        fg="blue",
    )

def parse_excel(file,keyword):
    oof = pandas.read_excel(file,sheet_name="Cau Hoi")
    ooof = pandas.read_excel(file, sheet_name="Kien thuc")
    fuck = pandas.read_excel(file, sheet_name="Dap An")
    print(list(oof))
    if "Chuong" in keyword:
        list_columns_fake = list(oof)[list(oof).index(keyword)+1:]
        print(list_columns_fake)
        list_columns = [keyword]
        for name in list_columns_fake:
            if "Unnamed" in name:
                list_columns.append(name)
            else: break
        print(list_columns)
        b1 = pandas.DataFrame(oof, columns= list_columns)
        print(b1)

def extra():
    parse_excel("Teacher_form.xlsx","Chuong 1")

if __name__ == "__main__":
    extra()
