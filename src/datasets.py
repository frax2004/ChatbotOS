
class Datasets:
  KEYWORDS: dict[str: tuple[str]] = {
    'RENAME': (
      'rename', 'renaming', 'renamed',
      'change', 'changing', 'changed',
      'modify', 'modifying', 'modified',
      'update', 'updating', 'updated',
      'alter', 'altering',
      'replace', 'replacing',
      'relabel', 'relabeling',
      'retitle', 'retitled'
    ),
    'CREATE': (
      'create', 'make', 'generate', 'build', 'construct', 'spawn', 'produce', 
      'initiate', 'setup', 'instantiate', 'touch', 'mkdir', 'mkfile', 'md', 
      'new', 'add', 'addition', 'start', 'write', 'launch', 'establish', 
      'form', 'compose', 'allocate'
    ),
    'DIRECTORY': (
      'directory', 'folder', 'path', 'subdir', 'subdirectory', 'dir', 
      'mkdir', 'md', 'cd', 'ls', 'pwd', 'tree', 'location', 'root', 
      'home', 'destination', 'source', 'mount', 'volume', 'pathname',
      'folderpath', 'filepath'
    ),
    'FILE': (
      'file', 'files', 'filename', 'document', 'doc', 'docs', 'text', 'txt',
      'script', 'log', 'logs', 'image', 'img', 'photo', 'data', 'pdf', 
      'archive', 'zip', 'item', 'object', 'attachment', 'extension', 'ext',
      'binary', 'bin', 'executable', 'exe', 'readme', 'manifest', 'content',
      'filepath', 'basename'
    ),
    'DELETE': (
      'delete', 'remove', 'erase', 'destroy', 'kill', 'purge', 'rm', 'del',
      'rmdir', 'wipe', 'clear', 'trash', 'discard', 'terminate', 'eliminate',
      'scrap', 'cancel', 'drop', 'unlink', 'expunge', 'cleanup', 'clean',
      'obliterate', 'uninstall', 'bin'
    ),
    'SHOW': (
      'show', 'display', 'view', 'list', 'ls', 'dir', 'cat', 'type', 'print', 
      'echo', 'read', 'see', 'reveal', 'look', 'check', 'inspect', 'examine', 
      'find', 'locate', 'grep', 'tree', 'more', 'less', 'head', 'tail', 
      'stat', 'status', 'info', 'information', 'contents', 'details', 
      'output', 'map', 'listout'
    ),
    'CHANGE': (
      'change', 'modify', 'alter', 'update', 'edit', 'switch', 'swap', 
      'replace', 'convert', 'set', 'reset', 'adjust', 'configure', 'tweak', 
      'toggle', 'cd', 'chmod', 'chown', 'chgrp', 'chsh', 'su', 'sudo', 
      'passwd', 'transform', 'reconfigure', 'shift', 'move'
    ),
    'COPY': (
      'copy', 'cp', 'scp', 'duplicate', 'replicate', 'clone', 'backup', 
      'mirror', 'xcopy', 'robocopy', 'rsync', 'reproduce', 'snapshot', 
      'sync', 'synchronize', 'transfer', 'multiply', 'reproduction', 
      'cloning', 'duplication', 'back-up'
    ),
    'MOVE': (
      'move', 'mv', 'relocate', 'transfer', 'shift', 'displace', 'reposition', 
      'migrate', 'migration', 'transport', 'cut', 'paste', 'place', 'put', 
      'redirect', 'reroute', 'rearrange', 'reorganize', 'drag', 'drop', 
      'carry', 'pathing', 'transferring'
    )
  }

  RENAME_KEYWORDS: tuple[str] = KEYWORDS['RENAME']
  CREATE_KEYWORDS: tuple[str] = KEYWORDS['CREATE']
  DIRECTORY_KEYWORDS: tuple[str] = KEYWORDS['DIRECTORY']
  FILE_KEYWORDS: tuple[str] = KEYWORDS['FILE']
  DELETE_KEYWORDS: tuple[str] = KEYWORDS['DELETE']
  SHOW_KEYWORDS: tuple[str] = KEYWORDS['SHOW']
  CHANGE_KEYWORDS: tuple[str] = KEYWORDS['CHANGE']
  COPY_KEYWORDS: tuple[str] = KEYWORDS['COPY']
  MOVE_KEYWORDS: tuple[str] = KEYWORDS['MOVE']
