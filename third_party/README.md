# Third-Party Dependency Notes

This folder is reserved for vendored or mirrored dependencies.

In the current workspace, the original upstream/reference code is still located at:

- [`multimodal/`](/d:/文件/论文/华西论文-多模态/code/multimodal)
- [`H-frame-work/`](/d:/文件/论文/华西论文-多模态/code/H-frame-work)

Reason: the historical source trees contain nested repositories and very deep paths, so the reorganization in this workspace keeps them in place while exposing new stable wrappers from [`src/`](/d:/文件/论文/华西论文-多模态/code/src).

Use the wrapper entry points first; treat the historical trees as reference implementations.
