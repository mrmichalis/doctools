#!/usr/bin/env python
# -*- mode: Python; coding: utf-8 -*-

import sys

def out_entries(entries, column_types, html_mode):
  buff = []
  if html_mode:
    for entry in entries:
      buff.append('<tr>')
      for index, content in enumerate(entry):
        buff.append('<td align="left" valign="top">')
        if column_types[index] == "mono":
          buff.append('<p><code class="literal">')
        buff.append(content.strip()) 
        if column_types[index] == "mono":
          buff.append('</code></p>')
        buff.append('</td>')
      buff.append('</tr>')
  else:
    for entry in entries:
      buff.append('<row>')
      for index, content in enumerate(entry):
        buff.append('<entry align="left" valign="top">')
        if column_types[index] == "mono":
          buff.append('<simpara><literal>')
        buff.append(content.strip()) 
        if column_types[index] == "mono":
          buff.append('</literal></simpara>')
        buff.append('</entry>')
      buff.append('</row>')
  return buff

def table_start(title, setting_key, column_count, html_mode):
  buff = []
  buff.append('<table id="')
  buff.append(setting_key)
  if html_mode:
    buff.append('" class="configsetting"  cellspacing="0" cellpadding="0">')
    buff.append('<caption>')
    buff.append(title)
    buff.append('</caption>')
  else:
    buff.append('" tabstyle="configsetting table" role="configsetting" frame="all" rowsep="1" colsep="1">')
    buff.append('<title>')
    buff.append(title)
    buff.append('</title>')
    buff.append('<tgroup cols="')
    buff.append(str(column_count))
    buff.append('">')
    for i in range(1, column_count + 1):
      buff.append('<colspec colname="col')
      buff.append(str(i))
      buff.append('"/>')
  return buff

def table_head(intro):
  buff = []
  buff.append('<thead>')
  buff.extend(intro)
  buff.append('</thead>')
  return buff;

def table_footer(default_value, column_count, html_mode):
  buff = []
  if html_mode:
    buff.append('<tfoot><tr><td class="configsetting-default" align="left" valign="top" colspan="')
    buff.append(str(column_count))
    buff.append('">Default value: <code class="literal">')
    buff.append(default_value)
    buff.append('</code></td></tr></tfoot>')
  else:
    buff.append('<tfoot><row><entry role="configsetting-default" align="left" valign="top" namest="col1" nameend="col')
    buff.append(str(column_count))
    buff.append('">Default value: <literal>')
    buff.append(default_value)
    buff.append('</literal></entry></row></tfoot>')
  return buff;

def config_intro(setting_key, description, column_count, html_mode):
  buff = []
  if html_mode:
    buff.append('<tr><td align="left" valign="top" colspan="')
    buff.append(str(column_count))
    buff.append('"><p class="configsetting-key"><code class="literal">')
    buff.append(setting_key)
    buff.append('</code></p><p class="configsetting-desc">')
    buff.append(description)
    buff.append('</p></td></tr>')
  else:
    buff.append('<row><entry align="left" valign="top" namest="col1" nameend="col')
    buff.append(str(column_count))
    buff.append('"><simpara role="configsetting-key"><literal>')
    buff.append(setting_key)
    buff.append('</literal></simpara><simpara role="configsetting-desc">')
    buff.append(description)
    buff.append('</simpara></entry></row>') 
  return buff

data = sys.stdin.readlines()
line = data.pop(0).split(':', 1)
setting_key = line[0]
default_value = None
if len(line) > 1:
  default_value = line[1]
description = data.pop(0)

if len(sys.argv) > 1:
  title = sys.argv[1]
html_mode = False
if len(sys.argv) > 2 and sys.argv[2]=="--html":
  html_mode = True
setting_type = "default"
if len(sys.argv) > 3:
  setting_type = sys.argv[3]

headings = ["Value"]
column_types = ["mono"]

body = []
body.append('<tbody>')

head = []

has_value_descriptions = False
rows = []
for line in data:
  parts = line.split(':', 1)
  rows.append(parts)
  if len(parts) > 1:
    has_value_descriptions = True

if len(rows) > 0:
  if setting_type in ["minmax", "min", "max"]:
      headings.insert(0, "Limit")
      column_types.insert(0, "default")
  if has_value_descriptions:
    headings.append("Description")
    column_types.append("default")  
  if setting_type == "minmax":
    rows[0].insert(0, "min")
    rows[1].insert(0, "max")
  elif setting_type == "min":
    rows[0].insert(0, "min")
  elif setting_type == "max":
    rows[0].insert(0, "max")
  column_count = len(headings)
  head.extend(config_intro(setting_key, description, column_count, html_mode))
  head.extend(out_entries([headings], ["default"] * column_count, html_mode))
  body.extend(out_entries(rows, column_types, html_mode))
else:
  column_count = 1
  body.extend(config_intro(setting_key, description, column_count, html_mode))

body.append('</tbody>')

sys.stdout.write(''.join(table_start(title, setting_key, column_count, html_mode)))
if len(head) > 0:
  sys.stdout.write(''.join(table_head(head)))  
if default_value is not None:
  sys.stdout.write(''.join(table_footer(default_value, column_count, html_mode)))
sys.stdout.write(''.join(body))
if not html_mode:
  sys.stdout.write('</tgroup>')
sys.stdout.write('</table>')
