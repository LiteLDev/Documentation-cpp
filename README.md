# LiteLoaderSDK Plugin Development Documentation Generator

This is the generator for LiteLoaderBDS plugin development documentation.

If you would like to preview the latest official build, please visit [LiteLoaderSDK Plugin Development Documentation](https://cpp.docs.litebds.com/en/) or [LiteLoaderSDK插件开发文档](https://cpp.docs.litebds.com/zh-Hans/)

## Build

### Prerequisites

* [Graphviz >= 1.8.10](https://www.graphviz.org/)

### Documentation Generation

Generate English documentation to `/docs/en/`:

```sh
doxygen Doxyfile_en
```

Generate Simplified Chinese documentation to `/docs/zh-Hans/`:

```sh
doxygen Doxyfile_zh-Hans
```

Generate raw English documentation for LiteLoaderBDS development to `/docs/raw/`:

```sh
doxygen Doxyfile_raw
```

All documentation will be generated in `/docs/en/`, `/docs/zh-Hans/` and `/cocs/raw/`.

## Contribution

If you would write some pages manually, please create them in `/pages/en/` or `/pages/zh-Hans/`.
Please firstly fork this repository and then create a pull request!
Doxygen will then automatically generate the documentation along with these pages.