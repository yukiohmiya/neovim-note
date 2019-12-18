import neovim
import datetime
import os


@neovim.plugin
class NotePlugin(object):
    DEBUG = False

    def __init__(self, nvim):
        self.nvim = nvim
        self.toggle = False
        if 'notes_dir' in self.nvim.vars:
            self.notes_dir = self.nvim.vars['notes_dir']

    def get_output_of_vim_cmd(self, nvim, cmd):
        """ Utility function to get the current output
            of a vim command
        Parameters:
            nvim: Neovim instance
            cmd: Command to fetch output from
        Returns:
            n/a
        """
        nvim.command('redir @a')
        nvim.command(cmd)
        nvim.command('redir END')
        return nvim.eval('@a').strip()

    def log_to_file(self, *args):
        if self.DEBUG:
            with open('./nvim.log', 'a') as fp:
                dt = datetime.datetime.now()
                fp.write('[{}] {}\n'.format(dt.strftime('%Y-%m-%d %H:%M:%S'),
                                            ' '.join(args)))

    def close_note(self):
        self.nvim.command('wincmd b')
        res = self.get_output_of_vim_cmd(self.nvim, 'set buftype?')
        if self.notes_dir in self.nvim.current.buffer.name:
            self.nvim.command('wq')
        elif res == 'buftype=nofile':
            self.nvim.command('q')

    @neovim.command("Note", range='', nargs='*')
    def note(self, args, range):
        self.log_to_file('==== START Note ====')

        self.log_to_file(str(dir(self.nvim.current.buffer)))

        self.log_to_file(str(self.nvim.current.buffer.number))
        self.log_to_file('Buffer Name:', self.nvim.current.buffer.name)

        if self.toggle:
            self.close_note()
        else:
            dt = datetime.date.today()
            todays_note = '{}/{}-{}-{}.md'.format(self.notes_dir, dt.year, dt.month, dt.day)
            self.nvim.command('setlocal splitright')
            self.nvim.command('vsplit')
            self.nvim.command('edit {}'.format(todays_note))

            self.log_to_file(str(self.nvim.current.buffer.number))

            if not os.path.isfile(todays_note):
                self.nvim.current.line = ('# {}-{}-{}'.format(dt.year, dt.month, dt.day))
        self.toggle = ~self.toggle

        self.log_to_file('==== END Note ====')

    @neovim.command("NoteList", range='', nargs='*')
    def notelist(self, args, range):
        self.log_to_file('==== START Note ====')

        if self.toggle:
            self.close_note()
        else:
            self.nvim.command('setlocal splitright')
            self.nvim.command('vsplit')
            self.nvim.command('e {}'.format(self.notes_dir))

            self.log_to_file(str(self.nvim.current.buffer.number))
            self.log_to_file('Buffer Name:', self.nvim.current.buffer.name)

        self.toggle = ~self.toggle

        self.log_to_file('==== END Note ====')
