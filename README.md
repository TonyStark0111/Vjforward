# VJ Forward Bot

![Typing SVG](https://readme-typing-svg.herokuapp.com/?lines=Welcome+To+VJ+Forward+Bot+!)

## Features

- [x] Public Forward (Bot)
- [x] Private Forward (User Bot)
- [x] Custom Caption 
- [x] Custom Button
- [x] Skip Duplicate Messages
- [x] Skip Messages Based On Extensions & Keywords & Size
- [x] Filter Type Of Messages
- [x] Auto Restart Pending Task After Bot Restart
- [x] Link Removal - Removes all URLs and mentions from captions
- [x] Forward Delay - Custom delay between forwarded messages (0 = default based on bot type)
- [x] Replacement Link - Replaces all URLs/mentions with:
   · Telegram username (e.g., @mynewchannel)
   · Custom URL (e.g., https://example.com)
- [x] HTML Tag Cleaning - Removes anchor tags like <a href="...">...</a> automatically
- [x] Per-User Settings - All settings are stored per user in the database
https://example.com Auto Migration - Existing users automatically get default values for new settings
- [x] Batch Forward Optimization - Automatically switches to individual copying when link modifications are enabled
      
## Commands

```
start - check I'm alive 
forward - forward messages
unequify - delete duplicate media messages in chats
settings - configure your settings
stop - stop your ongoing tasks
reset - reset your settings
restart - restart server (owner only)
resetall - reset all users settings (owner only)
broadcast - broadcast a message to all your users (owner only)
```

## Variables

* `API_ID` API Id from my.telegram.org
* `API_HASH` API Hash from my.telegram.org
* `BOT_TOKEN` Bot token from @BotFather
* `BOT_OWNER` Telegram Account Id of Owner.
* `DATABASE_URI` Database uri from [MongoDB](https://mongodb.com) Watch [Video Tutorial](https://youtu.be/DAHRdFdw99o)

## Credits

* <b>[Tech VJ]</b>
