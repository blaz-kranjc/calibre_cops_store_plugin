# COPS Store Plugin

A simple plugin for [calibre](https://calibre-ebook.com/) that can consume a library from a [COPS](https://blog.slucas.fr/projects/calibre-opds-php-server/) server as a store. This plugin should also work with any other OPDS servers.

## Installation and configuration
1. Close any currently open instances of calibre.
1. Run the following command in the root directory of this project: ` calibre-customize -b .`
1. Start calibre and click the __Get books__ button.
1. Click on __Configure__ button inside the pop-up.
1. Configure the plugin by right clicking on __COPS store__ plugin entry and pressing __Configure...__.
1. Enter the configuration parameters. The plugin requires the URL to point to the OPDS root of the server (*/feed.php* on COPS server). Username and password are optional.
1. Press __OK__ and close the __Configure__ window.
1. Check the box next to the __COPS store__ in the left pane of __Get books__ pop-up.
1. Search for books in the newly configured store.
