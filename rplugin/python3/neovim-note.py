import neovim
import datetime


@neovim.plugin
class MemoPlugin(object):
    notes_dir = '~/Documents/notes/'
    dt = datetime.date.today()
    today_notes = '{}{}-{}-{}.md'.format(notes_dir, dt.year, dt.month, dt.day)

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False

    @neovim.command("Memo", range='', nargs='*')
    def memo(self, args, range):
        if self.toggle:
            self.nvim.command('wincmd b')
            self.nvim.command('wq')
        else:
            self.nvim.command('setlocal splitright')
            self.nvim.command('setlocal columns=100')
            self.nvim.command('vnew {}'.format(self.today_notes))
        self.toggle = ~self.toggle
