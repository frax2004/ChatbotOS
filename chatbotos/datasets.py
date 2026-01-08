import json
from itertools import chain
from nltk.grammar import CFG
from nltk.parse.generate import generate

####################################################################################################
####################################################################################################
#######                                      GRAMMARS                                        #######
####################################################################################################
####################################################################################################

FILE = """
  FILE -> "file" | "files" | "filename" | "document" | "doc" | "docs" | "script" | "archive" | "item" | "object" | "filepath" | "basename"
"""

NOUN = """
  NOUN -> "path/placeholder.extension" | "placeholder.extension"
"""

FILE_OR_DIR = """
  FILE_OR_DIR -> FILE | DIR
  """

SPECIFIER = """
  SPECIFIER -> "this" | "a" | "that" | "the" |
"""

DIR = """ 
  DIR -> "directory" | "folder" | "path" | "subdir" | "subdirectory" | "dir" | "pathname" | "folderpath" | "filepath"
"""  


RENAME_PRODUCTION_RULES = f"""
  RENAME -> VERB SPECIFIER FILE_OR_DIR ENDING
  
  {FILE}
  {NOUN}
  {FILE_OR_DIR}
  {SPECIFIER}
  {DIR}

  ENDING -> TO NOUN |
  TO -> "to" | "as" | "into" | "in"
  VERB -> "rename" | "renaming" | "renamed" | "change" | "changing" | "changed" | "updating" | "updated" | "modify" | "modifying" | "modified" | "update" | "alter" | "altering" | "replace"  | "replacing" | "relabel"  | "relabeling" | "retitle"  | "retitled" | "ren"
"""

# TODO Verificare che le tre flag create directory e file poste a true non diano problemi
CREATE_FILE_PRODUCTION_RULES = f"""
  CREATE -> VERB SPECIFIER NEW FILE ENDING
  
  NEW -> "new" |

  {FILE}
  {NOUN}
  {SPECIFIER}
  {DIR}

  ENDING -> NAMING NOUN | NAMING NOUN TO DIR NOUN | TO NOUN |
  TO -> "into" | "in" | "at" | "inside" | "within" | "@" | "contained in"
  NAMING -> "named" | "called" | "known as" | "a.k.a"
  VERB -> "create" | "make" | "generate" | "build" | "construct" | "spawn" | "produce" | "setup" | "instantiate" | "touch" | "mkfile" | "new" | "add" | "write" | "form" | "compose" | "allocate" | "initiate"
"""

CREATE_DIR_PRODUCTION_RULES = f"""
  CREATE -> VERB SPECIFIER NEW DIR ENDING
  
  NEW -> "new" |

  {NOUN}
  {SPECIFIER}
  {DIR}

  ENDING -> NAMING NOUN | NAMING NOUN TO DIR NOUN | TO NOUN |
  TO -> "into" | "in" | "at" | "inside" | "within" | "@" | "contained in"
  NAMING -> "named" | "called" | "known as" | "a.k.a"
  VERB -> "create" | "make" | "generate" | "build" | "construct" | "spawn" | "produce" | "setup" | "instantiate" | "touch" | "mkdir" | "md" | "new" | "add" | "write" | "form" | "compose" | "allocate" | "initiate"
"""

DELETE_FILE_PRODUCTION_RULES = f"""
  DELETE -> VERB SPECIFIER FILE ENDING

  {FILE}
  {NOUN}
  {FILE_OR_DIR}
  {SPECIFIER}
  {DIR}

  ENDING -> FROM NOUN | FROM DIR NAMING NOUN |
  NAMING -> "named" | "called" | "known as" | "a.k.a"
  FROM -> "from" | "from within" | "inside" | "within" | "@" | "contained in" | "at" | "found in" | "located" | "located at" | "in"
  VERB -> "delete" | "remove" | "erase" | "destroy" | "kill" | "rm" | "del" | "wipe" | "clear" | "trash" | "discard" | "terminate" | "eliminate" | "scrap" | "cancel" | "drop" | "unlink" | "expunge" | "obliterate" | "bin"

"""

DELETE_DIR_PRODUCTION_RULES = f"""
  DELETE -> VERB SPECIFIER DIR ENDING RECURSIVELY

  {FILE}
  {NOUN}
  {SPECIFIER}
  {DIR}

  RECURSIVELY -> "recursively" | "recursive" | 
  ENDING -> FROM NOUN | FROM DIR NAMING NOUN |
  NAMING -> "named" | "called" | "known as" | "a.k.a"
  FROM -> "from" | "from within" | "inside" | "within" | "@" | "contained in" | "at" | "found in" | "located" | "located at" | "in"
  VERB -> "delete" | "remove" | "erase" | "destroy" | "kill" | "rm" | "del" | "rmdir" | "wipe" | "clear" | "trash" | "discard" | "terminate" | "eliminate" | "scrap" | "cancel" | "drop" | "unlink" | "expunge" | "obliterate" | "bin"
"""

SHOW_FILE_PRODUCTION_RULES = f"""
  SHOW -> VERB SPECIFIER FILE NAMING NOUN ENDING 
  ENDING -> TO NOUN | TO DIR NAMING NOUN | 
  
  {FILE}
  {NOUN}
  {SPECIFIER}
  {DIR}

  TO -> "into" | "in" | "at" | "inside" | "within" | "@" | "contained in" | "located at" | "located in" | "from"
  NAMING -> "named" | "called" | "known as" | "a.k.a"
  VERB -> "show" | "display" | "view" | "cat" | "type" | "print" | "echo" | "read" | "see" | "reveal" | "look" | "check" | "inspect" | "examine" | "output"
"""

SHOW_DIR_PRODUCTION_RULES = f"""
  SHOW -> VERB SPECIFIER DIR NAMING NOUN ENDING 
  ENDING -> TO NOUN | TO DIR NAMING NOUN |
  
  {NOUN}
  {SPECIFIER}
  {DIR}

  TO -> "into" | "in" | "at" | "inside" | "within" | "@" | "contained in"
  NAMING -> "named" | "called" | "known as" | "a.k.a"
  VERB -> "show" | "display" | "view" | "list" | "ls" | "dir" | "cat" | "type" | "print" | "echo" | "read" | "see" | "reveal" | "look" | "check" | "inspect" | "examine" | "output" | "listout"
"""

CHANGE_DIR_PRODUCTION_RULES = f"""
  CHANGE -> VERB TO DIR NOUN | VERB TO NOUN

  {NOUN}
  {DIR}

  TO -> "into" | "in" | "at" | "inside" | "within" | "@" | "contained in" | 
  VERB -> "change" | "modify" | "alter" | "switch" | "swap" | "set" | "cd"  | "shift" | "go" | "put yourself"
"""

COPY_PRODUCTION_RULES = f"""
  COPY -> VERB SPECIFIER FILE_OR_DIR MID ENDING

  {FILE}
  {NOUN}
  {FILE_OR_DIR}
  {SPECIFIER}
  {DIR}

  MID -> FROM DIR NAMING NOUN | FROM NAMING NOUN
  ENDING -> TO NOUN |
  NAMING -> "named" | "called" | "known as" | "a.k.a" |
  FROM -> "from" | "from within" | "inside" | "within" | "@" | "contained in" | "at" | "found in" | "located" | "located at" | "in"
  TO -> "into" | "in" | "at" | "inside" | "within" | "@" | "contained in"
  VERB -> "copy" | "cp" | "scp" | "duplicate" | "replicate" | "clone" | "backup"  | "mirror" | "xcopy" | "robocopy" | "reproduce" | "snapshot" | "sync" | "synchronize" | "transfer" | "multiply" | "reproduct" | "reproduction" | "back-up"

"""

MOVE_PRODUCTION_RULES = f"""
  MOVE -> VERB SPECIFIER FILE_OR_DIR MID ENDING

  {FILE}
  {NOUN}
  {FILE_OR_DIR}
  {SPECIFIER}
  {DIR}

  MID -> FROM DIR NAMING NOUN | FROM NAMING NOUN
  ENDING -> TO NOUN |
  NAMING -> "named" | "called" | "known as" | "a.k.a" |
  FROM -> "from" | "from within" | "inside" | "within" | "@" | "contained in" | "at" | "found in" | "located" | "located at" | "in"
  TO -> "into" | "in" | "at" | "inside" | "within" | "@" | "contained in"
  VERB -> "move" | "mv" | "relocate" | "transfer" | "shift" | "displace" | "reposition" | "migrate" | "migration" | "transport" | "cut" | "paste" | "place" | "put" | "redirect" | "reroute" | "rearrange" | "reorganize" | "drag" | "drop"  | "carry" | "pathing" | "transferring"
"""

PRODUCTION_RULES: dict[str, str] = {
  "RENAME" : RENAME_PRODUCTION_RULES,
  "CREATE_FILE" : CREATE_FILE_PRODUCTION_RULES,
  "CREATE_DIR" : CREATE_DIR_PRODUCTION_RULES,
  "DELETE_FILE" : DELETE_FILE_PRODUCTION_RULES,
  "DELETE_DIR" : DELETE_DIR_PRODUCTION_RULES,
  "SHOW_FILE" : SHOW_FILE_PRODUCTION_RULES,
  "SHOW_DIR" : SHOW_DIR_PRODUCTION_RULES,
  "CHANGE_DIR" : CHANGE_DIR_PRODUCTION_RULES,
  "COPY" : COPY_PRODUCTION_RULES,
  "MOVE" : MOVE_PRODUCTION_RULES,
}

CONTEXT_FREE_GRAMMARS: dict[str, CFG] = {
  "RENAME": CFG.fromstring(RENAME_PRODUCTION_RULES),
  "CREATE_FILE": CFG.fromstring(CREATE_FILE_PRODUCTION_RULES),
  "CREATE_DIR": CFG.fromstring(CREATE_DIR_PRODUCTION_RULES),
  "DELETE_FILE": CFG.fromstring(DELETE_FILE_PRODUCTION_RULES),
  "DELETE_DIR": CFG.fromstring(DELETE_DIR_PRODUCTION_RULES),
  "SHOW_FILE": CFG.fromstring(SHOW_FILE_PRODUCTION_RULES),
  "SHOW_DIR": CFG.fromstring(SHOW_DIR_PRODUCTION_RULES),
  "CHANGE_DIR": CFG.fromstring(CHANGE_DIR_PRODUCTION_RULES),
  "COPY": CFG.fromstring(COPY_PRODUCTION_RULES),
  "MOVE": CFG.fromstring(MOVE_PRODUCTION_RULES),
}


####################################################################################################
####################################################################################################
#######                                      KEYWORDS                                        #######
####################################################################################################
####################################################################################################



RENAME_KEYWORDS: tuple = (
  'rename', 'renaming', 'renamed',
  'change', 'changing', 'changed',
  'modify', 'modifying', 'modified',
  'update', 'updating', 'updated',
  'alter', 'altering',
  'replace', 'replacing',
  'relabel', 'relabeling',
  'retitle', 'retitled'
)

CREATE_KEYWORDS: tuple = (
  'create', 'make', 'generate', 'build', 'construct', 'spawn', 'produce', 
  'initiate', 'setup', 'instantiate', 'touch', 'mkdir', 'mkfile', 'md', 
  'new', 'add', 'addition', 'start', 'write', 'launch', 'establish', 
  'form', 'compose', 'allocate'
)

DIRECTORY_KEYWORDS: tuple = (
  'directory', 'folder', 'path', 'subdir', 'subdirectory', 'dir', 
  'mkdir', 'md', 'cd', 'ls', 'pwd', 'tree', 'location', 'root', 
  'home', 'destination', 'source', 'mount', 'volume', 'pathname',
  'folderpath', 'filepath'
)

FILE_KEYWORDS: tuple = (
  'file', 'files', 'filename', 'document', 'doc', 'docs', 'text', 'txt',
  'script', 'log', 'logs', 'image', 'img', 'photo', 'data', 'pdf', 
  'archive', 'zip', 'item', 'object', 'attachment', 'extension', 'ext',
  'binary', 'bin', 'executable', 'exe', 'readme', 'manifest', 'content',
  'filepath', 'basename'
)

DELETE_KEYWORDS: tuple = (
  'delete', 'remove', 'erase', 'destroy', 'kill', 'purge', 'rm', 'del',
  'rmdir', 'wipe', 'clear', 'trash', 'discard', 'terminate', 'eliminate',
  'scrap', 'cancel', 'drop', 'unlink', 'expunge', 'cleanup', 'clean',
  'obliterate', 'uninstall', 'bin'
)

SHOW_KEYWORDS: tuple = (
  'show', 'display', 'view', 'list', 'ls', 'dir', 'cat', 'type', 'print', 
  'echo', 'read', 'see', 'reveal', 'look', 'check', 'inspect', 'examine', 
  'find', 'locate', 'grep', 'tree', 'more', 'less', 'head', 'tail', 
  'stat', 'status', 'info', 'information', 'contents', 'details', 
  'output', 'map', 'listout'
)

CHANGE_KEYWORDS: tuple = (
  'change', 'modify', 'alter', 'update', 'edit', 'switch', 'swap', 
  'replace', 'convert', 'set', 'reset', 'adjust', 'configure', 'tweak', 
  'toggle', 'cd', 'chmod', 'chown', 'chgrp', 'chsh', 'su', 'sudo', 
  'passwd', 'transform', 'reconfigure', 'shift', 'move'
)

COPY_KEYWORDS: tuple = (
  'copy', 'cp', 'scp', 'duplicate', 'replicate', 'clone', 'backup', 
  'mirror', 'xcopy', 'robocopy', 'rsync', 'reproduce', 'snapshot', 
  'sync', 'synchronize', 'transfer', 'multiply', 'reproduction', 
  'cloning', 'duplication', 'back-up'
)

MOVE_KEYWORDS: tuple = (
  'move', 'mv', 'relocate', 'transfer', 'shift', 'displace', 'reposition', 
  'migrate', 'migration', 'transport', 'cut', 'paste', 'place', 'put', 
  'redirect', 'reroute', 'rearrange', 'reorganize', 'drag', 'drop', 
  'carry', 'pathing', 'transferring'
)

KEYWORDS: dict[str, list[str]] = {
  'RENAME': RENAME_KEYWORDS,
  'CREATE': CREATE_KEYWORDS,
  'DIRECTORY': DIRECTORY_KEYWORDS,
  'FILE': FILE_KEYWORDS,
  'DELETE': DELETE_KEYWORDS,
  'SHOW': SHOW_KEYWORDS,
  'CHANGE': CHANGE_KEYWORDS,
  'COPY': COPY_KEYWORDS,
  'MOVE': MOVE_KEYWORDS
}




















# COMMANDS = json.load(open('data/linuxcommands.json', encoding='utf-8'))

# def categories() -> set[str]:
#   return {
#     'all',
#     'rename',
#     'create',
#     'delete',
#     'show',
#     'change',
#     'copy',
#     'move',
#     'directory',
#     'file',
#   }


# def tagged_commands(categs: set[str] = {'all', }) -> list[dict[str, str]]:

#   categs = { *map(str.lower, categs) }
#   categs.intersection_update(categories())

#   categ2key = {
#     'all': [
#       'REMOVE_DIR', 
#       'CREATE_FILE', 
#       'UNDEFINED', 
#       'SHOW_FILE', 
#       'CREATE_DIR', 
#       'REMOVE_FILE', 
#       'MOVE', 
#       'RENAME', 
#       'SHOW_DIR', 
#       'CHANGE_DIR', 
#       'COPY'
#     ],
#     'rename': ['RENAME'],
#     'create': ['CREATE_FILE', 'CREATE_DIR'],
#     'delete': ['REMOVE_DIR', 'REMOVE_FILE'],
#     'show': ['SHOW_DIR', 'SHOW_FILE'],
#     'change': ['CHANGE_DIR'],
#     'copy': ['COPY'],
#     'move': ['MOVE'],
#     'directory': [
#       'CREATE_DIR', 
#       'SHOW_DIR', 
#       'REMOVE_DIR', 
#       'MOVE', 
#       'RENAME', 
#       'COPY', 
#       'CHANGE_DIR'
#     ],
#     'file': [
#       'CREATE_FILE', 
#       'SHOW_FILE', 
#       'REMOVE_FILE', 
#       'MOVE', 
#       'RENAME', 
#       'COPY'
#     ],
#   }

#   possible_tasks = list(chain(*[keywords for (categ, keywords) in categ2key.items() if categ in categs]))
#   tagged_vocabulary = json.load(open('data/commands-vocabulary.json'))

#   tagged_commands = []
#   for command in COMMANDS:
#     natural_command: str = command['input']
#     source_command: str = command['output'].split(' ')[0]
#     target_tasks: list[str] = tagged_vocabulary[source_command]
#     tagged_command = {'input': natural_command}
#     natural_command_words: list[str] = list(map(str.lower, natural_command.split(' ')))

#     if source_command == 'sudo': 
#       source_command = command['output'].split(' ')[1]

#     if source_command == 'rm': 
#       tagged_command['output'] = 'REMOVE_DIR' if 'directory' in natural_command_words else 'REMOVE_FILE'
#     elif source_command == 'mv': 
#       tagged_command['output'] = 'MOVE' if 'move' in natural_command_words else 'RENAME'
#     else:
#       tagged_command['output'] = target_tasks[0]

#     if tagged_command['output'] in possible_tasks:
#       tagged_commands.append(tagged_command)

#   return tagged_commands
