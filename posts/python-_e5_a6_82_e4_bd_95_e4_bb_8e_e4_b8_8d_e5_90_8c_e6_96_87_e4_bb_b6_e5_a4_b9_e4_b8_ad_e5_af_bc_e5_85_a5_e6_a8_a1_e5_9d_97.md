---
title: Python 如何从不同文件夹中导入模块
date: 2025-09-01T23:52:20
slug: python-%e5%a6%82%e4%bd%95%e4%bb%8e%e4%b8%8d%e5%90%8c%e6%96%87%e4%bb%b6%e5%a4%b9%e4%b8%ad%e5%af%bc%e5%85%a5%e6%a8%a1%e5%9d%97
id: 70
---

方法一：添加路径到sys.path
-----------------

一种简单的方法是将模块所在文件夹的路径添加到sys.path中。sys.path是一个包含Python解释器在导入模块时搜索路径的列表。通过将模块所在文件夹的路径添加到sys.path中，我们可以在任何地方导入该模块。

首先，我们需要确定模块所在文件夹的路径。假设我们的项目结构如下：

```
project/
├── main.py
└── subfolder/
    └── module.py
```

我们想要从main.py中导入subfolder文件夹中的module.py。我们可以使用以下代码将subfolder的路径添加到sys.path：

```
import sys
sys.path.append("subfolder")
```

现在，我们可以导入module.py，代码如下：

```
from module import function
```

这样就成功地从不同文件夹中导入了module.py中的函数。

方法二：使用相对路径导入
------------

除了将路径添加到sys.path中，我们还可以使用相对路径导入模块。相对路径是相对于当前脚本文件所在的文件夹来定位其他文件夹或文件的路径。

继续使用上面的例子，如果我们的main.py脚本和subfolder文件夹在同一个文件夹下，我们可以使用相对路径来导入module.py。

首先，假设我们的项目结构如下：

```
project/
└── main.py
    ├── subfolder/
    │   └── module.py
    └── utils/
        └── utility.py
```

我们想在main.py中导入module.py，并且main.py和module.py在同一级目录中。我们可以使用以下代码导入module.py：

```
from .subfolder.module import function
```

此处的`.`表示当前文件夹，`.subfolder.module`表示相对于当前文件夹的subfolder文件夹中的module.py。

如果我们希望在utility.py中导入module.py，可以使用以下代码：

```
from ..subfolder.module import function
```

此处的`..`表示当前文件夹的父级文件夹。

方法三：使用绝对路径导入
------------

另一种方法是使用绝对路径导入模块。绝对路径是指从根路径开始的完整路径。

继续使用上面的例子，假设我们的项目结构如下：

```
project/
├── main.py
├── subfolder/
│   └── module.py
└── utils/
    └── utility.py
```

现在，我们想在utility.py中导入module.py。我们可以使用以下代码导入module.py：

```
import sys
sys.path.append("/path/to/project")
from subfolder.module import function
```

在这个例子中，`/path/to/project`是项目根文件夹的绝对路径，`subfolder.module`是相对于根文件夹的路径。

使用绝对路径可以确保在任何情况下都能正确地导入模块，但需要注意绝对路径的可移植性。

最佳实践, 直接在site-packages里建立文件夹mypack，这样不管哪个项目都可以从这里导入即可，import mypack.abcd
========================================================================
