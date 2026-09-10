# Dy Language Support

Syntax highlighting and basic editor behavior for `.dy` source files in Visual
Studio Code and compatible editors.

## Try it locally

Copy or symlink this directory into your editor's extension directory, then run
`Developer: Reload Window` from the command palette.

- Cursor: `~/.cursor/extensions/dy-language-0.1.0`
- Visual Studio Code: `~/.vscode/extensions/dy-language-0.1.0`

After reloading, open a `.dy` file. The language indicator in the lower-right
corner should say `Dy`.

For extension development, launch the editor with this directory as its
extension development path:

```sh
cursor --extensionDevelopmentPath=/absolute/path/to/editors/vscode-dy
```
