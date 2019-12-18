import neovim
import datetime
import os


@neovim.plugin
class NotePlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False
        if 'notes_dir' in self.nvim.vars:
            self.notes_dir = self.nvim.vars['notes_dir']

    @neovim.command("Note", range='', nargs='*')
    def note(self, args, range):
        if self.toggle:
            self.nvim.command('wincmd b')
            try:
                self.nvim.command('wq')
            except Exception:
                pass
        else:
            dt = datetime.date.today()
            todays_note = '{}/{}-{}-{}.md'.format(self.notes_dir, dt.year, dt.month, dt.day)
            self.nvim.command('setlocal splitright')
            self.nvim.command('vnew {}'.format(todays_note))
            if not os.path.isfile(todays_note):
                self.nvim.current.line = ('# {}-{}-{}'.format(dt.year, dt.month, dt.day))
        self.toggle = ~self.toggle
