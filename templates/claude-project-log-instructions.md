## Conversation log format

My conversations in this project are logged to a Markdown file, so format every reply for direct pasting:

1. Begin every reply with a horizontal rule (`---`), then this heading:
   `## 🤖 CLAUDE · Turn N · YYYY-MM-DD`
   - N is the number of messages I have sent in this conversation so far.
   - The date is today's date as given in your context. If you do not know it, ask me instead of guessing.
2. Write the rest of the reply in plain Markdown. Use headings, lists, and tables only where they help.
3. When showing Markdown or code that itself contains triple-backtick fences, wrap it in a four-backtick fence so it pastes cleanly.
4. End every reply with a horizontal rule (`---`).
5. Do not add commentary about the format itself. Just follow it.
6. If I write "log my turn", reply with my previous message formatted as:
   `## 🧑 USER · Turn N · YYYY-MM-DD`, followed by my message as a blockquote (every line prefixed with `> `).