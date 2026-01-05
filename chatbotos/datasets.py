import json
from itertools import chain

KEYWORDS: dict[str, list[str]] = {
  'RENAME': [
    'rename', 'renaming', 'renamed',
    'change', 'changing', 'changed',
    'modify', 'modifying', 'modified',
    'update', 'updating', 'updated',
    'alter', 'altering',
    'replace', 'replacing',
    'relabel', 'relabeling',
    'retitle', 'retitled'
  ],

  'CREATE': [
    'create', 'make', 'generate', 'build', 'construct', 'spawn', 'produce', 
    'initiate', 'setup', 'instantiate', 'touch', 'mkdir', 'mkfile', 'md', 
    'new', 'add', 'addition', 'start', 'write', 'launch', 'establish', 
    'form', 'compose', 'allocate'
  ],

  'DIRECTORY': [
    'directory', 'folder', 'path', 'subdir', 'subdirectory', 'dir', 
    'mkdir', 'md', 'cd', 'ls', 'pwd', 'tree', 'location', 'root', 
    'home', 'destination', 'source', 'mount', 'volume', 'pathname',
    'folderpath', 'filepath'
  ],

  'FILE': [
    'file', 'files', 'filename', 'document', 'doc', 'docs', 'text', 'txt',
    'script', 'log', 'logs', 'image', 'img', 'photo', 'data', 'pdf', 
    'archive', 'zip', 'item', 'object', 'attachment', 'extension', 'ext',
    'binary', 'bin', 'executable', 'exe', 'readme', 'manifest', 'content',
    'filepath', 'basename'
  ],

  'DELETE': [
    'delete', 'remove', 'erase', 'destroy', 'kill', 'purge', 'rm', 'del',
    'rmdir', 'wipe', 'clear', 'trash', 'discard', 'terminate', 'eliminate',
    'scrap', 'cancel', 'drop', 'unlink', 'expunge', 'cleanup', 'clean',
    'obliterate', 'uninstall', 'bin'
  ],

  'SHOW': [
    'show', 'display', 'view', 'list', 'ls', 'dir', 'cat', 'type', 'print', 
    'echo', 'read', 'see', 'reveal', 'look', 'check', 'inspect', 'examine', 
    'find', 'locate', 'grep', 'tree', 'more', 'less', 'head', 'tail', 
    'stat', 'status', 'info', 'information', 'contents', 'details', 
    'output', 'map', 'listout'
  ],

  'CHANGE': [
    'change', 'modify', 'alter', 'update', 'edit', 'switch', 'swap', 
    'replace', 'convert', 'set', 'reset', 'adjust', 'configure', 'tweak', 
    'toggle', 'cd', 'chmod', 'chown', 'chgrp', 'chsh', 'su', 'sudo', 
    'passwd', 'transform', 'reconfigure', 'shift', 'move'
  ],

  'COPY': [
    'copy', 'cp', 'scp', 'duplicate', 'replicate', 'clone', 'backup', 
    'mirror', 'xcopy', 'robocopy', 'rsync', 'reproduce', 'snapshot', 
    'sync', 'synchronize', 'transfer', 'multiply', 'reproduction', 
    'cloning', 'duplication', 'back-up'
  ],

  'MOVE': [
    'move', 'mv', 'relocate', 'transfer', 'shift', 'displace', 'reposition', 
    'migrate', 'migration', 'transport', 'cut', 'paste', 'place', 'put', 
    'redirect', 'reroute', 'rearrange', 'reorganize', 'drag', 'drop', 
    'carry', 'pathing', 'transferring'
  ]
}


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

COMMANDS = json.load(open('data/linuxcommands.json', encoding='utf-8'))

def categories() -> set[str]:
  return {
    'all',
    'rename',
    'create',
    'delete',
    'show',
    'change',
    'copy',
    'move',
    'directory',
    'file',
  }


def tagged_commands(categs: set[str] = {'all'}) -> list[dict[str, str]]:

  categs = { *map(str.lower, categs) }
  categs.intersection_update(categories())

  categ2key = {
    'all': [
      'REMOVE_DIR', 
      'CREATE_FILE', 
      'UNDEFINED', 
      'SHOW_FILE', 
      'CREATE_DIR', 
      'REMOVE_FILE', 
      'MOVE', 
      'RENAME', 
      'SHOW_DIR', 
      'CHANGE_DIR', 
      'COPY'
    ],
    'rename': ['RENAME'],
    'create': ['CREATE_FILE', 'CREATE_DIR'],
    'delete': ['REMOVE_DIR', 'REMOVE_FILE'],
    'show': ['SHOW_DIR', 'SHOW_FILE'],
    'change': ['CHANGE_DIR'],
    'copy': ['COPY'],
    'move': ['MOVE'],
    'directory': [
      'CREATE_DIR', 
      'SHOW_DIR', 
      'REMOVE_DIR', 
      'MOVE', 
      'RENAME', 
      'COPY', 
      'CHANGE_DIR'
    ],
    'file': [
      'CREATE_FILE', 
      'SHOW_FILE', 
      'REMOVE_FILE', 
      'MOVE', 
      'RENAME', 
      'COPY'
    ],
  }
    
  targets = list(chain(*[keywords for (categ, keywords) in categ2key.items() if categ in categs]))
  tagged_vocabulary = json.load(open('data/commands-vocabulary.json'))

  tagged_commands = []
  for command in COMMANDS:
    natural_command: str = command['input']
    source_command: str = command['output'].split(' ')[0]
    target_tasks: list[str] = tagged_vocabulary[source_command]
    tagged_command = {'input': natural_command}
    natural_command_words: list[str] = list(map(str.lower, natural_command.split(' ')))

    if source_command == 'rm': 
      tagged_command['output'] = 'REMOVE_DIR' if 'directory' in natural_command_words else 'REMOVE_FILE'
    elif source_command == 'mv': 
      tagged_command['output'] = 'MOVE' if 'move' in natural_command_words else 'RENAME'
    else:
      tagged_command['output'] = target_tasks[0]

    if tagged_command['output'] in targets:
      tagged_commands.append(tagged_command)

  return tagged_commands
