# Publication checklist

Before pushing this repository to a public remote:

- run `./tools/publication_audit.sh`;
- confirm `git status --ignored` contains no model, map, bag, log, result, or credential files;
- review external package, topic, and protocol names with the project owner;
- confirm every dependency is fetched from its upstream project or supplied by the user;
- inspect `git diff --cached` and the initial commit contents;
- create repository secrets at deployment time rather than committing them.

The automated audit catches common leaks but cannot determine contractual or
organizational confidentiality. The final staged-content review is therefore
part of the publication process.
