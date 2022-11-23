# Quickstart {#quickstart}

## Prerequisites

### For You

You'll need to know the basic syntax of C++.
For a refresher to C++, see the [C++ tutorial](https://cplusplus.com/doc/tutorial/).
So should you have successfully run LiteLoaderBDS at least one time and have skimmed the [LiteLoaderBDS documentation](https://docs.litebds.com/en/#/README) except the pages for plugin development in order to comprehense how LiteLoaderBDS works.

### For Your Computer

Currently we only support building plugins on a tiny set of platforms.
If you could assist us in leveraging supported platforms, we would sincerely appreciate it.

The platforms required is shown below:

* Windows 10 64-bit / Windows 11

The software required is shown below:

* Bedrock Dedicated Server for Minecraft [Download](https://www.minecraft.net/en-us/download/server/bedrock)
* Git [Download](https://git-scm.com/download/win)
* LiteLoaderBDS [Download](https://github.com/LiteLDev/LiteLoaderBDS/releases/latest)
* Microsoft Visual Studio 2022 (with Microsoft Visual C++) [Download](https://visualstudio.microsoft.com/vs/)

At the same time, we recommend that you install these software for better experience:

* CMake 3.21 or higher versions [Download](https://cmake.org/download/)
* C/C++ Extension Pack of Visual Studio Code
* GitHub Desktop [Download](https://desktop.github.com/)
* Minecraft Bedrock Edition
* Visual Studio Code [Download](https://code.visualstudio.com/download)

What's more, we highly recommend that you register a GitHub account, not only for writing the plugin but also for optimizing your future coding experience.

## Create Your First Plugin

Now that you have got the development environment ready, it is time that you create your first plugin from scratch.

### Get the repository URL

* If you would like to host your code on GitHub, visit [the plugin template repository](https://github.com/LiteLDev/PluginTemplate-cpp) and click the button with text "Use this template", then filling in the form to create your plugin repository.
Then copy the URL of your repository.

    ![Use the Template](../images/quickstart_01.png)

* If you would just like to develop locally, copy `https://github.com/LiteLDev/PluginTemplate-cpp` to your clipboard.

### Clone the repository

* Open PowerShell or Command Prompt where you would like to put the repository, and then run `git clone --recurse-submodules <repository URL>`.
Note that you should replace the tag `<repository URL>` with the URL you copied in the previous step.
And the flag `--recurse-submodules` is required.

    ![Git Clone](../images/quickstart_02.png)

### Configure the plugin

Modify the configurations in `/src/Version.h` following the instructions inside the file.
Remember to delete the line starting with "static_assert".
Here we are explaining the configurations in detail.

First fill in the basic information, the name of the plugin, a brief one-line description and your name included.
Please pay attention that the plugin name should only contain English alphabet, digit, dash(-) and underscore(_).
Though currently LiteLoaderBDS does not check it, future versions of LiteLoaderBDS may forbid other characters in consideration of security.

```cpp
#define PLUGIN_NAME "My Plugin"
#define PLUGIN_INTRODUCTION "My Plugin is a plugin printing \"Hello, World!\" in the console."
#define PLUGIN_AUTHOR "Me"
```

Then set the plugin version.
Please refer to https://semver.org for more reference.
We provide three status preset: **dev**, **beta** and **release**, by the macro `PLUGIN_VERSION_STATUS` with `PLUGIN_VERSION_DEV`, `PLUGIN_VERSION_BETA` and `PLUGIN_VERSION_RELEASE`.
Some compiler and link behaviors varies with different preset, but you do not need to care about it.
If the version is still under development, choose **dev**.
If the version is the first one of the minor version to be published, or you don't have confidence in its statbility, choose **beta**.
If the version is ready for everyone to use without doubt, choose **release**.
You should only regard the **release** versions as the formal published versions.

```cpp
#define PLUGIN_VERSION_MAJOR 1
#define PLUGIN_VERSION_MINOR 0
#define PLUGIN_VERSION_REVISION 0
#define PLUGIN_VERSION_BUILD 0

#define PLUGIN_VERSION_STATUS PLUGIN_VERSION_DEV
```

Next, set the target BDS protocol version.
A few developers tend to ignore this configuration and just comment it.
Nevertheless, we highly NOT recommend you do so, for some APIs varies accross versions, which may cause severe unexpectable exceptions or even corruption of files.

You should have LiteLoaderBDS and BDS installed.
And then run **bedrock_server_mod.exe** and locate this line:

![Protocol Version Line](../images/quickstart_03.png)

Check the protocol version.
In the image above, the protocol version is 544.

Fill in the protocol version.

```cpp
#define TARGET_BDS_PROTOCOL_VERSION 545
```

### Build the plugin

* If you would like to build with CMake in Visual Studio Code (recommended), simply open the repository directory in Visual Studio Code, choose **Release** build variant (or others as you like), and click **Build**.
Then the plugin will be generated in `/build/Release/Plugin.dll` (or others depending on the build variant you chose).

* If you would like to build with CMake directly, create the directory `/build/`. Then open PowerShell or Command Prompt in `/build/` and run `cmake .. && cmake --build . -j`.
Then the plugin will be generated as `/build/Plugin.dll`.

* If you would like to build with Microsoft Visual Studio, open the repository directory in Microsoft Visual Studio, click **Build** -> **Build All** or just press `Ctrl` + `Shift` + `B` to build.
Then the plugin will be generated as `/out/x64-Debug/Plugin.dll`.

### Run your plugin

opy the `Plugin.dll` generated in the previous step to the `/plugin/` directory of the BDS directory (if not found, you should apply LiteLoaderBDS to BDS first. Please refer to [the instructions](https://docs.litebds.com/en/#/Usage)).

Run `/bedrock_server_mod.exe` in the BDS directory.

### Observe the plugin behavior

Now you can see the text "Hello, world!" shown on the terminal.

Congratulations to you for successfully creating your first plugin!

## Make Furthur Modifications

I bet you not satisfied with just a hello-world trick, which can be easily implemented by any C or C++ program, so let's do some further work.

There exists a question in refreshers' mind: how to **interact** with the Minecraft world when something **happens**?

Well, this question is exactly the meaning of a LiteLoaderBDS plugin.

To go into details, let's break the question into two parts, which have been marked out, and discuss the solutions of each part.

First, the interaction with the Minecraft world.
LiteLoaderBDS provides plentiful APIs performing operations to the world directly.
Via these APIs, you can get an entity or a block, set a block, or run a line of command.
However, the definitions of these APIs are not collected in a single header file, but splitted into multiple classes.
You can refer to `/SDK/include/llapi/GlobalServiceAPI.h` to see the classes containing these APIs.
In this article, we will use the **Level** class, the most common class for plugin development.

Second, the watcher on the occurrence of some events.
Though BDS has not provided any event related APIs like those in GameTest, we hooked some common events for you.
To check out all of them, you can have a glance at `/SDK/include/llapi/EventAPI.h`.
In this article, we will use the **PlayerJoinEvent**.

Following the instructions below, you will create a plugin giving every player an emerald and show welcome banner on every player's screen when they join the game as well as showing the latest joined player's name when someone types command `latest`.
Are you ready?
Let's start.

Open `/src/Plugin.cpp`, and follow instructions below.

1. Include necessary headers.

    ```cpp
    #include <string>

    #include <llapi/MC/CommandOrigin.hpp>
    #include <llapi/MC/CommandOutput.hpp>
    #include <llapi/MC/ItemStack.hpp>
    #include <llapi/MC/Level.hpp>
    #include <llapi/MC/Player.hpp>
    #include <llapi/MC/Types.hpp>

    #include <llapi/DynamicCommandAPI.h>
    #include <llapi/EventAPI.h>
    #include <llapi/GlobalServiceAPI.h>
    ```

    So many headers, right?
    To better manage them, we recommend that you include a new header if and only if the type of some variables or constants is defined in the header, or without including the header, your plugin cannot be built.
    Meanwhile, you should group these headers.
    One possible policy is grouping headers started with `MC/` into a group, STL headers into another group, and all other headers into the final group.

2. Define the global variables.

    ```cpp
    std::string latest_player_xuid;
    ```

    This variable is used to store the XUID of the latest joined player.

3. Listen to the event.

    Code below should be placed in the `PluginInit()` function.

    ```cpp
    Event::PlayerJoinEvent::subscribe([](const Event::PlayerJoinEvent& event) {
      // Give the item to the player
      auto* item = ItemStack::create("minecraft:emerald", /* count = */ 1);
      event.mPlayer->giveItem(item);
      delete item;

      // Show banner on every player's screen
      auto all_player_list = Level::getAllPlayers();
      for (auto* player : all_player_list) {
        player->sendTitlePacket(
          event.mPlayer->getRealName() + "joined",
          TitleType::SetTitle,
          /* FadeInDuration = */ 1,
          /* RemainDuration = */ 3,
          /* FadeOutDuration = */ 1
        );
      }

      return true;
    });
    ```

    In this piece of code, we subscribe to PlayerJoinEvent with a anonymous callback function.

    In the callback function, we firstly create an item stack, which representing a collection of identical items that can be picked up at a time, whose identifier is `minecraft:emerald` and whose stack count is one.
    Then we directly extract the player from the event object and give the player the item stack.

    Then we attempt to get all players, iterating over all of them and sending the newly joined player's name to them as titles.

    Finally, we return true, indicating that the player can join the server.
    Otherwise, if we return false, the player will be rejected from the server.
    (If you are creative and sharp enough, you may come up with the idea that these feature can be used to create a customized whitelist rule set.)

4. Register the command

    Code below should be placed in the **PluginInit()** function.

    ```cpp
    DynamicCommand::setup(
      /* name = */ "latest",
      /* description = */ "Get latest player.",
      /* enums = */ {},
      /* params = */ {},
      /* overloads = */ {
        {},
      },
      /* callback = */ [](
        DynamicCommand const& command,
        CommandOrigin const& origin,
        CommandOutput& output,
        std::unordered_map<std::string, DynamicCommand::Result>& results
      ) {
        output.success(
          std::string("The latest player's name is ") +
          Global<Level>->getPlayer(latest_player_xuid)->getRealName()
        );
      }
    );
    ```

    If you are interested in the meanings of the parameters, please refer to the DynamicCommand class.

    Now you can build the plugin and test it in LiteLoaderBDS.

## Debug Your Plugin

Open the directory of your plugin in Microsoft Visual Studio, and the project will be configured automatically.

Change **Solution Explorer** to CMake target view, right click on the project, and then select **Add Debug Configuration** to create `launch.vs.json`.

Then modify the project target value to the BDS executable `bedrock_server_mod.exe`.

Press F5 to debug your plugin.

## What's Next?

If you are still confused and not ready to create a plugin on your own, please see our [tutorials](90_tutorials_index.md).
We highly recommend you read [Death Counter](tutorials/death_counter.md), which is an analysis of [LLDeathCounter](https://github.com/Futrime/LLDeathCounter), a simple player death recorder.

If you want to browse the APIs, start from [the Level class](#Level).

If you are interested in more advanced techniques in plugin development, please see our [guides](91_guides_index.md).

If you have doubt about certain APIs, or if you would like to know what can your plugin do with the APIs, please [lookup the classes](/en/classes.html).

If you are eager to dive into the ocean of BDS APIs, please refer to [the API reference](/api).

If you are ready to contribute to this documentation, please go to [our documentation repository](https://github.com/LiteLDev/docs-cpp), raising issues or opening pull requests.

We sincerely wish you a wonderful plugin development experience!