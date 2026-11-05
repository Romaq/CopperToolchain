# Start here: your own Claude.ai project plus GitHub repository

This kit lets you do what the CopperToolchain project did: keep a Claude.ai project and a GitHub
repository side by side, with every conversation logged, decisions recorded, and privacy checked.
It is a pattern to adapt, not a setup to copy. Your goals, hardware, and comfort with scripts are yours.

## Step 0: decide three things

1. **Public or private repository?** The CopperToolchain repository is public, which is why its tools
   include a privacy check. If you choose private, you can relax some caution, but build the habit anyway:
   a private repository can become public by accident or by sharing. If you choose public, your lab's
   details (addresses, hostnames, services, how it is reached from outside) must never appear in it.
2. **What are you after?** Write two sentences. Prompt 2 will help refine them into goals later.
3. **Which license, if any?** Without a license, others have no legal permission to reuse your code, even
   if you intend them to. On GitHub you can add a `LICENSE` file from the web interface (Add file, Create new file,
   name it `LICENSE`, then choose a license template). The CopperToolchain repository uses the Unlicense.

## Step 1: name it

Use `prompts/01-name-your-project.md`. A good name says what the project is for, is not generic
(a name like "Home Lab" is lost among thousands of others), and works on both sides. The Claude.ai project name
may have spaces (for example "The Copper Toolchain"); the repository name may not (`CopperToolchain`).

## Step 2: create the repository and local folder

    ./bootstrap-project.sh "<Project Name>" <your-github-user>

It creates `~/Projects/<RepoName>` with logging, sync, and privacy tools, installs the privacy hook, and makes the
first commit. Create the matching empty repository on github.com and push (the script prints the commands).
It cannot create the Claude.ai project for you.

## Step 3: create the Claude.ai project

1. In Claude.ai, create a new project with the same name.
2. Open `templates/claude-project-instructions.md` in your new folder, fill in the "About this project"
   paragraph, and paste everything below the line into the project's instructions.
3. Check the project's memory setting on its page and decide whether the project's memory should be kept
   separate from your general memory. Separate is the safer default for a project that will be published.
4. Add the CopperToolchain project guide (`docs/PROJECT-GUIDE.md`) to the project's files. See "Reading CopperToolchain" below.

## Step 4: choose how you will log conversations

Use `prompts/05-choose-logging-method.md`. CopperToolchain uses clipboard shortcuts, but that suits Linux and a
comfort with scripts. Summary-only logging is a legitimate, lower-effort choice. Pick what you will actually keep doing.

## Step 5: find your goals

1. Copy `surveys/01-goals.md` to `surveys/responses/` and fill it in there. That folder is git-ignored.
2. Attach the filled file to a chat message. Do not paste it into the logged text.
3. Use `prompts/02-goals-from-survey.md`. Publish only the result (`docs/goals.md`), which holds no private details.

## Step 6: work in small steps, and write decisions down

- A new service must earn its place. Ask: what problem does it solve today, what breaks if it fails, how many
  minutes a month does it cost, can I rebuild it from a short recipe, and is there a simpler 80% solution?
- Record each decision in `docs/decisions/` in a few lines, including decisions to do nothing.
- Run `scripts/privacy-check.sh` before pushing. The hook does it for you.

## Reading CopperToolchain

- Read `docs/PROJECT-GUIDE.md` first. It lists the important elements and what to search for.
- To get a digest, give your project the CopperToolchain files and use `prompts/03-digest-copper-toolchain.md`.
- If your project cannot answer a question from those files, use `prompts/04-questions-for-copper-toolchain.md`. It writes a
  ready-to-send question for the CopperToolchain owner. Basic questions are welcome: an unanswered question shows where the
  documentation has a gap.

## What not to copy blindly

- Hardware, network arrangements, names, and paths that are specific to someone else's setup.
- Tools you do not need yet. Start with logging and the privacy check, and add the rest when a real problem calls for it.
- Anything that cannot be rebuilt from a short written recipe.

## Staying safe

- Never put credentials, tokens, keys, or personal details in logs, files, or prompts.
- Remember `git rm` removes a file only from the newest snapshot. History keeps it. See
  `docs/runbooks/sensitive-data-in-git.md` for what to do, in proportion to what leaked.
- The kit's scripts were tested on Linux only. The macOS clipboard line in `log-turn.sh` is untested, and Windows is not covered.
