import click
import onepy

on = onepy.OneNote()

def get_notebook_by_name(nb="Blocnote"):
    for notebook in on.hierarchy:
        if (notebook.name and notebook.name == nb):
            return notebook

def get_section_by_name(notebook, sectionName="System"):
    if sectionName!='All':
        return [section for section in notebook if section.name == sectionName ]
    else:
        return [section for section in notebook if isinstance(section,onepy.Section) ]

def get_page_by_name(section, pageName="LVS"):
    if pageName!='All':
        return [page for page in section if page.name == pageName ]
    else:
        return [page for page in section if isinstance(page,onepy.Page) ]

def dump_page_content(page):
    pagecontent = on.get_page_content( page.id )
    tagdefs = dict ( (td.index, td.name) for td in pagecontent.tagdefs )
    for outline in pagecontent:
        for oe in outline:
            for t in oe.tags:
                print ("!"+tagdefs[t.index]+"!",end="")
            click.echo (oe.text)


@click.command()
@click.option('--blocnote', prompt='BlocNote name', help='The bloc note to parse.')
@click.option('--section', prompt='Section name', help='The section to parse.', default='All')
@click.option('--page', prompt='Page name', help='The page to parse.', default='All')
def onenote(blocnote,section,page):
    nb = get_notebook_by_name(blocnote)
    for on_section in get_section_by_name(nb,section):
        for on_page in get_page_by_name(on_section,page):
            print ("========["+nb.name+"/"+on_section.name+"/"+on_page.name+"]=======")
            dump_page_content(on_page)

if __name__ == '__main__':
    onenote()
