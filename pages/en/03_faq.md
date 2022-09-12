# Frequently Asked Questions {#faq}

## How to get ...?

For any objects related to the game, you should check the headers in `MC/` .
All static LIAPIs and MCAPIs can be directly called.
You should prefer LIAPIs, for some MCAPIs do not act as you think.

You can also check the headers in `/` .

## Where to start browsing the APIs?

You should start from [the Level class](#Level).

If you want to create an object, you may be interested in the `create()` methods of classes.

## Why does my plugin throw an SEH exception when initializing?

When the function `PluginInit()` is called, the game is not loaded. If your plugin access anything related to the game, it is bound to throw an exception.

Please access anything related to the game after `ServerStartedEvent` fires.