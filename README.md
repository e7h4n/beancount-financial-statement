# Beancount 财报

[![Build Status](https://app.travis-ci.com/e7h4n/beancount-financial-statement.svg?branch=master)](https://app.travis-ci.com/e7h4n/beancount-financial-statement)

一个给个人用的财报工具，分析 beancount 账本，自动生成资产负债表。

## Demo

![Balance Sheet](/example/balance_sheet.png)

## 如何使用

1. 创建一个额外的 layout.txt 文件来控制资产负债表中各个项目的顺序。

例如:

```
Assets:Current assets:Cash and cash equivalent
Assets:Current assets:Short-term investment
Assets:Current assets:Account receivables
Assets:Non-current assets:Stock and index fund
Assets:Non-current assets:Equipments
Assets:Non-current assets:Real estate
Liabilities:Current liabilities:Credit card
Liabilities:Current liabilities:Account payable
Liabilities:Non-current liabilities:Loan
Equity:Current equity:Current assets
Equity:Current equity:Current liabilities
Equity:Non-current equity:Non-current assets
Equity:Non-current equity:Non-current liabilities
```

同时在账本开头设置 layout 文件的位置:

```beancount
1970-01-01 custom "finance-statement-option" "balance_sheet_layout" "layout.txt"
```

balance_sheet_layout 是相对于账本主文件的路径。

这样的 layout 会让资产负债表从上到下分别是资产、负债和所有者权益。

Layout 中的每一项，都可以在账本中通过 `balance_sheet_category` 和 `equity_category` 来指定。

2. 在账本中给所有的 Assets 和 Liabilities 设置类别。

例如:

```beancount
2019-01-01 open Assets:US:BofA
  balance_sheet_category: "Assets:Current assets:Cash and cash equivalent"
  equity_category: "Equity:Current equity:Current assets"
```

以上这个例子的意思是，将 `Assets:US:BofA` 这项资产，计入 `Assets:Current assets:Cash and cash equivalent` 这一分类。同时这项资产会参与 `Equity:Current equity:Current assets` 这项所有者权益的计算。

再看一个负债的例子:

```beancount
1980-05-12 open Liabilities:US:Chase:Slate                      USD
  balance_sheet_category: "Liabilities:Current liabilities:Credit card"
  equity_category: "Equity:Current equity:Current liabilities"
```

这个例子的意思是，将 `Liabilities:US:Chase:Slate` 这项负债，计入 `Liabilities:Current liabilities:Credit card` 这一分类，同时这项资产会参与 `Equity:Current equity:Current liabilities` 的计算。

3. 在账本中配置财报所使用的货币。

在账本开头设置:

```beancount
1970-01-01 custom "finance-statement-option" "working_currency" "USD"
```

这样会把生成的报表所有的货币都统一成 `working_currency`。

4. 执行命令

[正在开发，这里还缺一个好用的命令行 wrapper.]

## How to contribute

```bash
$ make
Some available commands:
 * run          - Run code.
 * test         - Run unit tests and test coverage.
 * doc          - Document code (pydoc).
 * clean        - Cleanup (e.g. pyc files).
 * code-style   - Check code style (pycodestyle).
 * code-lint    - Check code lints (pyflakes, pyline).
 * code-count   - Count code lines (cloc).
 * deps-install - Install dependencies (see requirements.txt).
 * deps-update  - Update dependencies (via pur).
```

## Todo

- [x] 资产负债表
 - [ ] 易于使用的命令行界面
 - [ ] 更多的 Test Case
 - [ ] 完善 Pydoc
 - [ ] 更好的 Code Style
 - [ ] 更多的例子
- [ ] 利润表
- [ ] 现金流量表

## License

MIT.
