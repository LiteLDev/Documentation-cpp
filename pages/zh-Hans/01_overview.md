# 概览 {#overview}

## 何为LiteLoaderBDS C++插件

简单来说，LiteLoaderBDS C++插件是对Minecraft基岩版专用服务器（BDS）的修改器，拓展了各种玩法、规则和实用工具。
在我们眼中，LiteLoaderBDS C++插件是与BDS底层交互的最硬核的方式，和其它插件相比，具有无可比拟的优势，但也有一定的劣势。

## 优缺点

优点：在大量的API帮助下，您可以如Minecraft官方开发者一样开发，实现一切功能，唯一的桎梏是您的想象力。
（事实上，LiteLoaderBDS提供的大部分API就是从BDS调试文件提取的的原生API。）

缺点：由于缺乏官方支持，我们只能使用一些“魔法”如Windows Hook机制和内存Patch机制对部分API进行重现，这导致这些API可能不稳定，造成崩服或数据丢失。

## 更多的API

您不仅能够使用BDS原生API（前缀`MCAPI`），也可以使用我们另外提供的API（前缀`LIAPI`）。
这些API大多替代了晦涩难懂的原生API，以期为您提供至高便利。
如果您发现某些原生API难以使用，请提出一个Issue通知我们。
我们将会考虑创建相关的API。

此外，我们还提供了诸多实用工具，例如数据库工具、发包工具、权限工具、表单工具、定时器工具等等。
我们也继承了部分第三方库，例如著名的nlohmann::json库和Base64库。

## 代码一瞥

让我们看一眼代码。
这段代码用于对刚加入的玩家展示欢迎标语并在后台提示其名字。

```cpp

#include <EventAPI.h>
#include <LoggerAPI.h>
#include <MC/Player.hpp>
#include <MC/Types.hpp>

void PluginInit()
{
  Logger logger;

  Event::PlayerJoinEvent::subscribe([](const Event::PlayerJoinEvent& event) {
    auto player = event.mPlayer;
    
    player->sendTitlePacket(
      "Welcome!",
      TitleType::SetTitle,
      /* FadeInDuration =  */ 1,
      /* RemainDuration =  */ 2,
      /* FadeOutDuration =  */ 1
    );

    logger.info("Player {} has joined the server.", player->getName());
  });
}

```

这段代码首先定义了一个日志记录器，用于输出信息到BDS控制台，然后订阅了PlayerJoinEvent事件。
一旦玩家加入（不妨设其名字为Notch），程序将对Notch发送一个内容为“Welcome！”的标题，并持续显示两秒钟；同时在后台显示“Player Notch has joined the server.”

## 下一步

如果你准备好写插件了，或者只是觉得这些代码优雅，请移步[快速开始](02_quickstart.md)以获得更多指导。