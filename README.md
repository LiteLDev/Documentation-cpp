# LiteLoaderBDS C++ Plugin Development Documentation and API Reference Generator

This is the generator for LiteLoaderBDS C++ plugin development documentation and API reference.

If you would like to preview the latest official build, please visit [LiteLoaderBDS C++ Plugin Development Documentation](https://cpp.docs.litebds.com/en/) or [LiteLoaderBDS C++插件开发文档](https://cpp.docs.litebds.com/zh-Hans/)

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

Generate raw English documentation for LiteLoaderBDS development to `/docs/api/`:

```sh
doxygen Doxyfile_raw
```

All documentation will be generated in `/docs/en/`, `/docs/zh-Hans/` and `/docs/api/`.

## Contribution

If you would write some pages manually, please create them in `/pages/en/` or `/pages/zh-Hans/`.

If you are contributing to the general documentation, please go to [the repository for general documentation](https://github.com/LiteLDev/docs).

If you are contributing to the Doxygen comments in `/SDK/`, please go to [the main repository](https://github.com/LiteLDev/LiteLoaderBDS) and modify the files in `/LiteLoader/`.

You should NOT modify the texts in different languages.
If you are likely to contribute to internationalization, please go to [our crowdin project](https://crowdin.com/project/liteloaderbds).
Please firstly fork this repository and then create a pull request!
Doxygen will then automatically generate the documentation along with these pages. 
