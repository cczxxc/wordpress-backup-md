---
id: 74
title: Python 笔误不小心在变量赋值的末尾加了逗号，会变成tuple，解决方案在此！
date: 2025-09-01T23:57:43
slug: python-笔误不小心在变量赋值的末尾加了逗号，会变成tupl
original_slug: python-%e7%ac%94%e8%af%af%e4%b8%8d%e5%b0%8f%e5%bf%83%e5%9c%a8%e5%8f%98%e9%87%8f%e8%b5%8b%e5%80%bc%e7%9a%84%e6%9c%ab%e5%b0%be%e5%8a%a0%e4%ba%86%e9%80%97%e5%8f%b7%ef%bc%8c%e4%bc%9a%e5%8f%98%e6%88%90tupl
link: https://xin.a0001.net/2025/09/01/python-%e7%ac%94%e8%af%af%e4%b8%8d%e5%b0%8f%e5%bf%83%e5%9c%a8%e5%8f%98%e9%87%8f%e8%b5%8b%e5%80%bc%e7%9a%84%e6%9c%ab%e5%b0%be%e5%8a%a0%e4%ba%86%e9%80%97%e5%8f%b7%ef%bc%8c%e4%bc%9a%e5%8f%98%e6%88%90tupl/
status: publish
---

**flake8-commas 2.1.0**

pip install flake8-commasCopy PIP instructions

[Latest version](https://pypi.org/project/flake8-commas/)

Released: Oct 14, 2021

Flake8 lint for trailing commas.

来自 <<https://pypi.org/project/flake8-commas/>>

Project description

**Note:** [Black](https://pypi.org/project/black/), the uncompromising Python code formatter, or [add-trailing-comma](https://github.com/asottile/add-trailing-comma) can do all this comma insertion automatically. We recommend you use one of those tools instead.

**Usage**

If you are using flake8 it’s as easy as:

pip install flake8-commas

Now you can avoid those annoying merge conflicts on dictionary and list diffs.

**Errors**

Different versions of python require commas in different places. Ignore the errors for languages you don’t use in your flake8 config:

|  |  |
| --- | --- |
| **Code** | **message** |
| C812 | missing trailing comma |
| C813 | missing trailing comma in Python 3 |
| C814 | missing trailing comma in Python 2 |
| C815 | missing trailing comma in Python 3.5+ |
| C816 | missing trailing comma in Python 3.6+ |
| C818 | trailing comma on bare tuple prohibited |
| C819 | trailing comma prohibited |

**Examples**

lookup\_table={‘key1′:’value’,’key2′:’something’# <– missing a trailing comma}json\_data=json.dumps({“key”:”value”,}),# <– incorrect trailing comma. json\_data is now a tuple. Likely by accident.
