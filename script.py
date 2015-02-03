#!/usr/bin/env python3

import re

#lxml
import lxml
from lxml.html import builder as E
from lxml.builder import ElementMaker as EM

input_file = 'input.txt' #File with ierarchy
output_file = 'output.txt' #output with html code

def get_links(lines, position, hierarchy):
    links = []
    pattern = re.compile('(?<=-)([^\s\$][^\s]*)\s(.+)')
    while position < len(lines):
        line = lines[position]
        line = line.replace('\n', '')
        if line == '':
            position += 1
            continue
        match = pattern.search(line)
        if match is None:
            return links, position
        links.append(E.DIV(E.A(match.group(2),
                               target='main',
                               href=hierarchy[-2]+'/'+match.group(1)+'/'
                               )))
        position += 1
    return links, position

def get_categories(lines, position, hierarchy):
    cats = []
    pattern = re.compile('(?<=-\$)(.+)')
    while position < len(lines):
        line = lines[position]
        line = line.replace('\n', '')
        if line == '':
            position += 1
            continue
        match = pattern.search(line)
        if match is None:
            return cats, position
        hierarchy.append(match.group(1))
        links, pos = get_links(lines, position+1, hierarchy)
        hierarchy.pop()
        cats.append(E.DIV(E.A(E.U(match.group(1)),
                              id='cat',
                              onclick="toggle(this, '"+hierarchy[-1]+match.group(1)+"');")))
        cats.append(E.DIV(*links,
                          id = hierarchy[-1]+match.group(1)))
        position = pos
    return cats, position

def get_boards(lines, position, hierarchy):
    divs = []
    pattern = re.compile('([^\s]+)\s(.+)')
    while position < len(lines):
        line = lines[position]
        line = line.replace('\n', '')
        if line == '':
            position += 1
            continue
        match = pattern.search(line)
        if match is None:
            return divs, position
        hierarchy.append(match.group(1))
        cats, pos = get_categories(lines, position+1, hierarchy)
        hierarchy.pop()
        divs.append(E.DIV(E.CLASS('fib'),
                         E.A(match.group(2),
                             id = 'board',
                             target = 'main',
                             href = 'http://'+match.group(1)),
                         E.A('[+]',
                             id = 'plus',
                             onclick = "toggle(this, '"+match.group(2)+"');")
                         )
                   )
        divs.append(E.DIV(*cats,
                         style = "display: none;",
                         id = match.group(2)))
        position = pos
    return divs, position

def get_sections(lines, position, hierarchy):
    trs = []
    pattern = re.compile('(?<=#)(.+)')
    while position < len(lines):
        line = lines[position]
        line = line.replace('\n', '')
        if line == '':
            position += 1
            continue
        match = pattern.search(line)
        if match is None:
            return trs, position
        hierarchy.append(match.group(1))
        divs, pos = get_boards(lines, position+1, hierarchy)
        hierarchy.pop()
        trs.append(E.TR(E.TD(E.CLASS('header'), match.group(1))))
        trs.append(E.TR(E.TD(E.CLASS('list'),*divs)))
        position = pos
    return trs, position
    

if __name__ == "__main__":
    f = open(input_file, 'r')
    hierarchy = []
    trs, end_pos = get_sections(f.readlines(), 0, hierarchy) #trs are tr sections from table
        
    html = E.TABLE(E.CLASS('category'),
                   E.TBODY(*trs),
                   width="100%",
                   border="0",
                   cellspacing="0",
                   cellpadding="0")

    html_code = lxml.html.tostring(html)

    res_f = open(output_file, 'wb')
    res_f.write(html_code)
    res_f.close()
