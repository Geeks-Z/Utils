
from notion.client import NotionClient
from notion.block import PageBlock
from md2notion.upload import upload, convert, uploadBlock
from md2notion.NotionPyRenderer import NotionPyRenderer, addLatexExtension
import itertools

client = NotionClient(token_v2="3d768f741e764eb1c3b8f9bae6dde742dc7a71d56620d73a43ee0f0490b6da5bbed14f40ff316a5560bd0707a08ed1ca2e6932732f50dde597e2d127b75012239ce53d21414e533ae4cb34013612")
page = client.get_block("https://www.notion.so/Test-54a2ae71f2fa45c5aef85064789715cc")

print("The old title is:", page.title)

with open("/Users/geeks_z/Documents/OneDrive - nuaa.edu.cn/MyNotes/ML/Regularization.md", "r", encoding="utf-8") as mdFile:
    newPage = page.children.add_new(PageBlock, title="TestMarkdown Upload")
    # upload(mdFile, newPage, notionPyRendererCls=addLatexExtension(NotionPyRenderer))
    lines = mdFile.readlines()
    new_lines = lines.copy()

    flag = 0
    insert_nums = 0
    for (i, line) in enumerate(lines):

        if i > 0 and i < len(lines) - 2:
            if flag == 0 and line == '$$\n':
                pos = i + insert_nums
                new_lines.insert(pos, '\n')
                insert_nums += 1
                flag = 1

            elif flag == 1 and line == '$$\n':
                pos = i + insert_nums + 1
                new_lines.insert(pos, '\n')
                insert_nums += 1
                flag = 0

    rendered = convert(new_lines, addLatexExtension(NotionPyRenderer))
    for blockDescriptor in rendered:
        uploadBlock(blockDescriptor, newPage, mdFile.name)