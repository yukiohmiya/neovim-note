import neovim
import datetime


@neovim.plugin
class NotePlugin(object):
    notes_dir = '~/Documents/notes/'

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False

    @neovim.command("Note", range='', nargs='*')
    def note(self, args, range):
        if self.toggle:
            self.nvim.command('wincmd b')
            self.nvim.command('wq')
        else:
            dt = datetime.date.today()
            today_notes = '{}{}-{}-{}.md'.format(self.notes_dir, dt.year, dt.month, dt.day)
            self.nvim.command('setlocal splitright')
            self.nvim.command('vnew {}'.format(today_notes))
        self.toggle = ~self.toggle
