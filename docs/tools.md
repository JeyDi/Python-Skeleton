# Tools

## Commitizen

[Commitizen](https://commitizen-tools.github.io/commitizen/) is installed as a dev dependency. It can be used to automatically handle versioning and changelogs
```
v{MAJOR}.{MINOR}.{PATCH}
```
Be sure to commit only a single type of change each time and use
```{code-block} console
$ cz commit
```
instead of the standard `git commit`.
```{note}
You can still use `git commit` but the commit has to follow a [specific standard](https://www.conventionalcommits.org/).
```

Other useful commands are:
- `cz bumpy --dry-run` which compute the next version number without actually tagging on git (dry run)
- `cz ch` generate the CHANGELOG.md

## Poetry

## Sphinx

Documentation is handled by Sphinx and in IDEs Google standard for docstring is set.

### MyST

The [MyST extension](https://myst-parser.readthedocs.io/) for Sphinx allows to write documentation pages in Markdown as well.
