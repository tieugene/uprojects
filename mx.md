# Goal #
Main goal of this project is to make something like DMS (Document Management System).

This will made by concatenating three technologies - [xattr](http://en.wikipedia.org/wiki/Xattr) + [inotify](http://en.wikipedia.org/wiki/Inotify) + index.html.

In short:
  * we edit xattr (extended attributes) of file using special xattr editor (e.g. eiciel); name, type and other attributes of xattrs for files in any folder defined by .index.cfg file ("scheme"), laying in this folder (so - each folder can have own xattr scheme);
  * after writing to disk inotify run special script - can be different to each handling folder;
  * this script creates index.html - using user defined algorythm;
  * then just check on "Use index.html" in your Konqueror... :-)

Main advantage of this project is that user defined metadata for file, stored into xattrs of this file, can be moved to anywhere w/ this file; and not depend from renaming this file.

# ToDo #

  * scheme - DONE
  * Qxattr + scheme - DONE...
  * xattr2index (w/ scheme)
  * inotify
  * index template?

# Scheme #
Description of available Xattrs:

| **Mult** | **1stLetter** | **DataType** | **Widget** | set | get |
|:---------|:--------------|:-------------|:-----------|:----|:----|
| -        | b             | bool         | CheckBox   | setCheckState | isChecked |
| +        | se            | str + enum   | ComboBox   | findText + setCurrentIndex | currentText |
| +        | st            | str + enum   | LineEdit + TreeView | setText | text |
| +        | sl            | str          | LineEdit   | setText | text |
| -        | sh            | html         | TextEdit   | setText | toHtml |
| -        | sp            | text         | PlainTextEdit | setText | toPlainText |
| +        | i/u[1..8]     | int/long     | SpinBox    | setValue | value |
| +        | f...          | float/double | DoubleSpinBox | setValue | Value |
| +        | d             | date         | DateEdit   | setDate | date |
| +        | t             | time         | TimeEdit   | setTime | time |
| +        | dt            | datetime     | DateTimeEdit | setDateTime | dateTime |
| -        | g             | image        | GraphicsView |     |     |
| +        | x             | URL          | LineEdit   | setText | text |

Excluded: RadioButton.

Main features:
  * File format - config;
  * Store method - "everything onboard" - xattr names describe everything about xattr type;
  * Empty xattr must be deleted;
  * Naming - 

&lt;type&gt;

.Name - "hungarian notation" + CamelCase;

Global attributes ([DEFAULT](DEFAULT.md) section:
  * ver:str - format version
  * codepage:str

Common attributes:
  * ID:string - uniq name - and xattr
  * Label:string(utf8) - option (default - ID w/o types
  * ToolTip:str - option
  * StatusTip:str - option
  * WhatsTip:str - option
  * Mandatory:bool [false](false.md) - option
  * Default: 

&lt;type&gt;

 - option

Widgets can present 0, 1 or many times - but not all of them.
Plural Xattrs stores in one xattr and sre separated dependently of datatype.
Widget and data type encoded in 1st letter of xattr name.

## CheckBox ##
Mult: no
Store as: bit
Options: None

## ListBox ##
Mults: yes, splited by CR or \0
Store as: str
Options:
  * Values:str, quoted CSV

## TreeView ##
Mults: yes, splited by CR or \0
Store as: str as path
Options:
  * Values:str, quoted CSV as paths

## LineEdit ##
Mults: yes, splited by CR or \0
Store as: str
Options:
  * Mask:str

## TextEdit ##
Mults: yes, splited by \0
Store as: str (html)
Options: None

## PlainTextEdit ##
Mults: yes, splited by \0
Store as: str
Options: None

## SpinBox ##
Mults: yes, not splited
Store as: int
Options:
  * Size:int - power of 2
  * Min:int
  * Max:int

## DoubleSpinBox ##
Mults: yes, not splited
Store as: byte sequence
Options:
  * Size:int
  * Prec:int
  * Min:fixed
  * Max:fixed

## Date ##
Mults: yes, not splited
Store as: int32
Options:
  * Min:isodate
  * Max:isodate
  * Unsigned:bool
? TZ, calendar

## Time ##
Mults: yes, not splited
Store as: int32 (h5m6s6ms10tz5)
Options: None

## DateTime ##
Mults: yes, not splited
Store as: int64
Options:
  * Min:isodate
  * Max:isodate
  * Unsigned:bool
? TZ, calendar

## Image ##
Mults: no
Store as: blob
Options: None

## Href ##
Mults: yes, splited by CR or \0
Store as: str
Options: None

## FileLinked ##
Mults: yes, not splited
Store as: int64
Options: None


---

  * Find: naming
  * Xattr name:value => RDF
  * ...but predicate attrs - ёк...
  * => everything == file
  * Anything can be stored in xattr - changing history, scheme own (!)
  * So, xattr description can be saved in dir xattr
  * ext3+webdav+http...