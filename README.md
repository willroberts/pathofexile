# pathofexile

A Python framework for building tools related to Path of Exile.

Includes a complete implementation of the Path of Exile Developer API, tools
for analytics, and tools for forum scraping.

## Features

* Full implementation of the Path of Exile API
  * Leagues
  * League Rules
  * Ladders
* Concurrent request mapping and caching for faster ladder retrievals
* Support for downloading and parsing the CSV ladders
* Analytics utilities for generating and printing ladder statistics
* Shop thread parser which generates Item() objects
* Forum post isolator which embeds the first post of a shop thread

## Requirements

* Python 2.x

## Documentation

1. <a href='docs/setup.md'>Setup</a>
2. <a href='docs/api.md'>Core API</a>
3. <a href='docs/ladders.md'>Ladders</a>
4. <a href='docs/analytics.md'>Analytics</a>
5. <a href='docs/items.md'>Items</a>
6. <a href='docs/posts.md'>Forum Posts</a>

## Contributing

Pull requests are highly encouraged! If you see room for improvement, fork the
code, commit your patch, and then send a pull request so I can merge it in.

To get started, check out `to_do.md` in this directory, and see the
<a href="#documentation">documentation</a>.
