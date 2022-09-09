# Hook指南 {#hook_howto}

HookAPI是LiteLoaderBDS实现各种功能的基础API，本页主要讲述HookAPI的使用方法，以及相关的原生实现，帮助您更快的了解实现原理，并熟悉相关流程

> 阅读并理解本页内容可能需要一定的汇编基础，有助于了解实际指令与目标实现的关联

## 相关名词

### Portable Executable（PE）

可移植性可执行文件（Portable Executable，缩写为PE）是一种用于可执行文件、目标文件和动态链接库的文件格式，主要使用在Windows操作系统上。在Windows开发环境中，PE格式也称为PE/COFF格式。

> Ref: [PE Format - Microsoft Doc](https://docs.microsoft.com/en-us/windows/win32/debug/pe-format)

### Relative virtual address (RVA)

在PE文件中，RVA为相对ImageBase而言的地址。PDB等地方记录的地址通常为RVA。
在未链接的Object中，RVA几乎没有意义。

### Virtual Address (VA)

VA是PE文件被操作系统加载进内存后的地址。VA不可在编译期间预测。

> 转换：VA = ImageBase + RVA

### Hook

Hook是指通过对函数入口进行修改，从而使其被调用时跳转到另外一段代码块的操作。

### Mangled Name

Mangeled Name 修饰函数名（为符合使用习惯，下文将用`符号`代指）是现代化的语言为实现包管理，函数重载等功能创建的一项对函数名（或变量等）（链接/查找时）修饰的方案。通过对函数名进行修饰，可以避免出现在不同命名空间内或不同重载的函数名冲突的问题。对于MSVC，Mangled Name包含`名字`,`类型`,`参数`,`this指针`,`调用约定`等信息。

## API介绍以及范例

LL提供了两种函数查找方式（基于符号查询或基于特征码搜索），可满足几乎全部使用需求。在此基础上封装了三种Hook模板，便于方便的Hook函数。分别是`THook`(符号查找)，`SHook`(特征码搜索)，和`AHook`（指定地址），另外还有三种特殊的变形，方便在不同场合的使用。分别是(`(T/A/S)`)`StaticHook`(静态函数特例),`InstanceHook`（实例化函数特例）,`ClasslessInstanceHook`（忽略this指针的实例化函数特例）

### 基础格式

Hook模板需要在全局定义域范围内使用，并会在插件全局变量初始化阶段自动隐式完成Hook的设置。

## THook

```cpp
// 符号：?disconnect@ServerPlayer@@QEAAXXZ
// 签名：public: void __cdecl ServerPlayer::disconnect(void) __ptr64
THook(void, "?disconnect@ServerPlayer@@QEAAXXZ", 
    ServerPlayer* player/*this*/) {
    return original(player);//执行原函数
}
```

基础形式：`THook(返回值, "符号", 参数列表...){函数体}`

当`void ServerPlayer::disconnect()`函数被调用时，你定义的代码块将优先被调用。为了拦截某个事件的发生，在部分情况中可以选择不执行原有的函数。若需要保留原有功能，请调用`original`函数。

## TInstanceHook

```cpp
// 符号：?disconnect@ServerPlayer@@QEAAXXZ
// 签名：public: void __cdecl ServerPlayer::disconnect(void) __ptr64
TInstanceHook(void, "?disconnect@ServerPlayer@@QEAAXXZ",
      ServerPlayer /*this*/) {
    return original(this); //执行原函数
}
```

基础形式：`TInstanceHook(返回值, "符号", this指针类型, 参数列表...){函数体}`

`TInstanceHook`与`THook`功能一致，但此写法可以以this指针的方式获得当前类的指针。

## TClasslessInstanceHook

```cpp
// 符号：?disconnect@ServerPlayer@@QEAAXXZ
// 签名：public: void __cdecl ServerPlayer::disconnect(void) __ptr64
TClasslessInstanceHook(void, "?disconnect@ServerPlayer@@QEAAXXZ",
      /*this*/) {
    return original(this); //执行原函数
}
```

基础形式：`TClasslessInstanceHook(返回值, "符号", this指针类型, 参数列表...){函数体}`

`TClasslessInstanceHook`与`TInstanceHook`功能一致，但此写法忽略this指针类型，隐藏this指针类型，方便某些特殊需求。
