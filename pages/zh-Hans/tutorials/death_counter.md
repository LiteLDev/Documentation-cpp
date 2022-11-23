# 死亡计数器 {#death_counter}

[![GitHub](https://img.shields.io/badge/GitHub-Futrime%2FLLDeathCounter-orange?style=for-the-badge&logo=github)](https://github.com/Futrime/LLDeathCounter)
[![License](https://img.shields.io/github/license/Futrime/LLDeathCounter?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter/blob/main/LICENSE)
[![Downloads](https://img.shields.io/github/downloads/Futrime/LLDeathCounter/total?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter/releases/latest)
[![Issues](https://img.shields.io/github/issues/Futrime/LLDeathCounter?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter/issues)
[![Stars](https://img.shields.io/github/stars/Futrime/LLDeathCounter?style=for-the-badge)](https://github.com/Futrime/LLDeathCounter)

本教程将分析由[Futrime](https://github.com/Futrime)创作的插件LLDeathCounter。
完整代码请见[GitHub仓库](https://github.com/Futrime/LLDeathCounter).

LLDeathCounter是一个将玩家死亡次数记录并显示在暂停菜单中的插件。

由于该插件过于简单，无需使用多文件，所以所有代码均位于 `/src/Plugin.cpp` 。

## 包含必要的头文件

我们需要这些头文件：

* EventAPI.h
* ScheduleAPI.h
* MC/Scoreboard.hpp

我们同时还需要一些其它头文件以保证中间量能被正常解析。

所有 `#include` 代码如下：

```cpp
#include <llapi/EventAPI.h>
#include <llapi/ScheduleAPI.h>

#include <llapi/MC/Objective.hpp>
#include <llapi/MC/Player.hpp>
#include <llapi/MC/Scoreboard.hpp>
#include <llapi/MC/Types.hpp>
#include <string>
```

## 初始化插件

当LiteLoaderBDS启动时，每个插件的`PluginInit()`函数将被调用。
你可以把它当作普通C++程序中的 `main()` 函数，但对于插件而言。
但是你应该特别注意，在`PluginInit()`函数中，你**不能访问任何与游戏有关的API**，这很可能导致SEH异常，因为插件是在游戏加载之前被初始化的。

如果你想对游戏对象做一些设置工作，你应该把代码放在`ServerStartedEvent`的回调中，它将在游戏加载时立即执行。

我们假定你已经掌握了`scoreboard`命令的用法和Minecraft的记分牌机制。
如果你对此感到困惑，请访问[Minecraft Wiki](https://minecraft.fandom.com/wiki/Scoreboard)了解更多信息。

在函数`PluginInit()`中：

```cpp
Event::ServerStartedEvent::subscribe([](const Event::ServerStartedEvent& event) {
  auto* objective = Scoreboard::newObjective("lldeathcounter", "Death Count");
  objective->setDisplay(/*slotName=*/"list",
                        /*sort=*/ObjectiveSortOrder::Descending);
  return true;
});
```

在这里，我们使用只读的监听方法，以优化性能，并防止意外地修改事件。

```cpp
Event::ServerStartedEvent::subscribe([](const Event::ServerStartedEvent& event) {
  // ...
});
```

我们首先创建一个记分牌目标，其ID为“lldeathcounter”，显示名称为“死亡计数”。

```cpp
auto* objective = Scoreboard::newObjective("lldeathcounter", "Death Count");
```

然后我们让目标出现在暂停菜单的玩家名单上。

```cpp
objective->setDisplay(/*slotName=*/"list",
                      /*sort=*/ObjectiveSortOrder::Descending);
```

虽然这个事件不能被抑制，但回调函数应该返回一个布尔值。
你可以返回真或假，这并不重要。
为了方便审查，我们建议你使用 `return true`。

## 玩家死亡时增加分数

如果你想用命令块做一个玩家死亡记录器，你必须让命令块每隔一段时间就执行一次命令，以测试玩家是否还活着，这听起来是在浪费性能，而且不优雅。

有了LiteLoaderBDS强大的事件系统，你只需监听PlayerDieEvent，并在事件被触发时操作记分牌。

你可以随时随地订阅一个事件，也可以随时随地通过调用`listener.remove()`取消订阅。
然而，我们建议将订阅器的创建放在`PluginInit()`函数中，使你的代码更容易理解。

在函数`PluginInit()`中：

```cpp
Event::PlayerDieEvent::subscribe([](const Event::PlayerDieEvent& event) {
  Scoreboard::addScore("lldeathcounter", event.mPlayer, 1);
  return true;
});
```

当事件被触发时，该插件会简单地将一个分数添加到该玩家的ID为“lldeathcounter”的记分牌上，并返回true。

## 编译运行

现在你可以编译这个插件，并把你的插件的DLL文件放到BDS的`/plugins/`目录下。
如果你能看到这样的菜单，你就成功了。

![The death count menu](../images/tutorial_death_counter_01.png)